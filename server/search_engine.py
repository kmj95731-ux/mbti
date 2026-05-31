"""Hybrid keyword + vector search over the NL Q&A database.

벡터 검색은 시맨틱 임베딩(가용 시) → TF-IDF 자동 폴백 구조이며,
키워드 검색은 SQLite FTS5 BM25 기반이다.
최종 융합은 RRF(Reciprocal Rank Fusion)로 처리하여 두 점수의 스케일 차이를 흡수한다.

TF-IDF 벡터라이저: word-level(1,2-gram) 사용.
char_wb 방식은 한국어 공통 형태소("도서","관련","때" 등)가 5,000건 이상 코퍼스에서
무관한 문서와 spurious cosine similarity를 발생시키므로 교체함.
"""

import os
import pickle
import re
from pathlib import Path
from typing import Optional

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .database import get_conn, get_items_for_index

# ── 한국어 쿼리 정규화 ──────────────────────────────────────
# word-level TF-IDF는 활용형("우울할","위로가")을 기본형("우울","위로")과
# 다른 토큰으로 취급하여 매칭 실패 → 어미·조사를 제거해 기본형에 근접시킴
_KO_ENDINGS = sorted([
    # 동사 어미
    "하는", "하다", "해요", "해서", "했어요", "했", "하고", "한다", "한", "함",
    "하면", "하며", "하기", "하게", "하나요", "하나", "합니다", "해줘", "해줘요",
    "되는", "됩니다", "됐", "되어", "되고", "되면", "되어서",
    "있는", "없는", "있어요", "없어요",
    "이에요", "예요", "입니다", "이야",
    # 조사 (긴 것 먼저)
    "으로부터", "에게서", "에서부터",
    "으로", "에서", "에게", "부터", "까지", "처럼", "만큼", "보다", "에는",
    "가", "이", "을", "를", "은", "는", "도", "로", "에", "의", "와", "과",
    "할", "적", "인",
], key=len, reverse=True)

_HANGUL_RE = re.compile(r"^[가-힣]+$")


def _normalize_ko_query(query: str) -> str:
    """한국어 어미·조사를 제거하여 기본형에 가깝게 정규화.

    '우울할 때 위로가 되는 책' → '우울 때 위로 되는 책'
    이후 _KW_STOPWORDS 필터를 거치면 '우울 위로'만 남아 정확한 매칭.
    """
    result = []
    for word in query.split():
        if not _HANGUL_RE.match(word):
            result.append(word)
            continue
        norm = word
        for ending in _KO_ENDINGS:
            if norm.endswith(ending) and len(norm) - len(ending) >= 2:
                norm = norm[: -len(ending)]
                break
        result.append(norm)
    normalized = " ".join(result)
    return normalized if normalized.strip() else query

_vectorizer: Optional[TfidfVectorizer] = None
_matrix = None      # sparse matrix
_ids: list[int] = []
_rec_keys: list[str] = []

CACHE_PATH = Path(__file__).parent / "tfidf_cache.pkl"

RRF_K = int(os.getenv("RRF_K", "60"))

# TF-IDF 최소 코사인 유사도 임계값 (기존 0.01 → 0.05 로 상향)
VECTOR_MIN_SCORE = float(os.getenv("VECTOR_MIN_SCORE", "0.05"))


def build_index() -> None:
    """Build (or rebuild) the TF-IDF matrix from all items in the DB."""
    global _vectorizer, _matrix, _ids, _rec_keys

    rows = get_items_for_index()
    if not rows:
        return

    _ids = [r["id"] for r in rows]
    _rec_keys = [r["rec_key"] for r in rows]
    texts = [f"{r['question']} {r['answer']}" for r in rows]

    # word-level(1,2-gram): 의미 단위 매칭 → 의미상 무관한 문서와의
    # spurious cosine similarity 억제 (char_wb 대비 정확도 개선)
    _vectorizer = TfidfVectorizer(
        analyzer="word",
        ngram_range=(1, 2),
        max_features=80_000,
        sublinear_tf=True,
        min_df=1,
        token_pattern=r"(?u)\b\w+\b",
    )
    _matrix = _vectorizer.fit_transform(texts)

    with open(CACHE_PATH, "wb") as f:
        pickle.dump({
            "vectorizer": _vectorizer,
            "matrix": _matrix,
            "ids": _ids,
            "rec_keys": _rec_keys,
            "count": len(rows),
        }, f)


