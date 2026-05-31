---
title: Mbtibooktalk
emoji: 📚
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
---

# 📚 MBTI Book Talk
### Claude AI로 제작한 MBTI 성격 유형별 도서 추천 웹앱

> **Live** → [minjin1-mbti.hf.space](https://minjin1-mbti.hf.space) &nbsp;|&nbsp; **GitHub** → [github.com/kmj95731-ux/mbti](https://github.com/kmj95731-ux/mbti)

---

## 🤖 Claude AI로 만들어진 앱

이 웹앱은 **Claude Code** (Anthropic의 AI 개발 도구)를 사용하여 처음부터 끝까지 제작되었습니다.

| 항목 | 내용 |
|------|------|
| 개발 도구 | Claude Code CLI (`claude-sonnet-4-6` 모델) |
| 개발 방식 | 자연어로 기능을 설명 → Claude가 코드 작성·수정·디버깅 수행 |
| 테스트 | Playwright 브라우저 자동화 테스트도 Claude가 직접 작성 및 실행 |
| 배포 | GitHub → HuggingFace Spaces 자동 동기화 (GitHub Actions) |

---

## 🏗️ 시스템 아키텍처

```
┌──────────────────────────────────────────────────────────┐
│                      사용자 브라우저                        │
│               index.html  (단일 페이지 앱)                  │
│    MBTI 검사 / 도서검색 / 큐레이션 / 사서 Q&A              │
└──────────────────────┬───────────────────────────────────┘
                       │  HTTP API
┌──────────────────────▼───────────────────────────────────┐
│              FastAPI 서버  (Python, 포트 7860)              │
│                                                            │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────────┐  │
│  │ search_      │  │ semantic_    │  │  claude_       │  │
│  │ engine.py    │  │ engine.py    │  │  chat.py       │  │
│  │ (하이브리드)  │  │ (임베딩)     │  │  (AI 사서)     │  │
│  └──────┬───────┘  └──────┬───────┘  └───────┬────────┘  │
│         └─────────────────┴──────────────────┘            │
│                            │                               │
│         ┌──────────────────▼──────────────────┐           │
│         │      SQLite DB  (사서 Q&A 5,905건)   │           │
│         └─────────────────────────────────────┘           │
└──────────────────────┬───────────────────────────────────┘
                       │  외부 API 연동
        ┌──────────────┼──────────────────┐
        ▼              ▼                  ▼
  국립중앙도서관     알라딘 TTB        Google Books
   Open API          도서 검색          도서 검색
  (사서 Q&A DB)    (표지·메타데이터)  (보조 검색)
```

---

## ✨ 주요 기능 4가지

### 1. 🔍 MBTI 검사
- 20문항 성격 유형 검사 → MBTI 16가지 유형 결정
- 결과에 따라 맞춤 도서 큐레이션 페이지로 자동 이동

### 2. 👥 MBTI별 도서 커뮤니티 방
- 16개 유형별 전용 방 운영
- 도서 검색 → 추천글 작성 → 실시간 커뮤니티 공유
- 큐레이션 도서 + 사용자 추천 도서 통합 표시

### 3. 🏛️ 주제별 도서 큐레이션
- 국립중앙도서관 Open API 연동
- **자연어 검색 지원** → 핵심 키워드 자동 추출 → 도서 검색
- KDC(한국십진분류법) 자동 분류 표시

### 4. 💬 사서에게 물어보세요
- 국립중앙도서관 사서 Q&A 데이터 **5,905건** 기반 RAG 검색
- 자연어 질문 → 관련 Q&A 검색 → 답변 생성
- 참고 출처 카드 함께 제공

---

## 🔎 핵심 로직 ① 자연어 키워드 추출

자연어 문장을 그대로 도서 API에 보내면 결과가 0건 → **키워드 자동 추출** 로직 적용

### 처리 흐름

```
입력: "힘들때 위로가 되는 책 추천해줘"
        │
        ▼
① 어미·조사 제거
   힘들때 → 힘들 (때 제거)
   위로가 → 위로 (가 제거)
   추천해줘 → 추천 (해줘 제거) → 노이즈어 → 삭제
        │
        ▼
② 노이즈어 필터 (책, 추천, 읽기, 좋은, 싶을, 찾고 등)
   "되는", "책", "추천" 제거
        │
        ▼
출력: "힘들 위로"  ← 이 키워드로 알라딘 API 검색
```

### MBTI 유형 코드 처리

```
입력: "MBTI INFP에게 추천하는 소설"
        │
        ▼
INFP, INTJ, ENFP 등 16가지 유형 코드 감지
        │
        ▼
유형 코드 → "MBTI" 로 통합
        │
        ▼
출력: "MBTI 소설"  ← 알라딘에 실제 책이 있는 검색어
```

### 적용 범위

| 섹션 | 자연어 지원 |
|------|------------|
| 도서검색 (추천하기 탭) | ✅ |
| 주제별 도서 큐레이션 | ✅ |
| 사서에게 물어보세요 | ✅ (하이브리드 검색으로 처리) |

---

## 🔎 핵심 로직 ② 하이브리드 검색 (사서 Q&A)

두 가지 검색 방식을 결합하여 정확도를 높임

```
사용자 질문
     │
     ├──────────────────────────────┐
     ▼                              ▼
 벡터 검색                      키워드 검색
 (시맨틱 임베딩)                (BM25 알고리즘)
                                   
 ko-sroberta 모델               SQLite FTS5
 → 의미가 비슷한 Q&A 탐색       → 단어가 일치하는 Q&A 탐색
 예) "슬플 때" ≈ "우울할 때"    예) "판타지" = "판타지"
     │                              │
     └──────────────┬───────────────┘
                    ▼
          RRF (순위 융합 알고리즘)
          두 결과의 순위를 통합·정규화
                    │
                    ▼
          동적 가중치 적용
```

### 동적 가중치

쿼리 길이와 검색 엔진 종류에 따라 자동으로 비중 조정

| 엔진 | 쿼리 | 벡터 | 키워드 |
|------|------|------|--------|
| 시맨틱 | 1~2단어 (`판타지`) | 0.40 | **0.60** |
| 시맨틱 | 3~4단어 (`자기계발 책 추천`) | 0.55 | 0.45 |
| 시맨틱 | 5단어+ (`힘들 때 위로가 되는 소설`) | **0.70** | 0.30 |
| TF-IDF 폴백 | 1~2단어 | 0.30 | **0.70** |
| TF-IDF 폴백 | 5단어+ | 0.50 | 0.50 |

> **왜 동적 가중치인가?**  
> 짧은 단어 → 정확한 단어 매칭이 유리 (키워드 우세)  
> 긴 자연어 문장 → 의미 파악이 중요 (벡터 우세)  
> TF-IDF 폴백 시 → 의미 파악 약화, 키워드를 더 신뢰

---

## 📥 Input / 📤 Output 상세

### 도서검색 API (`/api/book-search`)

```
Input  : query = "우울할 때 읽으면 좋은 책"
           ↓  _extract_book_keywords()
Processing: "우울할" → "우울", "읽으면"·"좋은"·"책" 제거
           ↓
Effective Query: "우울"
           ↓  알라딘 API + Google Books API 병렬 호출
Output : [
  { title, author, publisher, cover_url, isbn },
  ...
]
```

### 사서 Q&A API (`/api/librarian/ask`)

```
Input  : query = "힘들 때 위로가 되는 책 추천해줘"
           ↓  hybrid_search()
Processing:
  1. 벡터 검색 → 상위 16건 후보
  2. 키워드 검색 → 상위 16건 후보
  3. RRF 융합 → 동적 가중치(0.70:0.30) 적용
  4. 상위 8건 선택
           ↓  get_librarian_response()
Output : {
  response: "사서 답변 텍스트",
  sources: [ Q&A 출처 카드 8건 ],
  vector_engine: "tfidf",
  weights: { vector: 0.70, keyword: 0.30 }
}
```

### 큐레이션 API (`/api/analyze`)

```
Input  : keyword = "역사를 쉽게 이해할 수 있는 책 알려줘"
           ↓  _extract_book_keywords()
Effective: "역사 이해"
           ↓  국립중앙도서관 Open API
Output : {
  keyword: "역사를 쉽게...",  ← 표시용 원본 유지
  kdc: { code, name, color },  ← 자동 KDC 분류
  pagination: { total: 2587, ... },
  search_results: [ 도서 목록 ]
}
```

---

## 🛠️ 기술 스택

| 구분 | 기술 |
|------|------|
| **프론트엔드** | HTML5 / CSS3 / Vanilla JS (단일 파일 SPA) |
| **백엔드** | Python 3.11 / FastAPI |
| **벡터 검색** | `jhgan/ko-sroberta-multitask` (한국어 시맨틱 임베딩) |
| **키워드 검색** | SQLite FTS5 / BM25 |
| **TF-IDF 폴백** | scikit-learn TfidfVectorizer (word 1~2 gram) |
| **외부 API** | 국립중앙도서관 Open API / 알라딘 TTB / Google Books |
| **배포** | HuggingFace Spaces (Docker 컨테이너) |
| **CI/CD** | GitHub Actions |

---

## 📊 데이터 현황

| 항목 | 수치 |
|------|------|
| 사서 Q&A DB | **5,905건** (국립중앙도서관) |
| MBTI 큐레이션 도서 | 16개 유형 × 다수 |
| 연동 외부 도서 DB | 알라딘 + Google Books |

---

## 🚀 배포 구조

```
로컬 수정
   │
   ├─ git push origin master ─→ GitHub (소스 보관)
   │                                │
   │                         GitHub Actions
   │                                │
   └─ git push hf HEAD:main ──→ HuggingFace Spaces
                                    │
                              Docker 빌드 & 배포
                                    │
                            https://minjin1-mbti.hf.space
```

---

## 📅 개발 이력

| 날짜 | 작업 내용 |
|------|----------|
| 2026-05-28 | 초기 앱 구축 및 HuggingFace 배포, GitHub Actions CI/CD 설정 |
| 2026-05-31 | UI 버튼 수정, 하이브리드 검색 동적 가중치 도입, 전 섹션 자연어 검색 적용 |

---

## ✅ 테스트 결과 (2026-05-31)

| 테스트 항목 | 방법 | 결과 |
|------------|------|------|
| 자연어 도서검색 10개 쿼리 | API 테스트 | **10/10 PASS** |
| 앱 직접 검색 (도서검색 탭) | Playwright | **7/7 PASS** |
| 사서에게 물어보세요 | Playwright | **5/5 PASS** |

---

*Built with [Claude Code](https://claude.ai/code) — Anthropic*
