import streamlit as st
from google import genai
from google.genai import types
from datetime import datetime, timedelta


st.set_page_config(
    page_title="AI 여행 플래너 ✈️",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(160deg, #f0f4ff 0%, #fafbff 100%);
    }
    .hero-banner {
        background: linear-gradient(135deg, #1a73e8 0%, #0d47a1 60%, #6c2dcf 100%);
        padding: 2rem 2.5rem;
        border-radius: 16px;
        color: white;
        margin-bottom: 1.8rem;
        box-shadow: 0 8px 32px rgba(26,115,232,0.18);
    }
    .hero-banner h1 { font-size: 2.2rem; margin: 0 0 0.4rem 0; font-weight: 800; }
    .hero-banner p  { margin: 0; opacity: 0.88; font-size: 1.05rem; }
    .result-card {
        background: white;
        border-radius: 14px;
        padding: 1.8rem 2rem;
        box-shadow: 0 4px 24px rgba(26,115,232,0.10);
        border-left: 5px solid #1a73e8;
        margin-bottom: 1.2rem;
    }
    .stButton > button[kind="primary"] {
        background: linear-gradient(90deg, #1a73e8, #6c2dcf);
        border: none;
        border-radius: 10px;
        font-weight: 700;
        font-size: 1.05rem;
        padding: 0.55rem 2.2rem;
        color: white;
    }
</style>
""", unsafe_allow_html=True)


def init_gemini():
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        if not api_key or api_key.strip() == "":
            return None, "GEMINI_API_KEY가 비어 있습니다."
        client = genai.Client(api_key=api_key)
        return client, None
    except KeyError:
        return None, "secrets.toml 파일에 GEMINI_API_KEY가 등록되지 않았습니다."
    except Exception as e:
        return None, f"API 초기화 오류: {str(e)}"


def build_system_prompt() -> str:
    return """당신은 전문 여행 플래너입니다. 사용자가 제공한 여행 정보를 바탕으로
맞춤형 여행 일정을 아래 형식에 맞게 작성해 주세요.

## 출력 형식 (반드시 준수)

### 📅 일자별 일정
- 각 날짜마다 **오전 / 오후 / 저녁** 세 블록으로 나눠 구체적인 활동을 작성합니다.
- 장소명, 소요 시간, 간단한 설명을 포함합니다.
- 이동 수단 팁도 간략히 포함합니다.

### 🍽 추천 맛집 3곳
각 맛집마다:
- **식당명**: (이름)
- **특징**: (음식 스타일, 분위기, 대표 메뉴)
- **가격대**: (1인 기준 대략적인 금액)

### 💡 여행 꿀팁 3가지
번호를 매겨 여행자가 놓치기 쉬운 실질적인 팁을 작성합니다.

### ⚠️ 주의사항
여행지의 기후·문화·안전·교통 관련 중요 주의사항을 2~4가지 작성합니다.

---
**톤 가이드**: 친근하고 실용적인 어조. 초보 여행자도 이해할 수 있게 작성합니다.
**언어**: 반드시 한국어로 작성합니다.
"""


def generate_itinerary(client, destination: str, days: int,
                        style: str, companion: str, budget: str) -> str:
    user_prompt = f"""
다음 여행 정보를 바탕으로 맞춤 여행 일정을 작성해 주세요.

- 여행지: {destination}
- 여행 기간: {days}일
- 여행 스타일: {style}
- 동행 유형: {companion}
- 예산: {budget}

위 조건에 맞게 실용적이고 구체적인 일정을 작성해 주세요.
"""
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=user_prompt,
        config=types.GenerateContentConfig(
            system_instruction=build_system_prompt(),
        ),
    )
    if not response.text:
        raise ValueError("AI 응답이 비어 있습니다. 다시 시도해 주세요.")
    return response.text


if "history" not in st.session_state:
    st.session_state.history = []

if "current_result" not in st.session_state:
    st.session_state.current_result = None

if "current_info" not in st.session_state:
    st.session_state.current_info = None


st.markdown("""
<div class="hero-banner">
    <h1>✈️ AI 여행 플래너</h1>
    <p>여행지와 스타일만 입력하면 Gemini AI가 맞춤 일정을 즉시 생성합니다.</p>
</div>
""", unsafe_allow_html=True)

model, api_error = init_gemini()

if api_error:
    st.error(f"🔑 API 연결 실패: {api_error}")
    st.markdown("""
**해결 방법:**
1. 프로젝트 루트에 `.streamlit/secrets.toml` 파일을 생성하세요.
2. 아래 내용을 추가하세요:
```toml
GEMINI_API_KEY = "여기에_실제_API_키_입력"
```
3. Gemini API 키는 [Google AI Studio](https://aistudio.google.com/app/apikey)에서 무료로 발급받을 수 있습니다.
    """)
    st.stop()


col_input, col_result = st.columns([1, 1.6], gap="large")

with col_input:
    st.subheader("🗺️ 여행 정보 입력", divider="blue")

    destination = st.text_input(
        "📍 여행지",
        placeholder="예: 도쿄, 파리, 제주도, 뉴욕...",
        help="국내·해외 모두 가능합니다.",
    )

    today = datetime.today().date()
    date_range = st.date_input(
        "📅 여행 기간",
        value=(today, today + timedelta(days=2)),
        min_value=today,
        format="YYYY/MM/DD",
    )

    if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
        start_date, end_date = date_range
        days = (end_date - start_date).days + 1
        st.caption(f"📆 {start_date.strftime('%Y.%m.%d')} ~ {end_date.strftime('%Y.%m.%d')} · 총 {days}일")
    else:
        days = None
        st.caption("⬆️ 종료 날짜를 선택해 주세요.")

    style = st.selectbox(
        "🎨 여행 스타일",
        options=["힐링", "액티비티", "맛집 투어", "문화·역사", "쇼핑"],
    )

    companion = st.selectbox(
        "👥 동행 유형",
        options=["혼자", "커플", "가족", "친구들"],
    )

    budget = st.selectbox(
        "💰 예산",
        options=["저예산 (알뜰 여행)", "보통 (합리적 여행)", "여유있게 (프리미엄 여행)"],
    )

    st.divider()

    generate_btn = st.button(
        "🚀 AI 일정 생성하기",
        type="primary",
        use_container_width=True,
        disabled=(not destination.strip() or days is None),
    )

    if not destination.strip():
        st.caption("⬆️ 여행지를 입력하면 버튼이 활성화됩니다.")

    with st.expander("💡 입력 예시 보기"):
        st.markdown("""
- **여행지**: 오사카
- **기간**: 4일
- **스타일**: 맛집 투어
- **동행**: 커플
- **예산**: 보통
        """)


if generate_btn and destination.strip() and days is not None:
    with st.spinner("✈️ AI가 맞춤 여행 일정을 생성 중입니다... 잠시만 기다려 주세요!"):
        try:
            result_text = generate_itinerary(
                client=model,
                destination=destination.strip(),
                days=days,
                style=style,
                companion=companion,
                budget=budget,
            )

            st.session_state.current_result = result_text
            st.session_state.current_info = {
                "destination": destination.strip(),
                "days": days,
                "style": style,
                "companion": companion,
                "budget": budget,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
            }

            st.session_state.history.insert(0, {
                "info": st.session_state.current_info,
                "result": result_text,
            })
            if len(st.session_state.history) > 5:
                st.session_state.history = st.session_state.history[:5]

        except Exception as e:
            error_msg = str(e)
            if "quota" in error_msg.lower() or "rate" in error_msg.lower():
                st.error("⏳ API 요청 한도에 도달했습니다. 잠시 후 다시 시도해 주세요.")
            elif "invalid" in error_msg.lower() or "api_key" in error_msg.lower():
                st.error("🔑 API 키가 유효하지 않습니다. secrets.toml을 확인해 주세요.")
            else:
                st.error(f"❌ 일정 생성 중 오류가 발생했습니다: {error_msg}")


with col_result:
    if st.session_state.current_result:
        info = st.session_state.current_info

        st.subheader(
            f"📋 {info['destination']} {info['days']}일 여행 일정",
            divider="blue",
        )
        st.markdown(
            f"**{info['style']}** · **{info['companion']}** · **{info['budget']}** "
            f"<span style='color:#888; font-size:0.85rem;'>— {info['timestamp']}</span>",
            unsafe_allow_html=True,
        )

        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        st.markdown(st.session_state.current_result)
        st.markdown('</div>', unsafe_allow_html=True)

        st.download_button(
            label="📥 일정 텍스트 다운로드",
            data=st.session_state.current_result,
            file_name=f"{info['destination']}_{info['days']}일_여행일정.txt",
            mime="text/plain",
            use_container_width=True,
        )

    else:
        st.subheader("📋 여행 일정이 여기에 표시됩니다", divider="blue")
        st.markdown("""
        <div style="text-align:center; padding: 3rem 1rem; color: #888;">
            <div style="font-size:4rem;">✈️</div>
            <p style="font-size:1.1rem; margin-top:1rem;">
                왼쪽에서 여행 정보를 입력하고<br>
                <b>AI 일정 생성하기</b> 버튼을 클릭하세요!
            </p>
        </div>
        """, unsafe_allow_html=True)


with st.sidebar:
    st.markdown("## ✈️ AI 여행 플래너")
    st.caption("Powered by Gemini 2.0 Flash")
    st.divider()

    if model:
        st.success("✅ Gemini API 연결됨", icon="🔑")
    else:
        st.error("❌ API 연결 실패")

    st.divider()

    st.markdown("### 📂 최근 일정 히스토리")
    if st.session_state.history:
        for i, item in enumerate(st.session_state.history):
            info = item["info"]
            if st.button(
                f"{'🔵' if i == 0 else '⚪'} {info['destination']} {info['days']}일 · {info['style']}",
                key=f"history_{i}",
                use_container_width=True,
            ):
                st.session_state.current_result = item["result"]
                st.session_state.current_info = info
                st.rerun()
    else:
        st.caption("아직 생성된 일정이 없습니다.")

    st.divider()

    st.markdown("### 💡 사용 팁")
    st.markdown("""
- 여행지는 **구체적**일수록 더 좋은 일정이 생성됩니다
- 히스토리에서 **이전 결과**를 다시 확인할 수 있어요
- **텍스트 파일로 저장**해 두면 오프라인에서도 확인 가능합니다
    """)

    st.divider()
    st.caption("© 2026 AI 여행 플래너\nGemini API 기반 여행 일정 생성 서비스")
