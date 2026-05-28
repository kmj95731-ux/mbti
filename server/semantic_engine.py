"""한국어 시맨틱 임베딩 검색 엔진.

- sentence-transformers + ko-sroberta-multitask 사용
- 모델 미설치·메모리 부족 등 환경 문제 발생 시 자동으로 비활성화
- 임베딩 행렬은 디스크에 캐시(.npz)하여 재시작 시 즉시 로드

ENV
---
SEMANTIC_MODEL : 한국어 임베딩 모델명 (기본: jhgan/ko-sroberta-multitask)
SEMANTIC_ENABLED : "0" 으로 설정 시 강제 비활성화
"""

from __future__ import annotations

import os
import pickle
from pathlib import Path
from typing import Optional

import numpy as np

from .database import get_conn, get_items_for_index

MODEL_NAME = os.getenv("SEMANTIC_MODEL", "jhgan/ko-sroberta-multitask")
CACHE_PATH = Path(__file__).parent / "semantic_cache.pkl"
DISABLED = os.getenv("SEMANTIC_ENABLED", "1") == "0"

_model = None
_embeddings: Optional[np.ndarray] = None
_ids: list[int] = []
_rec_keys: list[str] = []
_load_failed: bool = False


def _try_load_model():
    """sentence-transformers 모델을 지연 로드. 실패 시 None 반환."""
    global _model, _load_failed
    if DISABLED or _load_failed:
        return None
    if _model is not None:
        return _model
    try:
        from sentence_transformers import SentenceTransformer  # type: ignore
        _model = SentenceTransformer(MODEL_NAME)
        return _model
    except Exception as e:
        _load_failed = True
        print(f"[semantic_engine] 모델 로드 실패 → TF-IDF 폴백: {e}")
        return None


def is_available() -> bool:
    """시맨틱 검색 가용 여부."""
    if DISABLED:
        return False
    if _embeddings is not None:
        return True
    return _try_load_model() is not None


def build_index() -> bool:
    """전체 Q&A에 대해 임베딩을 생성하여 디스크 캐시."""
    global _embeddings, _ids, _rec_keys
    model = _try_load_model()
    if model is None:
        return False

    rows = get_items_for_index()
    if not rows:
        return False

    _ids = [r["id"] for r in rows]
    _rec_keys = [r["rec_key"] for r in rows]
    texts = [f"{r['question']} {r['answer']}"[:1024] for r in rows]

    print(f"[semantic_engine] {len(texts)}건 임베딩 생성 중...")
    embs = model.encode(texts, batch_size=32, show_progress_bar=False,
                        convert_to_numpy=True, normalize_embeddings=True)
    _embeddings = embs.astype(np.float32)

    with open(CACHE_PATH, "wb") as f:
        pickle.dump({"ids": _ids, "rec_keys": _rec_keys,
                     "embeddings": _embeddings, "model": MODEL_NAME}, f)
    print(f"[semantic_engine] 임베딩 캐시 저장 완료 ({_embeddings.shape})")
    return True


def _ensure_loaded() -> bool:
    global _embeddings, _ids, _rec_keys
    if _embeddings is not None:
        return True
    if not CACHE_PATH.exists():
        return False
    try:
        with open(CACHE_PATH, "rb") as f:
            data = pickle.load(f)
        _embeddings = data["embeddings"]
        _ids = data["ids"]
        _rec_keys = data["rec_keys"]
        return True
    except Exception as e:
        print(f"[semantic_engine] 캐시 로드 실패: {e}")
        return False


def semantic_search(query: str, top_k: int = 10) -> list[dict]:
    """시맨틱 임베딩 기반 코사인 유사도 검색."""
    if not is_available():
        return []
    if not _ensure_loaded():
        return []
    model = _try_load_model()
    if model is None:
        return []

    q_vec = model.encode([query], convert_to_numpy=True, normalize_embeddings=True)[0]
    scores = (_embeddings @ q_vec).astype(np.float32)
    top_idx = np.argsort(scores)[::-1][: top_k * 2]
    top_idx = [i for i in top_idx if scores[i] >= 0.2][:top_k]
    if not top_idx:
        return []

    id_list = [_ids[i] for i in top_idx]
    placeholders = ",".join("?" * len(id_list))
    with get_conn() as conn:
        rows = conn.execute(
            f"SELECT id, rec_key, question, answer, subject, answer_date, answer_lib "
            f"FROM qa_items WHERE id IN ({placeholders})",
            id_list,
        ).fetchall()
    by_id = {r["id"]: dict(r) for r in rows}

    results = []
    for i in top_idx:
        row = by_id.get(_ids[i])
        if row:
            results.append({**row, "score": float(scores[i]), "search_type": "semantic"})
    return results


def invalidate_cache() -> None:
    global _embeddings, _ids, _rec_keys
    _embeddings = None
    _ids = []
    _rec_keys = []
    if CACHE_PATH.exists():
        CACHE_PATH.unlink()
