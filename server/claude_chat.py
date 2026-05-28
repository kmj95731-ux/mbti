"""사서 응답 생성 모듈 — 국립중앙도서관 Q&A DB + 정보나루 대출 데이터 기반.

Claude API 없이 동작하며, 검색 결과와 정보나루 도서 데이터를 조합해 응답을 구성한다.
"""

import os

from .data4lib import search_books

# 환경변수 (임계값 조정 가능)
RAG_SCORE_HIGH = float(os.getenv("RAG_SCORE_HIGH", "0.020"))
RAG_SCORE_MID  = float(os.getenv("RAG_SCORE_MID",  "0.013"))
RAG_MARGIN_MIN = float(os.getenv("RAG_MARGIN_MIN", "0.05"))
RAG_NORMALIZE  = os.getenv("RAG_NORMALIZE", "1") == "1"

_legacy = os.getenv("MIN_RAG_SCORE")
if _legacy:
    RAG_SCORE_MID = float(_legacy)

CONTEXT_TOP_N = 8


def _classify_tier(results: list[dict]) -> str:
    if not results:
        return "low"
    top = results[0]
    raw = float(top.get("combined_score", top.get("score", 0.0)))

    if RAG_NORMALIZE and "norm_score" in top:
        norm   = float(top.get("norm_score", 0.0))
        margin = float(top.get("margin", 0.0))
        if norm >= 0.6 and margin >= RAG_MARGIN_MIN:
            return "high"
        elif norm >= 0.3:
            return "mid"
        else:
            return "low"

    if raw >= RAG_SCORE_HIGH:
        return "high"
    elif raw >= RAG_SCORE_MID:
        return "mid"
    else:
        return "low"


def _build_response(
    user_query: str,
    results: list[dict],
    d4l_books: list[dict],
    tier: str,
) -> str:
    lines = []

    if tier == "high":
        top = results[0]
        ans_lib  = top.get("answer_lib", "국립중앙도서관")
        ans_date = top.get("answer_date", "")
        answer   = (top.get("answer") or "").strip()

        lines.append(f"안녕하세요. 「{user_query}」에 대해 안내해 드립니다.\n")
        lines.append(answer)
        if ans_lib or ans_date:
            meta = " | ".join(filter(None, [ans_lib, ans_date]))
            lines.append(f"\n※ 출처: 국립중앙도서관 「사서에게 물어보세요」 ({meta})")

        if len(results) > 1:
            lines.append("\n\n📋 관련 추가 Q&A")
            for r in results[1:4]:
                q = (r.get("question") or "").strip().replace("\n", " ")[:100]
                a = (r.get("answer") or "").strip().replace("\n", " ")[:200]
                lines.append(f"• {q}\n  → {a}…")

    elif tier == "mid":
        lines.append(f"※ 참고 자료를 기반으로 보완 답변드립니다.\n")
        lines.append(f"「{user_query}」와 관련하여 아래 자료를 안내해 드립니다.\n")

        for i, r in enumerate(results[:3], 1):
            q       = (r.get("question") or "").strip().replace("\n", " ")[:120]
            a       = (r.get("answer") or "").strip().replace("\n", " ")[:350]
            ans_lib = r.get("answer_lib", "")
            lines.append(f"[{i}] {q}")
            lines.append(f"   → {a}…")
            if ans_lib:
                lines.append(f"   (답변: {ans_lib})")
            lines.append("")

        lines.append(
            "더 정확한 정보는 국립중앙도서관 「사서에게 물어보세요」 서비스를 이용해 주세요.\n"
            "→ https://www.nl.go.kr/ask/"
        )

    else:  # low
        lines.append(
            "※ 본 답변은 국립중앙도서관 Q&A DB에 직접 매칭되는 자료가 없어, "
            "정보나루 대출 통계 데이터를 기반으로 안내드립니다.\n"
        )
        if not d4l_books:
            lines.append(
                f"「{user_query}」에 대한 자세한 안내가 필요하시면, "
                "국립중앙도서관 「사서에게 물어보세요」 서비스를 이용해 주세요.\n"
                "→ https://www.nl.go.kr/ask/"
            )

    # 정보나루 추천 도서 섹션 (tier 무관 공통)
    if d4l_books:
        lines.append("\n\n📚 정보나루 실제 대출 통계 기반 추천 도서")
        for i, b in enumerate(d4l_books, 1):
            title   = b.get("title", "")
            authors = b.get("authors", "저자 미상")
            pub     = b.get("publisher", "")
            year    = b.get("pub_year", "")
            cls_nm  = b.get("class_nm", "")
            loans   = b.get("loan_count", 0)
            pub_info = f"{pub}" + (f", {year}" if year else "")
            lines.append(
                f"{i}. 『{title}』 / {authors}"
                + (f" / {pub_info}" if pub_info.strip(",") else "")
                + (f" — {cls_nm}" if cls_nm else "")
                + f" (대출 {loans}회)"
            )
        lines.append("※ 위 목록은 정보나루 도서관 실제 대출 통계 기반입니다.")

    return "\n".join(lines).strip()


def get_librarian_response(user_query: str, search_results: list[dict]) -> dict:
    tier = _classify_tier(search_results)
    top  = search_results[0] if search_results else {}
    top_score  = float(top.get("combined_score", top.get("score", 0.0)))
    norm_score = float(top.get("norm_score", 0.0))

    d4l_books = search_books(user_query)
    response  = _build_response(user_query, search_results, d4l_books, tier)

    return {
        "response":      response,
        "used_claude":   False,
        "source_count":  len(search_results),
        "cited_indices": [],
        "response_mode": "general" if tier == "low" else "rag",
        "response_tier": tier,
        "top_score":     round(top_score, 5),
        "norm_score":    round(norm_score, 5),
        "data4lib_count": len(d4l_books),
    }
