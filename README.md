# ✈️ AI 여행 플래너

Gemini 2.0 Flash 기반의 맞춤 여행 일정 생성 Streamlit 웹앱입니다.

여행지, 기간, 스타일만 입력하면 AI가 일자별 일정 · 맛집 추천 · 꿀팁을 즉시 생성합니다.

---

## 📸 주요 기능

- 🗺️ 여행지·기간·스타일·예산 입력으로 맞춤 일정 생성
- 📅 일자별 오전/오후/저녁 구분 상세 일정
- 🍽 추천 맛집 3곳 (특징·가격대 포함)
- 💡 여행 꿀팁 3가지 + ⚠️ 주의사항
- 📂 히스토리 — 최근 5개 일정 사이드바에서 바로 확인
- 📥 텍스트 파일 다운로드 지원

---

## 🚀 로컬 실행 방법

### 1단계 — 패키지 설치

```bash
pip install -r requirements.txt
```

### 2단계 — Gemini API 키 발급

[Google AI Studio](https://aistudio.google.com/app/apikey) 접속 → **Create API key** 클릭 → 키 복사

### 3단계 — API 키 설정

```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

`.streamlit/secrets.toml` 파일을 열어 API 키 입력:

```toml
GEMINI_API_KEY = "여기에_실제_API_키_입력"
```

> ⚠️ `secrets.toml`은 `.gitignore`에 포함되어 있으므로 Git에 올라가지 않습니다.

### 4단계 — 앱 실행

```bash
streamlit run app.py
```

---

## ☁️ Streamlit Cloud 배포 방법

### 1단계 — [share.streamlit.io](https://share.streamlit.io) 접속

GitHub 계정으로 로그인 후 **New app** 클릭

### 2단계 — 레포 연결

| 항목 | 값 |
|------|-----|
| Repository | `YOUR_USERNAME/travel-planner-ai` |
| Branch | `main` |
| Main file path | `app.py` |

### 3단계 — Secrets 등록

**Advanced settings** → **Secrets** 탭에 아래 내용 붙여넣기:

```toml
GEMINI_API_KEY = "여기에_실제_Gemini_API_키_입력"
```

### 4단계 — Deploy!

배포 완료 후 아래 형식의 공유 URL이 생성됩니다:

```
https://YOUR_USERNAME-travel-planner-ai-app-XXXXX.streamlit.app
```

---

## 📁 파일 구조

```
travel-planner-ai/
├── app.py                         # 메인 Streamlit 앱
├── requirements.txt               # 의존 패키지
├── .gitignore
├── README.md
└── .streamlit/
    └── secrets.toml.example       # API 키 설정 예시
```

## 🛠️ 기술 스택

| 기술 | 용도 |
|------|------|
| Streamlit | 웹앱 프레임워크 |
| Google Gemini 2.0 Flash | AI 일정 생성 모델 |
| google-generativeai | Gemini Python SDK |
