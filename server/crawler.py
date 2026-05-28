import asyncio
import re
import html
from typing import Optional

import httpx
from bs4 import BeautifulSoup

BASE_URL = "https://www.nl.go.kr/NL/contents/N30501000000.do"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    "Referer": BASE_URL,
}

# Global crawl state (single-process server)
crawl_state = {
    "running": False,
    "total": 0,
    "done": 0,
    "errors": 0,
    "stage": "idle",  # idle | listing | detail | indexing | complete
    "message": "",
}


def _clean_html(raw: str) -> str:
    """Strip HTML tags and decode entities to plain text."""
    raw = html.unescape(raw)
    soup = BeautifulSoup(raw, "html.parser")
    for tag in soup.find_all(["br", "p", "div", "li"]):
        tag.insert_after("\n")
    text = soup.get_text(separator="")
    # Collapse whitespace while preserving paragraph breaks
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


async def _fetch_list_page(client: httpx.AsyncClient, page: int) -> list[dict]:
    """Fetch one list page, return list of {rec_key, subject, title}."""
    resp = await client.post(
        BASE_URL,
        data={"page": str(page), "viewCount": "100", "schStr": "", "schFld": "0"},
        headers=HEADERS,
        timeout=30.0,
    )
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    items = []
    for row in soup.find_all("tr"):
        link = row.find("a", href=re.compile(r"fn_goView"))
        if not link:
            continue
        m = re.search(r"fn_goView\('([^']+)'\)", link.get("href", ""))
        if not m:
            continue
        rec_key = m.group(1)
        tds = row.find_all("td")
        subject = tds[1].get_text(strip=True) if len(tds) >= 2 else ""
        title = link.get_text(strip=True)
        items.append({"rec_key": rec_key, "subject": subject, "title": title})

    return items


async def _fetch_detail(client: httpx.AsyncClient, rec_key: str, subject: str) -> Optional[dict]:
    """Fetch detail page, return full Q&A dict or None on failure."""
    url = f"{BASE_URL}?schM=view&ackRecKey={rec_key}"
    try:
        resp = await client.get(url, headers=HEADERS, timeout=30.0)
        resp.raise_for_status()
    except Exception:
        return None

    soup = BeautifulSoup(resp.text, "html.parser")

    q_el = soup.find(class_="question_cont")
    question = q_el.get_text(strip=True) if q_el else ""

    a_el = soup.find(class_="answer_cont")
    answer = _clean_html(str(a_el)) if a_el else ""

    reg_date = answer_date = answer_lib = ""
    info_els = soup.find_all(class_="info_inner")
    for info in info_els:
        dts = info.find_all("dt")
        dds = info.find_all("dd")
        for dt, dd in zip(dts, dds):
            label = dt.get_text(strip=True)
            val = dd.get_text(strip=True)
            if "등록일" in label:
                reg_date = val
            elif "답변일" in label:
                answer_date = val
            elif "답변도서관" in label:
                answer_lib = val

    return {
        "rec_key": rec_key,
        "question": question,
        "answer": answer,
        "subject": subject,
        "reg_date": reg_date,
        "answer_date": answer_date,
        "answer_lib": answer_lib,
    }


async def run_crawl(rebuild_index_fn=None, force: bool = False,
                    max_pages: int = 200) -> None:
    """전수/증분 크롤. force=True 인 경우 기존 rec_key도 재수집.

    Parameters
    ----------
    rebuild_index_fn : callable | None
        수집 완료 후 호출할 인덱스 재빌드 함수
    force : bool
        True면 기존 항목도 전수 재수집(답변 갱신분 반영)
    max_pages : int
        목록 페이지 순회 안전 한도(무한 루프 방지)
    """
    from .database import upsert_item, get_known_keys

    crawl_state.update({"running": True, "done": 0, "errors": 0,
                        "stage": "listing",
                        "message": ("전수 재수집 시작..." if force else "신규 수집 시작...")})

    known = get_known_keys() if not force else set()
    all_items: list[dict] = []
    empty_streak = 0  # 연속 빈 응답 카운터

    async with httpx.AsyncClient() as client:
        # Step 1: collect all rec_keys from list pages
        for page in range(1, max_pages + 1):
            try:
                page_items = await _fetch_list_page(client, page)
            except Exception as e:
                crawl_state["errors"] += 1
                crawl_state["message"] = f"목록 오류 (page {page}): {e}"
                break
            if not page_items:
                empty_streak += 1
                if empty_streak >= 2:
                    break
                continue
            empty_streak = 0
            all_items.extend(page_items)
            crawl_state["message"] = f"목록 수집 중... {len(all_items)}건 (page {page})"
            await asyncio.sleep(0.3)

        # Step 2: fetch details (force 시 전수, 아니면 신규만)
        target_items = all_items if force else [i for i in all_items if i["rec_key"] not in known]
        crawl_state.update({
            "total": len(target_items),
            "stage": "detail",
            "message": f"{'전수' if force else '신규'} {len(target_items)}건 상세 수집 시작",
        })
        new_items = target_items

        CONCURRENCY = 5
        sem = asyncio.Semaphore(CONCURRENCY)

        async def fetch_and_save(item: dict) -> None:
            async with sem:
                detail = await _fetch_detail(client, item["rec_key"], item["subject"])
                if detail and (detail["question"] or detail["answer"]):
                    upsert_item(**detail)
                    crawl_state["done"] += 1
                else:
                    crawl_state["errors"] += 1
                crawl_state["message"] = (
                    f"상세 수집 중... {crawl_state['done']}/{crawl_state['total']}건"
                )
                await asyncio.sleep(0.2)

        await asyncio.gather(*[fetch_and_save(i) for i in new_items])

    # Step 3: rebuild vector index
    crawl_state["stage"] = "indexing"
    crawl_state["message"] = "벡터 인덱스 빌드 중..."
    if rebuild_index_fn:
        await asyncio.get_event_loop().run_in_executor(None, rebuild_index_fn)

    crawl_state.update({"running": False, "stage": "complete",
                        "message": f"완료: {crawl_state['done']}건 수집"})
