"""정보나루(data4library.kr) OpenAPI 연동 모듈.

대출 인기 도서 검색 결과를 RAG 컨텍스트로 제공하여
사서 답변의 신뢰도를 높인다.

ENV
---
DATA4LIB_API_KEY : 정보나루 OpenAPI 인증키
"""

import os
import httpx
from datetime import datetime, timedelta

API_KEY  = os.getenv("DATA4LIB_API_KEY", "")
BASE_URL = "https://data4library.kr/api"

# 최근 N개월 대출 데이터 기준
_MONTHS_BACK = 12

# 도서관 공통어 — 정보나루 키워드 검색 시 제외
_STOPWORDS = {
    "책", "도서", "추천", "관련", "알려", "어떤", "좋은", "있는", "없는",
    "되는", "하는", "해요", "해서", "같은", "위한", "대한", "읽고", "읽을",
    "볼", "줘요", "주세요", "합니다", "드립니다", "때", "수", "것", "제",
}


def _date_range() -> tuple[str, str]:
    end   = datetime.today()
    start = end - timedelta(days=_MONTHS_BACK * 30)
    return start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d")


def _extract_keywords(query: str, max_words: int = 3) -> str:
    """질의에서 의미 있는 단어만 추출하여 검색 키워드로 반환."""
    words = [w for w in query.split() if len(w) >= 2 and w not in _STOPWORDS]
    return " ".join(words[:max_words]) if words else query[:20]


def search_books(query: str, top_k: int = 5) -> list[dict]:
    """정보나루 대출 도서 검색 API 호출.

    활성화 전·오류 시 빈 리스트 반환(정상 폴백).
    """
    if not API_KEY:
        return []

    keyword = _extract_keywords(query)
    if not keyword:
        return []

    start_dt, end_dt = _date_range()
    params = {
        "authKey":  API_KEY,
        "keyword":  keyword,
        "startDt":  start_dt,
        "endDt":    end_dt,
        "pageSize": top_k * 2,
        "format":   "json",
    }

    try:
        resp = httpx.get(f"{BASE_URL}/loanItemSrch", params=params, timeout=5.0)
        resp.raise_for_status()
        data = resp.json()

        # API 활성화 전·오류 응답 처리
        if "error" in data.get("response", {}):
            return []

        docs = data.get("response", {}).get("docs", [])
        books = []
        for item in docs:
            doc = item.get("doc", {})
            title = doc.get("bookname", "").strip()
            if not title:
                continue
            books.append({
                "title":       title,
                "authors":     doc.get("authors", ""),
                "publisher":   doc.get("publisher", ""),
                "pub_year":    doc.get("publication_year", ""),
                "isbn13":      doc.get("isbn13", ""),
                "class_nm":    doc.get("class_nm", ""),
                "loan_count":  int(doc.get("loan_count", 0) or 0),
                "book_url":    doc.get("bookDtlUrl", ""),
                "source":      "data4library",
            })

        # 대출 횟수 많은 순 정렬
        books.sort(key=lambda x: x["loan_count"], reverse=True)
        return books[:top_k]

    except Exception as e:
        print(f"[data4lib] 검색 실패 (무시): {e}")
        return []


def format_for_rag(books: list[dict]) -> str:
    """검색 결과를 RAG 컨텍스트 문자열로 변환."""
    if not books:
        return ""
    lines = ["[정보나루 실제 대출 데이터 기반 추천 도서]"]
    for i, b in enumerate(books, 1):
        line = (
            f"{i}. 『{b['title']}』"
            f" / {b['authors'] or '저자 미상'}"
            f" / {b['publisher'] or '-'}"
            f" ({b['pub_year'] or '-'})"
            f" — 분류: {b['class_nm'] or '-'}"
            f", 대출 {b['loan_count']}회"
        )
        lines.append(line)
    lines.append("※ 위 목록은 정보나루 도서관 실제 대출 통계 기반입니다.")
    return "\n".join(lines)
