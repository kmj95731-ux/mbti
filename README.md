---
title: Mbtibooktalk
emoji: 📚
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
---

# 📚 MBTI Book Talk

> 같은 MBTI끼리 함께 나누는 책이야기 — MBTI 유형별 도서 추천 커뮤니티 웹앱

---

## 🚀 바로 열기

```
index.html  ←  이 파일 하나로 전체 앱이 실행됩니다
```

브라우저에서 `index.html`을 열거나, GitHub Pages로 배포하면 바로 사용 가능합니다.

---

## 📁 파일 구조

```
mbti-book-talk/
├── index.html      ← 전체 앱 (SPA, 단일 파일)
├── js/
│   └── data.js     ← 16종 MBTI 데이터 + 큐레이션 도서 (2019–2024)
└── README.md
```

---

## ✨ 주요 기능

| 기능 | 설명 |
|------|------|
| MBTI 검사 | Gemini AI 검사 링크 연결 |
| 유형 선택 | 16가지 MBTI 유형 직접 선택 |
| 큐레이션 도서 | 각 유형 특성 기반 최신 도서 추천 (선정 근거 포함) |
| 커뮤니티 추천 | 같은 유형 사람들끼리 도서 추천 + 한줄평 |
| 실시간 공유 | Firebase Firestore 연동 시 모든 사용자가 실시간 공유 |
| 하트 투표 | 마음에 드는 추천에 하트 |
| 도서 정보 | 알라딘 API + Google Books로 표지·정보 자동 로딩 |
| 도서관 링크 | 알라딘 구매 / 전북대 도서관 / Google Books 바로가기 |
| 독서 후기 | MBTI 뱃지와 함께 후기 남기기 |

---

## 🔥 Firebase 설정 (커뮤니티 공유 활성화)

> 설정 없이도 로컬 모드로 동작합니다. 다른 사람과 실시간 공유하려면 아래 설정이 필요합니다.

### 1단계 — Firebase 프로젝트 생성
[console.firebase.google.com](https://console.firebase.google.com) → 새 프로젝트 생성

### 2단계 — Firestore 활성화
Firestore Database → 데이터베이스 만들기 → **asia-northeast3(서울)** → 테스트 모드

### 3단계 — 웹 앱 등록 후 설정 복사
프로젝트 개요 → `</>` 아이콘 → 앱 등록 → `firebaseConfig` 복사

### 4단계 — index.html 상단 수정

`index.html` 맨 위 스크립트에서 아래 부분을 찾아 값을 교체:

```javascript
const FIREBASE_CONFIG = {
  apiKey:            "여기에_apiKey",      // ← Firebase에서 복사한 값으로 교체
  authDomain:        "여기에_authDomain",
  projectId:         "여기에_projectId",
  storageBucket:     "여기에_storageBucket",
  messagingSenderId: "여기에_messagingSenderId",
  appId:             "여기에_appId"
};
```

### Firestore 보안 규칙 (테스트용)
Firebase 콘솔 → Firestore → 규칙 탭:
```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /{document=**} {
      allow read, write: if true;
    }
  }
}
```

---

## 🌐 GitHub Pages 배포

```bash
# 1. GitHub 저장소 생성 후 업로드
# 2. 저장소 Settings → Pages → Branch: main → Save
# 3. https://{username}.github.io/{repo-name} 으로 접속
```

---

## 📖 도서 선정 기준

각 MBTI 유형의 **핵심 인지 기능과 가치관**에 맞는 책을 선정했습니다.

- **NT(분석가)**: 시스템 사고·원칙·이론 탐구 관련 도서
- **NF(외교관)**: 의미·공감·이상·감성 문학
- **SJ(관리자)**: 체계·습관·검증된 원칙·재정 관리
- **SP(탐험가)**: 현실 실행·모험·즉각적 성과·감각적 경험

모든 책에는 해당 유형에 추천하는 구체적인 이유가 표시됩니다.

---

## 🔧 사용된 기술

- **HTML/CSS/JS** (단일 파일 SPA, 프레임워크 없음)
- **Firebase Firestore** (실시간 공유 DB)
- **알라딘 TTB API** (도서 검색, key: ttbpopi07062229002)
- **Google Books API** (도서 표지 및 소개)
- **Google Fonts** (Black Han Sans, Noto Sans KR)

---

## 📌 향후 개발 예정

- [ ] 연령별 필터 (어린이/청소년/성인)
- [ ] 음성 후기 입력
- [ ] 도서 투표 랭킹
- [ ] 학교 도서관 소장 여부 연결
- [ ] 우수 추천 시상 시스템