def _ensure_index() -> bool:
    global _vectorizer, _matrix, _ids, _rec_keys
    if _vectorizer is not None:
        return True
    if CACHE_PATH.exists():
        try:
            with open(CACHE_PATH, "rb") as f:
                cached = pickle.load(f)
            _vectorizer = cached["vectorizer"]
            _matrix = cached["matrix"]
            _ids = cached["ids"]
            _rec_keys = cached.get("rec_keys", [])
            return True
        except Exception:
            pass
    return False


def _fetch_rows_by_ids(ids: list[int]) -> dict:
    if not ids:
        return {}
    placeholders = ",".join("?" * len(ids))
    with get_conn() as conn:
        rows = conn.execute(
            f"SELECT id, rec_key, question, answer, subject, answer_date, answer_lib "
            f"FROM qa_items WHERE id IN ({placeholders})",
            ids,
        ).fetchall()
    return {r["id"]: dict(r) for r in rows}


def vector_search(query: str, top_k: int = 10) -> list[dict]:
    """TF-IDF 벡터 검색(폴백용).

    어미·조사 제거 후 기본형으로 정규화한 쿼리를 사용하여
    '우울할' → '우울' 등 활용형도 올바르게 매칭.
    """
    if not _ensure_index():
        return []
    normalized = _normalize_ko_query(query)
    # 원본과 정규화 결합: 두 쪽 모두 고려
    combined = f"{query} {normalized}" if normalized != query else query
    q_vec = _vectorizer.transform([combined])
    scores = cosine_similarity(q_vec, _matrix).flatten()
    top_idx = np.argsort(scores)[::-1][:top_k * 2]
    top_idx = [i for i in top_idx if scores[i] >= VECTOR_MIN_SCORE][:top_k]
    id_list = [_ids[i] for i in top_idx]
    rows = _fetch_rows_by_ids(id_list)
    results = []
    for idx in top_idx:
        row = rows.get(_ids[idx])
        if row:
            results.append({**row, "score": float(scores[idx]), "search_type": "vector"})
    return results


# 도서관 Q&A 전체에 너무 자주 나타나 단독 폴백 검색어로 쓰면 잡음이 되는 단어
_KW_STOPWORDS = {
    # 도서관 공통어
    "책", "도서", "추천", "관련", "알려", "어떤", "좋은", "있는", "없는",
    "되는", "하는", "해요", "해서", "같은", "위한", "대한", "있어요", "싶어요",
    "읽고", "읽을", "읽어", "볼", "봐요", "줘요", "주세요", "드립니다", "합니다",
    # 한국어 범용 시간·상황어 — 거의 모든 문서에 등장하여 잡음 유발
    "때", "후", "전", "중", "시", "경우", "상황", "다음", "이후", "이전",
    # 일반 동사·형용사 어간
    "하고", "하여", "하면", "이런", "저런", "그런", "이런", "많은", "다양한",
}


def keyword_search(query: str, top_k: int = 10) -> list[dict]:
    """SQLite FTS5 BM25 키워드 검색."""
    SQL = """
        SELECT q.id, q.rec_key, q.question, q.answer, q.subject,
               q.answer_date, q.answer_lib, bm25(qa_fts) AS score
        FROM qa_fts
        JOIN qa_items q ON qa_fts.rowid = q.id
        WHERE qa_fts MATCH ?
        ORDER BY score
        LIMIT ?
    """
    def _run(term):
        try:
            with get_conn() as conn:
                return conn.execute(SQL, (term, top_k)).fetchall()
        except Exception:
            return []

    rows = _run(query.replace('"', '""'))
    if not rows:
        # 2차: 정규화 쿼리로 재시도 ("우울할 위로가" → "우울 위로")
        normalized = _normalize_ko_query(query)
        if normalized != query:
            rows = _run(normalized.replace('"', '""'))
    if not rows:
        # 3차: 정규화된 의미어 단어별 개별 검색
        # 도서관 공통어("책","도서","추천" 등) 제외 → 엉뚱한 문서 매칭 방지
        normalized = _normalize_ko_query(query)
        words = [
            w for w in normalized.split()
            if len(w) >= 2 and w not in _KW_STOPWORDS
        ]
        seen, rows = set(), []
        for word in words[:5]:
            for r in _run(word):
                if r["id"] not in seen:
                    seen.add(r["id"])
                    rows.append(r)
        rows = rows[:top_k]

    return [{**dict(r), "score": abs(float(r["score"])), "search_type": "keyword"}
            for r in rows]


