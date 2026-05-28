import sqlite3
import json
import re
from pathlib import Path

DB_PATH    = Path(__file__).parent / "nl_qa.db"
SEED_DIR   = Path(__file__).parent


def get_conn() -> sqlite3.Connection:
    # timeout 상향 + WAL 모드로 다중 접속자 환경 동시성 보강
    conn = sqlite3.connect(DB_PATH, timeout=30.0, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    try:
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA synchronous=NORMAL")
        conn.execute("PRAGMA busy_timeout=30000")
    except Exception:
        pass
    return conn


# 답변 본문에서 ISBN(10/13자리) 및 청구기호 패턴 추출용 정규식
_ISBN_RE = re.compile(r"(?<!\d)(97[89][\-\s]?\d{1,5}[\-\s]?\d{1,7}[\-\s]?\d{1,7}[\-\s]?\d|\d{10}|\d{9}X)(?!\d)")
_CALLNO_RE = re.compile(r"\b\d{3}(?:\.\d{1,4})?\s?[가-힣A-Za-z]\d{1,5}(?:[가-힣A-Za-z])?\b")


def extract_metadata(answer_text: str) -> dict:
    """답변 본문에서 ISBN·청구기호를 추출하여 dict로 반환."""
    if not answer_text:
        return {"isbns": [], "call_numbers": []}
    isbns = list({m.replace(" ", "").replace("-", "") for m in _ISBN_RE.findall(answer_text)})
    callnos = list({m.strip() for m in _CALLNO_RE.findall(answer_text)})
    return {"isbns": isbns[:10], "call_numbers": callnos[:10]}


def init_db() -> None:
    with get_conn() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS qa_items (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            rec_key     TEXT    UNIQUE NOT NULL,
            question    TEXT    NOT NULL DEFAULT '',
            answer      TEXT    NOT NULL DEFAULT '',
            subject     TEXT    DEFAULT '',
            reg_date    TEXT    DEFAULT '',
            answer_date TEXT    DEFAULT '',
            answer_lib  TEXT    DEFAULT '',
            isbns       TEXT    DEFAULT '',
            call_numbers TEXT   DEFAULT '',
            updated_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""")
        # 기존 DB 호환: 컬럼이 없으면 추가
        for ddl in (
            "ALTER TABLE qa_items ADD COLUMN isbns TEXT DEFAULT ''",
            "ALTER TABLE qa_items ADD COLUMN call_numbers TEXT DEFAULT ''",
            "ALTER TABLE qa_items ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
        ):
            try:
                conn.execute(ddl)
            except sqlite3.OperationalError:
                pass

        conn.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS qa_fts USING fts5(
            question,
            answer,
            subject,
            content     = qa_items,
            content_rowid = id,
            tokenize    = 'unicode61'
        )""")

        conn.execute("""
        CREATE TRIGGER IF NOT EXISTS qa_ai AFTER INSERT ON qa_items BEGIN
            INSERT INTO qa_fts(rowid, question, answer, subject)
            VALUES (new.id, new.question, new.answer, new.subject);
        END""")

        conn.execute("""
        CREATE TRIGGER IF NOT EXISTS qa_au AFTER UPDATE ON qa_items BEGIN
            INSERT INTO qa_fts(qa_fts, rowid, question, answer, subject)
            VALUES ('delete', old.id, old.question, old.answer, old.subject);
            INSERT INTO qa_fts(rowid, question, answer, subject)
            VALUES (new.id, new.question, new.answer, new.subject);
        END""")

        # 이용자 피드백 테이블 (임계값 자동 튜닝 데이터 수집용)
        conn.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            query        TEXT    NOT NULL DEFAULT '',
            response_tier TEXT   NOT NULL DEFAULT '',
            top_score    REAL    DEFAULT 0,
            norm_score   REAL    DEFAULT 0,
            helpful      INTEGER NOT NULL DEFAULT 0,
            created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""")

        conn.commit()


def seed_from_json() -> int:
    """DB가 비어있으면 seed JSON 파일들에서 데이터를 일괄 삽입. 삽입 건수 반환."""
    if count_items() > 0:
        return 0
    seed_files = sorted(SEED_DIR.glob("nl_qa_seed_*.json"))
    if not seed_files:
        return 0
    total = 0
    with get_conn() as conn:
        for path in seed_files:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            conn.executemany("""
                INSERT OR IGNORE INTO qa_items
                    (rec_key, question, answer, subject, answer_date, answer_lib)
                VALUES (:rec_key, :question, :answer, :subject, :answer_date, :answer_lib)
            """, data)
            total += len(data)
        conn.commit()
    return total


def upsert_item(rec_key: str, question: str, answer: str, subject: str,
                reg_date: str = "", answer_date: str = "", answer_lib: str = "") -> bool:
    """Insert or update a Q&A item. ISBN·청구기호도 함께 추출 저장. Returns True if newly inserted."""
    meta = extract_metadata(answer)
    isbns_str = ",".join(meta["isbns"])
    callno_str = ",".join(meta["call_numbers"])
    with get_conn() as conn:
        existing = conn.execute(
            "SELECT id FROM qa_items WHERE rec_key = ?", (rec_key,)
        ).fetchone()

        if existing:
            conn.execute("""
            UPDATE qa_items SET question=?, answer=?, subject=?,
                reg_date=?, answer_date=?, answer_lib=?,
                isbns=?, call_numbers=?, updated_at=CURRENT_TIMESTAMP
            WHERE rec_key=?
            """, (question, answer, subject, reg_date, answer_date, answer_lib,
                  isbns_str, callno_str, rec_key))
            conn.commit()
            return False
        else:
            conn.execute("""
            INSERT INTO qa_items
                (rec_key, question, answer, subject, reg_date, answer_date, answer_lib,
                 isbns, call_numbers)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (rec_key, question, answer, subject, reg_date, answer_date, answer_lib,
                  isbns_str, callno_str))
            conn.commit()
            return True


def get_known_keys() -> set:
    with get_conn() as conn:
        rows = conn.execute("SELECT rec_key FROM qa_items").fetchall()
    return {r["rec_key"] for r in rows}


def count_items() -> int:
    with get_conn() as conn:
        return conn.execute("SELECT COUNT(*) FROM qa_items").fetchone()[0]


def get_items_for_index() -> list:
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT id, rec_key, question, answer, subject FROM qa_items"
        ).fetchall()
    return [dict(r) for r in rows]
