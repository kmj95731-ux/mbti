from fastapi import FastAPI, HTTPException, Query, Response
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
import xml.etree.ElementTree as ET
import asyncio
import json
import os
import re
import time as _time
import threading as _threading
from typing import Optional, Tuple
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

from .database import init_db, count_items, seed_from_json as _seed, get_conn as _get_conn
from .database import count_items as _count_items
from .crawler import crawl_state, run_crawl
from .search_engine import hybrid_search, build_index, invalidate_cache, _normalize_ko_query, _KW_STOPWORDS
from .search_engine import build_index as _build_index
from .claude_chat import get_librarian_response

app = FastAPI(title="도서 큐레이션 API")

# ── 실시간 접속자 추적 ────────────────────────────────────────
_presence: dict[str, float] = {}
_PRESENCE_TTL = 90  # 90초 이상 ping 없으면 오프라인 처리

# ── CORS 화이트리스트 ────────────────────────────────────────
_cors_default = (
    "http://localhost:8000,http://127.0.0.1:8000,"
    "https://dongle0516-mbtibooktalk.hf.space,"
    "https://marvinloveyou12-rgb.github.io"
)
_cors_env = os.getenv("CORS_ALLOW_ORIGINS", _cors_default).strip()
_cors_origins = ["*"] if _cors_env == "*" else [
    o.strip() for o in _cors_env.split(",") if o.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# ── 앱 시작 시 DB 초기화 + 인덱스 복구 ──────────────────────
init_db()

def _startup():
    _seed()
    if _count_items() > 0:
        # word-level TF-IDF로 교체 후 첫 기동 시 기존 char_wb 캐시 자동 무효화
        from pathlib import Path as _P
        import pickle as _pk
        cache = _P(__file__).parent / "tfidf_cache.pkl"
        if cache.exists():
            try:
                with open(cache, "rb") as _f:
                    _meta = _pk.load(_f)
                # vectorizer analyzer가 char_wb이면 낡은 캐시 → 삭제 후 재빌드
                _old_vec = _meta.get("vectorizer")
                if _old_vec and getattr(_old_vec, "analyzer", None) == "char_wb":
                    cache.unlink()
                    print("[startup] char_wb 캐시 감지 → 삭제 후 word-level 재빌드")
            except Exception:
                cache.unlink(missing_ok=True)
        _build_index()
        # 시맨틱 인덱스(가용 시) — 백그라운드 빌드
        try:
            from .semantic_engine import build_index as _sem_build, is_available
            if is_available():
                _sem_build()
        except Exception as e:
            print(f"[startup] semantic index 빌드 스킵: {e}")

_threading.Thread(target=_startup, daemon=True).start()


# ── 알라딘 TTB API ───────────────────────────────────────────
_ALADIN_KEY = "ttbpopi07062229002"
_ALADIN_SEARCH_URL = "https://www.aladin.co.kr/ttb/api/ItemSearch.aspx"
_GOOGLE_BOOKS_URL  = "https://www.googleapis.com/books/v1/volumes"


async def _aladin_search(q: str, query_type: str, start: int = 1, max_results: int = 50) -> list[dict]:
    cb = "_x"
    params = {
        "ttbkey": _ALADIN_KEY, "Query": q, "QueryType": query_type,
        "MaxResults": max_results, "start": start, "SearchTarget": "Book",
        "output": "js", "Version": "20131101", "CallBack": cb,
    }
    try:
        async with httpx.AsyncClient(timeout=8.0) as client:
            r = await client.get(_ALADIN_SEARCH_URL, params=params)
        text = r.text.strip()
        if text.startswith(cb + "(") and text.endswith(")"):
            text = text[len(cb) + 1:-1]
        data = json.loads(text)
        return [{
            "title":     b.get("title", ""),
            "author":    b.get("author", ""),
            "publisher": b.get("publisher", ""),
            "isbn":      b.get("isbn13") or b.get("isbn") or "",
            "cover":     (b.get("cover") or "").replace("coversum", "cover200"),
            "link":      b.get("link", ""),
            "source":    "aladin",
        } for b in data.get("item", [])]
    except Exception as e:
        print(f"[book-search] aladin error: {e}")
        return []


async def _google_books_search(q: str, max_results: int = 40) -> list[dict]:
    try:
        async with httpx.AsyncClient(timeout=8.0) as client:
            r = await client.get(_GOOGLE_BOOKS_URL, params={
                "q": q, "langRestrict": "ko", "maxResults": min(max_results, 40),
            })
        items = r.json().get("items", [])
        return [{
            "title":     v.get("title", ""),
            "author":    ", ".join(v.get("authors", [])),
            "publisher": v.get("publisher", ""),
            "isbn":      next((x["identifier"] for x in v.get("industryIdentifiers", []) if x["type"] == "ISBN_13"), ""),
            "cover":     (v.get("imageLinks", {}).get("thumbnail") or "").replace("http://", "https://"),
            "link":      v.get("infoLink", ""),
            "source":    "google",
        } for i in items for v in [i.get("volumeInfo", {})]]
    except Exception as e:
        print(f"[book-search] google error: {e}")
        return []


# ── 국립중앙도서관 외부 API ──────────────────────────────────
API_KEY = os.getenv("NL_API_KEY")
SEARCH_URL = "https://www.nl.go.kr/NL/search/openApi/search.do"
SASEO_URL  = "https://www.nl.go.kr/NL/search/openApi/saseoApi.do"
NL_QA_VIEW_URL = "https://www.nl.go.kr/NL/contents/N30501000000.do?schM=view&ackRecKey={rec_key}"

# Claude 답변 본문에서 『도서명』을 추출해 도서 검색 API와 연동하기 위한 정규식
_BOOK_TITLE_RE = re.compile(r"『([^』]{1,60})』")


# ── KDC 분류 매핑 ───────────────────────────────────────────
KDC_MAP = {
    "0": {"name": "총류",   "color": "#6C757D",
          "keywords": ["도서관","백과사전","정보학","컴퓨터","프로그래밍","인공지능","데이터","소프트웨어","IT","딥러닝"]},
    "1": {"name": "철학",   "color": "#8B5CF6",
          "keywords": ["철학","윤리","논리","심리","심리학","인식론","형이상학","명상","마음","의식","행복"]},
    "2": {"name": "종교",   "color": "#F59E0B",
          "keywords": ["종교","불교","기독교","이슬람","성경","불경","신앙","신학","사찰","기도"]},
    "3": {"name": "사회과학","color": "#3B82F6",
          "keywords": ["사회","경제","정치","법","교육","경영","복지","행정","무역","통계","금융","부동산","토지","세금"]},
    "4": {"name": "자연과학","color": "#10B981",
          "keywords": ["과학","수학","물리","화학","생물","천문","지구","환경","우주","생태","자연"]},
    "5": {"name": "기술과학","color": "#EF4444",
          "keywords": ["기술","공학","의학","농업","건축","제조","전기","기계","의료","건강","요리","음식"]},
    "6": {"name": "예술",   "color": "#EC4899",
          "keywords": ["예술","음악","미술","영화","사진","디자인","스포츠","게임","그림","조각","춤","패션"]},
    "7": {"name": "언어",   "color": "#14B8A6",
          "keywords": ["언어","한국어","영어","일본어","중국어","문법","번역","어학","외국어"]},
    "8": {"name": "문학",   "color": "#F97316",
          "keywords": ["문학","소설","시","수필","희곡","동화","만화","웹툰","픽션","이야기","단편","장편"]},
    "9": {"name": "역사",   "color": "#84CC16",
          "keywords": ["역사","지리","한국사","세계사","전쟁","문화","문명","고고학","고대","근대","조선","일제"]},
}

DR_CODE_MAP = {
    "0": 5, "1": 6, "2": 6, "3": 5,
    "4": 4, "5": 4, "6": 6, "7": 6,
    "8": 11, "9": 6,
}

DR_CODE_NAME = {4: "자연과학", 5: "사회과학", 6: "인문과학", 11: "문학"}


def classify_keyword(keyword: str) -> Tuple[Optional[str], dict]:
    scores = {kdc: 0 for kdc in KDC_MAP}
    for kdc, info in KDC_MAP.items():
        for kw in info["keywords"]:
            if keyword == kw:
                scores[kdc] += 10
            elif kw in keyword:
                scores[kdc] += 3
            elif keyword in kw:
                scores[kdc] += 2
    best = max(scores, key=scores.get)
    if scores[best] == 0:
        return None, {"name": "미분류", "color": "#9CA3AF"}
    return best, KDC_MAP[best]


def strip_html(text: str) -> str:
    import html as _html
    text = _html.unescape(text or "")
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def parse_search_xml(xml_text: str, keyword: str) -> Tuple[list, int]:
    try:
        root = ET.fromstring(xml_text)
        total = int(root.findtext(".//total") or 0)
        items = []
        for item in root.findall(".//item"):
            title = item.findtext("title_info") or ""
            items.append({
                "id":          item.findtext("id"),
                "title":       title,
                "author":      item.findtext("author_info") or "-",
                "publisher":   item.findtext("pub_info") or "-",
                "year":        item.findtext("pub_year_info") or "-",
                "call_no":     item.findtext("call_no") or "-",
                "kdc_name":    item.findtext("kdc_name_1s") or "-",
                "kdc_code":    item.findtext("kdc_code_1s") or "",
                "type":        item.findtext("type_name") or "-",
                "detail_link": "https://www.nl.go.kr" + (item.findtext("detail_link") or ""),
            })
        return items, total
    except Exception:
        return [], 0


def parse_saseo_xml(xml_text: str) -> list:
    try:
        root = ET.fromstring(xml_text)
        items = []
        for item in root.findall(".//item"):
            image = item.findtext("mokchFilePath") or item.findtext("recomfilepath") or ""
            image = image.strip().replace("http://", "https://")
            content = strip_html(item.findtext("recomcontens") or "")
            items.append({
                "recom_no":  item.findtext("recomNo"),
                "title":     item.findtext("recomtitle") or "-",
                "author":    item.findtext("recomauthor") or "-",
                "publisher": item.findtext("recompublisher") or "-",
                "call_no":   item.findtext("recomcallno") or "-",
                "image":     image.strip(),
                "content":   content,
                "isbn":      item.findtext("recomisbn") or "",
                "category":  item.findtext("drCodeName") or "",
            })
        return items
    except Exception:
        return []


# ── 사서 Q&A 엔드포인트 (RAG) ───────────────────────────────
class AskRequest(BaseModel):
    query: str
    top_k: int = 8


async def _enrich_with_books(answer_text: str, max_books: int = 5) -> list[dict]:
    """Claude 답변에서 『…』로 표기된 도서명을 추출해 국중도 검색 API로 메타데이터 보강."""
    if not API_KEY or not answer_text:
        return []
    titles = []
    seen = set()
    for t in _BOOK_TITLE_RE.findall(answer_text):
        t = t.strip()
        if t and t not in seen:
            seen.add(t)
            titles.append(t)
        if len(titles) >= max_books:
            break
    if not titles:
        return []

    async with httpx.AsyncClient(timeout=8.0) as client:
        async def _one(title: str) -> Optional[dict]:
            try:
                r = await client.get(SEARCH_URL, params={
                    "key": API_KEY, "kwd": title,
                    "pageNum": 1, "pageSize": 1,
                    "type_name": "도서", "sort": "S",
                })
                items, _ = parse_search_xml(r.text, title)
                if items:
                    items[0]["matched_title"] = title
                    return items[0]
            except Exception:
                return None
            return None
        results = await asyncio.gather(*[_one(t) for t in titles])
    return [r for r in results if r]


@app.post("/api/librarian/ask")
async def librarian_ask(req: AskRequest):
    if not req.query.strip():
        raise HTTPException(status_code=400, detail="질문을 입력해주세요.")

    # 1) 하이브리드 검색 (동적 가중치, RRF 정규화)
    results = await asyncio.get_event_loop().run_in_executor(
        None, hybrid_search, req.query, req.top_k
    )

    # 2) Claude 사서 응답 생성 (RAG)
    chat = await asyncio.get_event_loop().run_in_executor(
        None, get_librarian_response, req.query, results
    )

    # 3) 응답 본문 『도서명』 → 국중도 도서검색 API 메타데이터 보강
    book_cards = await _enrich_with_books(chat["response"])

    vec_engine = results[0].get("vector_engine", "tfidf") if results else "tfidf"

    return {
        "query": req.query,
        "response": chat["response"],
        "used_claude": chat["used_claude"],
        "source_count": chat["source_count"],
        "cited_indices": chat.get("cited_indices", []),
        "response_mode": chat.get("response_mode", "rag"),
        "response_tier": chat.get("response_tier", "high"),
        "top_score": chat.get("top_score", 0.0),
        "norm_score": chat.get("norm_score", 0.0),
        "data4lib_count": chat.get("data4lib_count", 0),
        "weights": {
            "vector": results[0].get("vec_weight", 0.0) if results else 0.0,
            "keyword": results[0].get("kw_weight", 0.0) if results else 0.0,
        },
        "vector_engine": vec_engine,
        "sources": [{
            "rec_key": r.get("rec_key"),
            "question": r.get("question", "")[:150],
            "answer": r.get("answer", "")[:400],
            "subject": r.get("subject", ""),
            "answer_date": r.get("answer_date", ""),
            "answer_lib": r.get("answer_lib", ""),
            "search_type": r.get("search_type", ""),
            "score": round(r.get("combined_score", r.get("score", 0)), 4),
            "kw_rrf": round(r.get("kw_rrf", 0), 5),
            "vec_rrf": round(r.get("vec_rrf", 0), 5),
            "source_url": NL_QA_VIEW_URL.format(rec_key=r.get("rec_key", "")),
        } for r in results],
        "book_cards": book_cards,
    }


class FeedbackRequest(BaseModel):
    query: str
    response_tier: str
    top_score: float = 0.0
    norm_score: float = 0.0
    helpful: bool


@app.post("/api/librarian/feedback")
async def librarian_feedback(req: FeedbackRequest):
    """이용자 피드백 저장 — 임계값 자동 튜닝 데이터 수집용."""
    with _get_conn() as conn:
        conn.execute(
            "INSERT INTO feedback (query, response_tier, top_score, norm_score, helpful) "
            "VALUES (?, ?, ?, ?, ?)",
            (req.query[:500], req.response_tier, req.top_score, req.norm_score, int(req.helpful)),
        )
        conn.commit()
    return {"status": "ok"}


@app.post("/api/crawl/start")
async def crawl_start(force: bool = Query(False, description="True면 기존 답변까지 전수 재수집")):
    if crawl_state["running"]:
        return {"status": "already_running", **crawl_state}

    def _rebuild():
        invalidate_cache()
        build_index()
        try:
            from .semantic_engine import build_index as _sem_build, invalidate_cache as _sem_inv
            _sem_inv()
            _sem_build()
        except Exception as e:
            print(f"[crawl] semantic index 재빌드 스킵: {e}")

    asyncio.create_task(run_crawl(rebuild_index_fn=_rebuild, force=force))
    return {"status": "started", "force": force, **crawl_state}


@app.post("/api/presence/ping")
async def presence_ping(sid: str = Query(...)):
    now = _time.time()
    _presence[sid] = now
    cutoff = now - _PRESENCE_TTL
    stale = [k for k, v in _presence.items() if v < cutoff]
    for k in stale:
        del _presence[k]
    return {"online": len(_presence)}


@app.get("/api/presence/count")
async def presence_count():
    cutoff = _time.time() - _PRESENCE_TTL
    return {"online": sum(1 for v in _presence.values() if v >= cutoff)}


@app.get("/api/img-proxy")
async def img_proxy(url: str = Query(...)):
    """HTTP 이미지를 HTTPS 환경에서 사용하기 위한 프록시."""
    try:
        async with httpx.AsyncClient(timeout=8.0, follow_redirects=True) as client:
            r = await client.get(url)
        ct = r.headers.get("content-type", "image/jpeg")
        return Response(content=r.content, media_type=ct)
    except Exception:
        raise HTTPException(status_code=404, detail="image not found")


@app.get("/api/crawl/status")
async def crawl_status():
    return {"db_count": count_items(), **crawl_state}


@app.get("/api/librarian/stats")
async def librarian_stats():
    return {
        "db_count": count_items(),
        "crawl_stage": crawl_state["stage"],
        "crawl_running": crawl_state["running"],
    }


# ── 도서 분류 + 검색 결과 엔드포인트 ─────────────────────────
@app.get("/api/analyze")
async def analyze(
    keyword: str = Query(..., description="검색 키워드"),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=5, le=50),
):
    if not API_KEY:
        raise HTTPException(status_code=500, detail="API 키가 설정되지 않았습니다.")

    kdc_code, kdc_info = classify_keyword(keyword)
    dr_code = DR_CODE_MAP.get(kdc_code, 11) if kdc_code else 11

    async with httpx.AsyncClient(timeout=15.0) as client:
        search_resp = await client.get(SEARCH_URL, params={
            "key":       API_KEY,
            "kwd":       keyword,
            "pageNum":   page,
            "pageSize":  page_size,
            "type_name": "도서",
            "sort":      "S",
        })

    search_books, total = parse_search_xml(search_resp.text, keyword)

    return {
        "keyword": keyword,
        "kdc": {
            "code":    kdc_code,
            "name":    kdc_info.get("name", "미분류"),
            "color":   kdc_info.get("color", "#9CA3AF"),
        },
        "pagination": {
            "page":        page,
            "page_size":   page_size,
            "total":       total,
            "total_pages": (total + page_size - 1) // page_size if total else 0,
        },
        "search_results": search_books,
    }


