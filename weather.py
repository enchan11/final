import streamlit as st
import requests
import random

st.set_page_config(page_title="3D 날씨 시뮬레이터", layout="centered")

# =========================
# 1. 날씨 데이터
# =========================
@st.cache_data(ttl=600)
def get_weather():
    url = "https://wttr.in/Bangbae-dong?format=j1"

    try:
        data = requests.get(url, timeout=5).json()

        current = data["current_condition"][0]
        astro = data["weather"][0]["astronomy"][0]

        temp = int(current["temp_C"])
        desc = current["weatherDesc"][0]["value"].lower()
        humidity = int(current["humidity"])
        visibility = int(current["visibility"])

        sunrise = astro["sunrise"]
        sunset = astro["sunset"]

        if humidity > 80:
            dust = "좋음"
        elif humidity > 50:
            dust = "보통"
        else:
            dust = "나쁨"

        if "rain" in desc:
            weather = "Rain"
        elif "snow" in desc:
            weather = "Snow"
        elif "cloud" in desc:
            weather = "Clouds"
        else:
            weather = "Clear"

        return temp, weather, humidity, dust, visibility, sunrise, sunset

    except:
        return 22, "Clear", 60, "보통", 15, "06:00", "19:00"


temp, weather, humidity, dust, visibility, sunrise, sunset = get_weather()

# =========================
# 2. 테마
# =========================
sky = {
    "Clear": "#74b9ff",
    "Clouds": "#636e72",
    "Rain": "#2d3436",
    "Snow": "#dfe6e9"
}.get(weather)

ground = {
    "Clear": "#2ecc71",
    "Clouds": "#95a5a6",
    "Rain": "#27ae60",
    "Snow": "#ffffff"
}.get(weather)

# =========================
# 3. CSS (3D + 움직임 핵심)
# =========================
st.markdown(f"""
<style>

body {{
    background: {sky};
    overflow-x: hidden;
}}

/* =======================
   🌄 3D 땅 (언덕)
======================= */
.ground {{
    position: fixed;
    bottom: -120px;
    width: 140%;
    height: 300px;
    left: -20%;
    background: {ground};
    border-radius: 50%;
    z-index: -1;
    box-shadow: inset 0 20px 40px rgba(0,0,0,0.1);
    animation: groundMove 6s ease-in-out infinite alternate;
}}

@keyframes groundMove {{
    0% {{ transform: scale(1); }}
    100% {{ transform: scale(1.03); }}
}}

/* =======================
   ☁️ 구름 (부드러운 이동)
======================= */
.cloud {{
    position: fixed;
    width: 140px;
    height: 50px;
    background: white;
    border-radius: 50px;
    opacity: 0.85;
    filter: blur(0.2px);
    animation: cloudMove 25s linear infinite;
}}

.cloud::before,
.cloud::after {{
    content: "";
    position: absolute;
    background: white;
    border-radius: 50%;
}}

.cloud::before {{
    width: 60px;
    height: 60px;
    top: -25px;
    left: 20px;
}}

.cloud::after {{
    width: 80px;
    height: 80px;
    top: -35px;
    right: 20px;
}}

@keyframes cloudMove {{
    0% {{ transform: translateX(-200px); }}
    100% {{ transform: translateX(120vw); }}
}}

/* =======================
   ☀️ 태양 (3D 느낌 회전)
======================= */
.sun {{
    position: fixed;
    top: 60px;
    right: 80px;
    width: 80px;
    height: 80px;
    background: radial-gradient(circle, #fff200, #ffa502);
    border-radius: 50%;
    box-shadow: 0 0 50px #ffa502;
    animation: sunPulse 3s ease-in-out infinite;
}}

@keyframes sunPulse {{
    0% {{ transform: scale(1); }}
    50% {{ transform: scale(1.1); }}
    100% {{ transform: scale(1); }}
}}

/* =======================
   🌧️ 비 (진짜 떨어지는 느낌)
======================= */
.rain {{
    position: fixed;
    width: 2px;
    height: 18px;
    background: #74b9ff;
    animation: rainFall 0.8s linear infinite;
    opacity: 0.7;
}}

@keyframes rainFall {{
    0% {{ transform: translateY(-20px); }}
    100% {{ transform: translateY(100vh); }}
}}

/* =======================
   ❄️ 눈
======================= */
.snow {{
    position: fixed;
    width: 6px;
    height: 6px;
    background: white;
    border-radius: 50%;
    animation: snowFall 3s linear infinite;
}}

@keyframes snowFall {{
    0% {{ transform: translateY(-20px) translateX(0); }}
    100% {{ transform: translateY(100vh) translateX(30px); }}
}}

/* =======================
   📦 카드 (고정 + 안정)
======================= */
.card {{
    background: white;
    padding: 22px;
    border-radius: 20px;
    margin-top: 30px;
    box-shadow: 0 15px 40px rgba(0,0,0,0.15);
    position: relative;
    z-index: 10;
}}

/* =======================
   🌫️ 흐림 효과 (Cloudy)
======================= */
.blur {{
    filter: brightness(0.8);
}}

</style>
""", unsafe_allow_html=True)

# =========================
# 4. 오브젝트 생성
# =========================
obj = ""

if weather == "Clear":
    obj = """
    <div class='sun'></div>
    <div class='cloud' style='top:80px;'></div>
    """

elif weather == "Clouds":
    obj = """
    <div class='cloud' style='top:80px;'></div>
    <div class='cloud' style='top:140px; animation-delay:5s'></div>
    """

elif weather == "Rain":
    obj = """
    <div class='cloud' style='top:80px'></div>
""" + "".join(
        f"<div class='rain' style='left:{i*10}%; animation-delay:{i*0.2}s'></div>"
        for i in range(10)
    )

elif weather == "Snow":
    obj = """
    <div class='cloud' style='top:80px'></div>
""" + "".join(
        f"<div class='snow' style='left:{i*8}%; animation-delay:{i*0.3}s'></div>"
        for i in range(12)
    )

# =========================
# 5. UI 출력
# =========================
st.markdown("<div class='ground'></div>", unsafe_allow_html=True)
st.markdown(f"<div>{obj}</div>", unsafe_allow_html=True)

st.title("🌤️ 3D 방배동 날씨 월드")

st.markdown(f"""
<div class='card'>
<h2>{temp}°C</h2>
<p>날씨: {weather}</p>
<p>미세먼지: {dust}</p>
<p>습도: {humidity}%</p>
<p>가시거리: {visibility} km</p>
<p>일출: {sunrise} / 일몰: {sunset}</p>
</div>
""", unsafe_allow_html=True)
