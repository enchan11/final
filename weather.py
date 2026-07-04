import streamlit as st
import requests
from streamlit_lottie import st_lottie

st.set_page_config(
    page_title="방배동 날씨 세계 🌤️",
    page_icon="🌈",
    layout="centered"
)

# =========================
# 1. 날씨 데이터
# =========================
@st.cache_data(ttl=600)
def get_weather():
    url = "https://wttr.in/Bangbae-dong?format=j1"

    default = (22, "Clear", "맑음", "보통", "15km", "05:32", "19:51")

    try:
        res = requests.get(url, timeout=5)
        data = res.json()

        current = data["current_condition"][0]
        astro = data["weather"][0]["astronomy"][0]

        temp = int(float(current["temp_C"]))
        desc = current["weatherDesc"][0]["value"].lower()
        humidity = int(current["humidity"])
        visibility = current["visibility"] + "km"

        sunrise = astro["sunrise"]
        sunset = astro["sunset"]

        if humidity > 85:
            dust = "좋음"
        elif humidity > 40:
            dust = "보통"
        else:
            dust = "나쁨"

        weather_main = "Clear"
        if "cloud" in desc:
            weather_main = "Clouds"
        elif "rain" in desc:
            weather_main = "Rain"
        elif "snow" in desc:
            weather_main = "Snow"

        return temp, weather_main, desc, dust, visibility, sunrise, sunset

    except:
        return default


temp, weather_main, weather_desc, dust, visibility, sunrise, sunset = get_weather()

dust_color = "#2ed573" if dust in ["좋음", "보통"] else "#ff4757"


# =========================
# 2. 테마 (핵심)
# =========================
themes = {
    "Clear": {
        "sky": "#74b9ff",
        "ground": "#55efc4"
    },
    "Clouds": {
        "sky": "#a4b0be",
        "ground": "#2ed573"
    },
    "Rain": {
        "sky": "#2f3640",
        "ground": "#1dd1a1"
    },
    "Snow": {
        "sky": "#dfe6e9",
        "ground": "#ffffff"
    }
}

theme = themes.get(weather_main, themes["Clear"])
st.markdown(f"""
<style>

/* =========================
   배경 (절대 고정)
========================= */
html, body, [data-testid="stAppViewContainer"] {{
    background: {theme["sky"]};
    font-family: sans-serif;
}}

/* 땅 */
[data-testid="stAppViewContainer"]::after {{
    content: "";
    position: fixed;
    bottom: -120px;
    left: 0;
    width: 100%;
    height: 260px;
    background: {theme["ground"]};
    border-radius: 50% 50% 0 0;
    z-index: 0;
}}

/* =========================
   배경 오브젝트 (fixed)
========================= */
.sun {{
    position: fixed;
    top: 80px;
    right: 100px;
    width: 80px;
    height: 80px;
    background: radial-gradient(circle,#ffeaa7,#fdcb6e);
    border-radius: 50%;
    z-index: 0;
}}

.cloud {{
    position: fixed;
    top: 140px;
    left: -200px;
    width: 120px;
    height: 40px;
    background: white;
    border-radius: 50px;
    animation: move 25s linear infinite;
    z-index: 0;
}}

@keyframes move {{
    from {{ left: -200px; }}
    to {{ left: 110%; }}
}}

/* 비 (조건부만 보여야 함) */
.rain {{
    position: fixed;
    width: 2px;
    height: 20px;
    background: #74b9ff;
    animation: fall 1s linear infinite;
    z-index: 0;
}}

@keyframes fall {{
    0% {{ transform: translateY(-10%); }}
    100% {{ transform: translateY(110vh); }}
}}

/* =========================
   UI 카드 (절대 안정)
========================= */
.card {{
    background: white;
    border-radius: 16px;
    padding: 18px;
    margin-top: 15px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    position: relative;
    z-index: 10;
}}

.grid {{
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 10px;
}}

.box {{
    background: #f1f2f6;
    padding: 10px;
    border-radius: 12px;
    text-align: center;
    height: 80px;
    display: flex;
    flex-direction: column;
    justify-content: center;
}}

.title {{
    text-align: center;
    font-size: 26px;
    font-weight: bold;
}}

</style>
""", unsafe_allow_html=True)


# =========================
# 3. 배경 오브젝트 (핵심 수정)
# =========================
st.markdown('<div class="sun"></div>', unsafe_allow_html=True)
st.markdown('<div class="cloud"></div>', unsafe_allow_html=True)

# 👉 비는 "조건부"
if weather_main == "Rain":
    st.markdown('<div class="rain"></div>', unsafe_allow_html=True)


# =========================
# 4. UI
# =========================
st.markdown("<div class='title'>방배동 날씨</div>", unsafe_allow_html=True)

st.markdown(f"""
<div class="card">
<h2>🌡 현재 {temp}°C / {weather_desc}</h2>
</div>
""", unsafe_allow_html=True)


st.markdown(f"""
<div class="card">
<h3 style="text-align:center;">📊 기상 인덱스</h3>

<div class="grid">
    <div class="box">🌅<br>{sunrise}</div>
    <div class="box">🌇<br>{sunset}</div>
    <div class="box">😷<br>{dust}</div>
    <div class="box">👁<br>{visibility}</div>
</div>
</div>
""", unsafe_allow_html=True)


st.markdown(f"""
<div class="card">
👗 오늘 코디 추천<br><br>
<b>{ "여름 반팔" if temp > 23 else "겉옷 필수" }</b>
</div>
""", unsafe_allow_html=True)
