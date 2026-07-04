# =========================
# 1단계: weather_engine.py
# =========================

import requests
import streamlit as st

@st.cache_data(ttl=600)
def get_weather():
    url = "https://wttr.in/Bangbae-dong?format=j1"

    try:
        r = requests.get(url, timeout=5)
        data = r.json()

        current = data["current_condition"][0]
        astro = data["weather"][0]["astronomy"][0]

        temp = int(current["temp_C"])
        desc_en = current["weatherDesc"][0]["value"].lower()
        humidity = int(current["humidity"])
        visibility = int(current["visibility"])

        sunrise = astro["sunrise"]
        sunset = astro["sunset"]

        # 🌫️ 미세먼지 (대체 로직)
        if humidity > 80:
            dust = "좋음"
        elif humidity > 50:
            dust = "보통"
        else:
            dust = "나쁨"

        # 🌤️ 날씨 분류
        if "rain" in desc_en or "shower" in desc_en:
            weather = "Rain"
        elif "snow" in desc_en:
            weather = "Snow"
        elif "cloud" in desc_en or "overcast" in desc_en:
            weather = "Clouds"
        else:
            weather = "Clear"

        return temp, weather, humidity, dust, visibility, sunrise, sunset

    except:
        return 22, "Clear", 60, "보통", 15, "06:00", "19:00"
        # =========================
# 2단계: app.py
# =========================

import streamlit as st
from streamlit_lottie import st_lottie
import requests
from weather_engine import get_weather

st.set_page_config(page_title="날씨 시뮬레이터", layout="centered")

temp, weather, humidity, dust, visibility, sunrise, sunset = get_weather()

# 🌈 밝기 자동 조절 (핵심: 흐리면 어두워짐)
brightness = {
    "Clear": "1",
    "Clouds": "0.75",
    "Rain": "0.6",
    "Snow": "0.85"
}.get(weather, "1")

# 🌤️ 배경
sky = {
    "Clear": "linear-gradient(#74b9ff, #a29bfe)",
    "Clouds": "linear-gradient(#636e72, #b2bec3)",
    "Rain": "linear-gradient(#2d3436, #636e72)",
    "Snow": "linear-gradient(#dfe6e9, #ffffff)"
}.get(weather)

# 🌿 땅
ground_color = {
    "Clear": "#55efc4",
    "Clouds": "#a4b0be",
    "Rain": "#2ecc71",
    "Snow": "#ffffff"
}.get(weather)

# 🌤️ 오브젝트 (중요: 절대 fixed + top 제한)
objects = {
    "Clear": """
        <div class='sun'></div>
        <div class='cloud c1'></div>
    """,
    "Clouds": """
        <div class='cloud c1'></div>
        <div class='cloud c2'></div>
    """,
    "Rain": """
        <div class='cloud c1'></div>
        <div class='rain r1'></div>
        <div class='rain r2'></div>
    """,
    "Snow": """
        <div class='cloud c1'></div>
        <div class='snow s1'></div>
    """
}.get(weather)

# ================= CSS =================
st.markdown(f"""
<style>

html, body {{
    background: {sky};
    filter: brightness({brightness});
}}

.weather-card {{
    background: white;
    padding: 20px;
    border-radius: 20px;
    margin-top: 20px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
}}

.ground {{
    position: fixed;
    bottom: 0;
    width: 100%;
    height: 180px;
    background: {ground_color};
    border-radius: 50% 50% 0 0;
    z-index: -1;
}}

/* ===== 하늘 제한 영역 (핵심 수정) ===== */
.sky-layer {{
    position: fixed;
    top: 0;
    width: 100%;
    height: 60vh;
    overflow: hidden;
    pointer-events: none;
}}

/* ===== 태양 ===== */
.sun {{
    position: absolute;
    top: 60px;
    right: 80px;
    width: 70px;
    height: 70px;
    background: yellow;
    border-radius: 50%;
    box-shadow: 0 0 30px yellow;
}}

/* ===== 구름 ===== */
.cloud {{
    position: absolute;
    width: 120px;
    height: 40px;
    background: white;
    border-radius: 50px;
    opacity: 0.8;
}}

.c1 {{ top: 80px; left: -150px; animation: move 25s linear infinite; }}
.c2 {{ top: 140px; left: -200px; animation: move 35s linear infinite; }}

@keyframes move {{
    0% {{ transform: translateX(0); }}
    100% {{ transform: translateX(120vw); }}
}}

/* ===== 비 ===== */
.rain {{
    position: absolute;
    width: 2px;
    height: 15px;
    background: #74b9ff;
    animation: fall 1s linear infinite;
}}

.r1 {{ left: 30%; top: 0; }}
.r2 {{ left: 60%; top: 0; animation-delay: 0.5s; }}

@keyframes fall {{
    0% {{ transform: translateY(0); }}
    100% {{ transform: translateY(60vh); }}
}}

/* ===== 눈 ===== */
.snow {{
    position: absolute;
    width: 6px;
    height: 6px;
    background: white;
    border-radius: 50%;
    animation: snow 3s linear infinite;
}}

.s1 {{ left: 50%; top: 0; }}

@keyframes snow {{
    0% {{ transform: translateY(0); }}
    100% {{ transform: translateY(60vh); }}
}}

</style>
""", unsafe_allow_html=True)

# ================= UI =================
st.markdown("<div class='ground'></div>", unsafe_allow_html=True)
st.markdown(f"<div class='sky-layer'>{objects}</div>", unsafe_allow_html=True)

st.title("🌤️ 방배동 날씨 시뮬레이터")

st.markdown(f"""
<div class='weather-card'>
    <h2>{temp}°C</h2>
    <p>미세먼지: {dust} / 습도: {humidity}%</p>
    <p>가시거리: {visibility} km</p>
    <p>일출: {sunrise} / 일몰: {sunset}</p>
</div>
""", unsafe_allow_html=True)