# 도서 검색 전용 추가 노이즈어 (자연어 요청 문장에서 자주 나오는 동사/형용사)
_BOOK_QUERY_NOISE = {
    "읽기", "읽으면", "읽는", "읽어도", "읽어요",
    "좋은", "좋아", "좋겠어", "좋아요",
    "싶을", "싶어", "싶은", "싶습니다",
    "찾고", "찾는", "찾아",
    "키우고", "키우는", "키우기",
    "이해할", "이해하는", "이해하기",
    "죽고", "만큼", "정도",
    "쉽게", "깊게", "많이",
}

# 영문+한글 혼합 단어 끝의 한글 조사 제거용 (예: INFP에게 → INFP)
_KO_PARTICLE_RE = re.compile(
    r"(에게서|으로부터|에서부터|에게|에서|으로|에는|에도|까지|부터|처럼|만큼|보다|이나|이라|라도|의|을|를|은|는|이|가|도|로|에|와|과)$"
)

# MBTI 16가지 유형 코드 — 알라딘에 개별 유형명으로 된 책이 거의 없으므로 "MBTI"로 통합
_MBTI_TYPES = {
    "INTJ", "INTP", "ENTJ", "ENTP",
    "INFJ", "INFP", "ENFJ", "ENFP",
    "ISTJ", "ISFJ", "ESTJ", "ESFJ",
    "ISTP", "ISFP", "ESTP", "ESFP",
}


