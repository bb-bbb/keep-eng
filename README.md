# 🎧 YouTube English Study AI

> **유튜브 영상 하나로 영어 학습 노트를 자동 생성하고, 반복 학습까지 관리해주는 AI 기반 영어 공부 서비스**

---

## 📌 프로젝트 개요

YouTube English Study AI는 사용자가  **유튜브 영어 영상 링크를 입력하면** ,

* 영어 자막을 자동으로 추출하고
* 문단 단위로 정리하여
* 🇺🇸 영어 문장 / 🇰🇷 자연스러운 한국어 번역
* 핵심 **숙어·표현 정리**
* **반복 학습(Spaced Repetition)** 을 위한 복습 스케줄 생성
* 복습 시점에 **알림(Reminder)** 제공

까지 한 번에 처리해주는 **AI 영어 학습 보조 서비스**입니다.

이 프로젝트는 단순 번역기가 아니라, **실제 영어 학습 흐름**을 고려한 구조로 설계되었습니다.

---

## 🎯 핵심 기능 (Features)

### 1. 유튜브 링크 기반 영어 학습

* 영어 자막이 포함된 유튜브 영상 링크 입력
* 자동 자막 추출

### 2. 문단 단위 학습 노트 생성

각 문단마다:

* 영어 원문
* 자연스러운 한국어 번역
* 중요 숙어 / 표현 정리
* 숙어별 의미 + 예문 제공
* ▶️ **문단 시작 시점부터 영상/음성 재생 버튼 제공**

### 3. AI 기반 언어 분석

* LLM을 활용한 번역 및 표현 분석
* 시험 영어가 아닌 **실제 사용되는 영어 표현 중심**

### 4. 반복 학습 시스템 (Spaced Repetition)

* 0일 / 2일 / 5일 / 10일 주기 복습
* 학습 상태에 따라 복습 일정 조정 가능

### 5. 알림 시스템 (예정)

* 이메일 기반 복습 알림
* 추후 웹 푸시 / 모바일 알림 확장 가능

---

## 🧠 전체 시스템 흐름

```
YouTube URL
   ↓
자막 추출 (English Transcript)
   ↓
문단 단위 분리
   ↓
AI 분석 (번역 + 숙어)
   ↓
학습 노트 저장
   ↓
복습 스케줄 생성
   ↓
알림 전송
```

---

## 🛠 기술 스택 (Tech Stack)

### Backend

* **Python**
* **FastAPI**
* YouTube Transcript API
* OpenAI / LLM API

### Database

* SQLite (MVP)
* PostgreSQL (확장 예정)

### Frontend

* 간단한 HTML/CSS (MVP)
* Next.js (확장 예정)

### Infra / Deployment

* Vercel
* Railway / Render

---

## 📂 프로젝트 구조 (예시)

```
backend/
├─ app/
│ ├─ main.py # FastAPI 엔트리포인트
│ ├─ routers/
│ │ └─ study.py # 유튜브 링크 → 학습 노트 생성 API
│ ├─ services/
│ │ ├─ youtube.py # 자막 추출 + 타임스탬프 처리
│ │ ├─ paragraph.py # 문장 → 문단 분리 로직
│ │ ├─ llm.py # 번역 + 숙어 분석 (LLM)
│ │ ├─ audio.py # 문단별 재생용 timestamp 매핑
│ │ └─ scheduler.py # 반복 학습 스케줄 생성
│ ├─ models/
│ │ ├─ video.py # YouTube 영상 모델
│ │ ├─ paragraph.py # 문단 + start_time 저장
│ │ ├─ idiom.py # 숙어 / 표현 모델
│ │ └─ review.py # 복습 스케줄 모델
│ └─ database.py # DB 연결


frontend/
├─ components/
│ ├─ VideoPlayer.tsx # 유튜브 iframe + start 제어
│ ├─ ParagraphCard.tsx # 문단 카드 + ▶️ 재생 버튼
│ └─ IdiomList.tsx # 숙어 리스트
├─ pages/
│ └─ index.tsx # 메인 학습 페이지
└─ styles/


README.md
```

---

## 🧪 MVP 목표

### Phase 1 (현재)

* [X] 유튜브 자막 추출
* [X] 문단 단위 정리
* [X] AI 번역 + 숙어 분석
* [X] 웹에서 학습 노트 출력

### Phase 2 (예정)

* [ ] 사용자 계정
* [ ] 반복 학습 스케줄링
* [ ] 이메일 알림

### Phase 3 (확장)

* [ ] 모바일 대응 UI
* [ ] 개인별 학습 통계
* [ ] 북마크 / 즐겨찾기

---

## 💡 이 프로젝트를 만든 이유

영어 공부를 하면서 느낀 가장 큰 문제는:

> “좋은 영어 콘텐츠는 많은데,  **정리하고 반복하기가 너무 귀찮다** ”

이 프로젝트는 **실제 학습자의 관점**에서,

* 입력은 최소화하고
* 정리는 자동화하며
* 기억은 반복으로 강화하는

**지속 가능한 영어 학습 도구**를 목표로 합니다.

---

## 🧑‍💻 Author

* **ningning**
* AI / NLP / LLM Engineering

---

## 📜 License

This project is licensed under the MIT License.
