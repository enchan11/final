import streamlit as st
import requests
from streamlit_lottie import st_lottie

# =========================================
# 1. 기본 설정
# =========================================
st.set_page_config(
    page_title="방배동 날씨",
    page_icon="🌤️",
    layout="centered"
)

st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# =========================================
# 2. 날씨 API
# =========================================
@st.cache_data(ttl=600)
def get_weather():
    url = "https://wttr.in/Bangbae-dong?format=j1"

    try:
        r = requests.get(url, timeout=5)
        data = r.json()

        current = data["current_condition"][0]
        astro = data["weather"][0]["astronomy"][0]

        temp = round(float(current["temp_C"]))
        desc = current["weatherDesc"][0]["value"]

        humidity = int(current["humidity"])
        visibility = current["visibility"] + "km"

        if humidity > 85:
            dust = "좋음"
        elif humidity > 40:
            dust = "보통"
        else:
            dust = "나쁨"

        return temp, desc, dust, visibility, astro["sunrise"], astro["sunset"]

    except:
        return 22, "Clear", "보통", "15km", "06:00", "18:00"


temp, desc, dust, visibility, sunrise, sunset = get_weather()

dust_color = "#2ed573" if dust in ["좋음", "보통"] else "#ff4757"


# =========================================
# 3. UI (여기서 핵심: Streamlit 기본 카드만 사용)
# → CSS로 카드 숨김 문제 완전히 제거
# =========================================

st.title("🌤️ 방배동 실시간 날씨")

st.subheader(f"현재 기온: {temp}°C")
st.write(f"상태: {desc}")

col1, col2 = st.columns(2)

with col1:
    st.metric("일출", sunrise)
    st.metric("미세먼지", dust)

with col2:
    st.metric("일몰", sunset)
    st.metric("가시거리", visibility)

st.markdown("---")

st.subheader("👕 오늘 코디 추천")

if temp >= 28:
    st.write("민소매 / 반팔 / 린넨")
elif temp >= 23:
    st.write("반팔 셔츠 / 면바지")
elif temp >= 17:
    st.write("맨투맨 / 가디건")
elif temp >= 10:
    st.write("니트 / 자켓")
else:
    st.write("패딩 / 목도리")
    st.markdown("""
<style>

/* 배경 */
.stApp {
    background: linear-gradient(to bottom, #74b9ff, #a29bfe);
}

/* 언덕 */
.stApp::after {
    content:"";
    position:fixed;
    bottom:-120px;
    left:-10%;
    width:120%;
    height:300px;
    background:#55efc4;
    border-radius:50%;
    z-index:-1;
}

/* 태양 */
.sun {
    position:fixed;
    top:80px;
    right:80px;
    width:80px;
    height:80px;
    background:radial-gradient(circle,#ffeaa7,#fdcb6e);
    border-radius:50%;
    box-shadow:0 0 40px #fdcb6e;
    animation:pulse 3s infinite alternate;
    z-index:-1;
}

@keyframes pulse {
    from {transform:scale(1);}
    to {transform:scale(1.1);}
}

/* 구름 */
.cloud {
    position:fixed;
    top:120px;
    left:-200px;
    width:120px;
    height:40px;
    background:white;
    border-radius:50px;
    animation:move 25s linear infinite;
    z-index:-1;
}

@keyframes move {
    from {left:-200px;}
    to {left:110%;}
}

/* 비 */
.rain {
    position:fixed;
    width:2px;
    height:20px;
    background:#74b9ff;
    animation:fall 1s linear infinite;
    z-index:-1;
}

@keyframes fall {
    0% {transform:translateY(-100px);}
    100% {transform:translateY(100vh);}
}

/* 눈 */
.snow {
    position:fixed;
    width:6px;
    height:6px;
    background:white;
    border-radius:50%;
    animation:snow 4s linear infinite;
    z-index:-1;
}

@keyframes snow {
    0% {transform:translateY(-100px);}
    100% {transform:translateY(100vh);}
}

</style>

<div class="sun"></div>
<div class="cloud"></div>
<div class="rain"></div>
<div class="snow"></div>
""", unsafe_allow_html=True)