def _extract_book_keywords(query: str) -> str:
    """자연어 쿼리에서 도서 검색용 핵심 키워드 추출.

    '힘들때 위로가 되는 책 추천해줘' → '힘들 위로'
    '혼자 여행할 때 읽기 좋은 책' → '혼자 여행'
    'MBTI INFP에게 추천하는 소설' → 'MBTI 소설'
    2단어 이하 짧은 쿼리는 그대로 반환.
    """
    if len(query.split()) <= 2:
        return query
    normalized = _normalize_ko_query(query)
    noise = _KW_STOPWORDS | _BOOK_QUERY_NOISE
    keywords = []
    has_mbti_type = False
    for w in normalized.split():
        # 영문+한글 혼합 단어의 한글 조사 제거 (INFP에게 → INFP)
        if re.search(r"[A-Za-z]", w):
            w = _KO_PARTICLE_RE.sub("", w)
        if w.upper() in _MBTI_TYPES:
            has_mbti_type = True
            continue  # 유형 코드는 제거하고 MBTI 키워드로 통합
        if len(w) >= 2 and w not in noise:
            keywords.append(w)
    # MBTI 유형 코드가 있었으면 "MBTI" 키워드를 맨 앞에 추가
    if has_mbti_type and "MBTI" not in [k.upper() for k in keywords]:
        keywords.insert(0, "MBTI")
    return " ".join(keywords) if keywords else query