def _rrf_scores(ranked_keys: list[str], k: int = RRF_K) -> dict:
    """Reciprocal Rank Fusion: 1 / (k + rank) 점수 산출."""
    return {key: 1.0 / (k + rank + 1) for rank, key in enumerate(ranked_keys)}


def _vector_pipeline(query: str, top_k: int) -> tuple:
    """시맨틱 임베딩 가용 시 우선 사용, 아니면 TF-IDF로 폴백."""
    try:
        from . import semantic_engine
        if semantic_engine.is_available():
            sem = semantic_engine.semantic_search(query, top_k * 2)
            if sem:
                return sem, "semantic"
    except Exception as e:
        print(f"[hybrid] 시맨틱 검색 호출 실패 → TF-IDF 폴백: {e}")
    return vector_search(query, top_k * 2), "tfidf"


def _dynamic_weights(query: str, vec_engine: str) -> tuple[float, float]:
    """쿼리 길이 + 벡터 엔진 종류에 따라 가중치 동적 결정.

    시맨틱 모델 정상:  단어형(≤2) 0.40:0.60 / 중간(3-4) 0.55:0.45 / 자연어(5+) 0.70:0.30
    TF-IDF 폴백:       단어형(≤2) 0.30:0.70 / 중간(3-4) 0.40:0.60 / 자연어(5+) 0.50:0.50
    """
    words = len(query.split())
    if vec_engine == "semantic":
        if words <= 2:
            return 0.40, 0.60
        elif words <= 4:
            return 0.55, 0.45
        else:
            return 0.70, 0.30
    else:  # tfidf fallback
        if words <= 2:
            return 0.30, 0.70
        elif words <= 4:
            return 0.40, 0.60
        else:
            return 0.50, 0.50


def hybrid_search(query: str, top_k: int = 8) -> list[dict]:
    """벡터(시맨틱·TF-IDF 자동선택) + 키워드 하이브리드 검색.

    - 두 검색 결과를 RRF로 정규화하여 스케일 차이 제거
    - 최종 점수 = VECTOR_WEIGHT × vec_rrf + KEYWORD_WEIGHT × kw_rrf
    """
    kw_list = keyword_search(query, top_k * 2)
    vec_list, vec_engine = _vector_pipeline(query, top_k)
    v_w, k_w = _dynamic_weights(query, vec_engine)

    kw = {r["rec_key"]: r for r in kw_list}
    vec = {r["rec_key"]: r for r in vec_list}

    all_keys = set(kw) | set(vec)
    if not all_keys:
        return []

    kw_rrf = _rrf_scores([r["rec_key"] for r in kw_list])
    vec_rrf = _rrf_scores([r["rec_key"] for r in vec_list])

    merged = []
    for key in all_keys:
        base = vec.get(key) or kw.get(key)
        kw_s = kw_rrf.get(key, 0.0)
        vec_s = vec_rrf.get(key, 0.0)
        combined = v_w * vec_s + k_w * kw_s
        if key in kw and key in vec:
            stype = "hybrid"
        else:
            stype = base.get("search_type", "")
        merged.append({
            **base,
            "combined_score": combined,
            "kw_rrf": kw_s,
            "vec_rrf": vec_s,
            "search_type": stype,
            "vector_engine": vec_engine,
            "vec_weight": v_w,
            "kw_weight": k_w,
        })


    merged.sort(key=lambda x: x["combined_score"], reverse=True)
    merged = merged[:top_k]

    # min-max 정규화 + Top1-Top2 margin 계산
    if merged:
        scores = [r["combined_score"] for r in merged]
        s_min, s_max = min(scores), max(scores)
        eps = 1e-6
        for r in merged:
            r["norm_score"] = (r["combined_score"] - s_min) / (s_max - s_min + eps)
        merged[0]["margin"] = (scores[0] - scores[1]) if len(scores) >= 2 else scores[0]

    return merged


def invalidate_cache() -> None:
    """TF-IDF 인덱스 캐시 무효화."""
    global _vectorizer, _matrix, _ids, _rec_keys
    _vectorizer = _matrix = None
    _ids = []
    _rec_keys = []
    if CACHE_PATH.exists():
        CACHE_PATH.unlink()