# ── 도서 검색 프록시 (알라딘 + Google Books) ─────────────────
@app.get("/api/book-search")
async def book_search_proxy(
    q: str = Query(..., description="검색어"),
    filter_type: str = Query("all", description="all|title|author|publisher"),
    max_results: int = Query(30, ge=1, le=100),
):
    qt_map = {"title": "Title", "author": "Author", "publisher": "Publisher"}
    qt = qt_map.get(filter_type, "Keyword")

    if filter_type in qt_map:
        effective_q = q
        aladin_calls = [_aladin_search(effective_q, qt, 1, 50)]
        google_q = {"title": f"intitle:{q}", "author": f"inauthor:{q}", "publisher": f"inpublisher:{q}"}[filter_type]
    else:
        effective_q = _extract_book_keywords(q)
        aladin_calls = [
            _aladin_search(effective_q, "Title",   1,  50),
            _aladin_search(effective_q, "Title",  51,  50),
            _aladin_search(effective_q, "Keyword", 1,  50),
            _aladin_search(effective_q, "Keyword", 51, 50),
        ]
        google_q = effective_q

    results = await asyncio.gather(*aladin_calls, _google_books_search(google_q))
    seen, books = set(), []
    for b in [item for sub in results for item in sub]:
        key = b["isbn"] or (b["title"] + b["author"])
        if key not in seen:
            seen.add(key)
            books.append(b)

    return {"books": books[:max_results]}


# 상위 디렉터리(mbtibooktalk 루트)를 정적으로 서빙
_root = os.path.join(os.path.dirname(__file__), "..")
app.mount("/", StaticFiles(directory=_root, html=True), name="static")
