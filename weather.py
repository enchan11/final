import streamlit as st
import requests

# =========================
# 1. 기본 설정
# =========================
st.set_page_config(page_title="방배동 3D 날씨 월드", layout="centered")

st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# =========================
# 2. 날씨 데이터
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

        # 미세먼지 (대체 로직)
        if humidity > 80:
            dust = "좋음"
        elif humidity > 50:
            dust = "보통"
        else:
            dust = "나쁨"

        # 날씨 분류
        if "rain" in desc:
            weather = "Rain"
        elif "snow" in desc:
            weather = "Snow"
        elif "cloud" in desc or "overcast" in desc:
            weather = "Clouds"
        else:
            weather = "Clear"

        return temp, weather, humidity, dust, visibility, sunrise, sunset

    except:
        return 22, "Clear", 60, "보통", 15, "06:00", "19:00"


temp, weather, humidity, dust, visibility, sunrise, sunset = get_weather()


# =========================
# 3. 테마
# =========================
sky_color = {
    "Clear": "#74b9ff",
    "Clouds": "#636e72",
    "Rain": "#2d3436",
    "Snow": "#dfe6e9"
}.get(weather)

ground_color = {
    "Clear": "#2ecc71",
    "Clouds": "#95a5a6",
    "Rain": "#27ae60",
    "Snow": "#ffffff"
}.get(weather)


# =========================
# 4. 오브젝트 생성
# =========================
obj = ""

if weather == "Clear":
    obj = """
    <div class='sun'></div>
    <div class='cloud c1'></div>
    <div class='cloud c2'></div>
    """

elif weather == "Clouds":
    obj = """
    <div class='cloud c1'></div>
    <div class='cloud c2'></div>
    """

elif weather == "Rain":
    obj = """
    <div class='cloud c1'></div>
""" + "".join(
        f"<div class='rain' style='left:{i*10}%; animation-delay:{i*0.2}s'></div>"
        for i in range(12)
    )

elif weather == "Snow":
    obj = """
    <div class='cloud c1'></div>
""" + "".join(
        f"<div class='snow' style='left:{i*8}%; animation-delay:{i*0.3}s'></div>"
        for i in range(12)
    )


# =========================
# 5. CSS (완전 안정 레이어 구조)
# =========================
st.markdown(f"""
<style>

/* ===== 전체 캔버스 ===== */
.scene {{
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: -10;
    pointer-events: none;
}}

/* ===== 하늘 ===== */
.sky {{
    position: absolute;
    width: 100%;
    height: 70vh;
    background: {sky_color};
}}

/* ===== 땅 (3D 언덕) ===== */
.ground {{
    position: absolute;
    bottom: -120px;
    width: 140%;
    height: 300px;
    left: -20%;
    background: {ground_color};
    border-radius: 50%;
    box-shadow: inset 0 20px 40px rgba(0,0,0,0.15);
}}

/* ===== 태양 ===== */
.sun {{
    position: absolute;
    top: 60px;
    right: 80px;
    width: 80px;
    height: 80px;
    background: radial-gradient(circle, #fff200, #ffa502);
    border-radius: 50%;
    box-shadow: 0 0 50px #ffa502;
}}

/* ===== 구름 ===== */
.cloud {{
    position: absolute;
    width: 140px;
    height: 50px;
    background: white;
    border-radius: 50px;
    opacity: 0.85;
    animation: move 30s linear infinite;
}}

.c1 {{ top: 80px; left: -200px; }}
.c2 {{ top: 150px; left: -300px; animation-delay: 5s; }}

@keyframes move {{
    0% {{ transform: translateX(0); }}
    100% {{ transform: translateX(120vw); }}
}}

/* ===== 비 ===== */
.rain {{
    position: absolute;
    width: 2px;
    height: 18px;
    background: #74b9ff;
    animation: fall 0.8s linear infinite;
}}

@keyframes fall {{
    0% {{ transform: translateY(-20px); }}
    100% {{ transform: translateY(100vh); }}
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

@keyframes snow {{
    0% {{ transform: translateY(-20px); }}
    100% {{ transform: translateY(100vh); }}
}}

/* ===== 카드 (최상단 고정) ===== */
.card {{
    position: relative;
    z-index: 10;
    background: white;
    padding: 22px;
    border-radius: 20px;
    margin-top: 25px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.15);
}}

</style>
""", unsafe_allow_html=True)


# =========================
# 6. 렌더링 구조 (핵심)
# =========================
st.markdown(f"""
<div class='scene'>
    <div class='sky'></div>
    {obj}
    <div class='ground'></div>
</div>
""", unsafe_allow_html=True)


# =========================
# 7. UI
# =========================
st.title("🌤️ 방배동 3D 날씨 월드")

st.markdown(f"""
<div class='card'>
<h2>🌡️ {temp}°C</h2>
<p>날씨: {weather}</p>
<p>미세먼지: {dust}</p>
<p>습도: {humidity}%</p>
<p>가시거리: {visibility} km</p>
<p>일출: {sunrise} / 일몰: {sunset}</p>
</div>
""", unsafe_allow_html=True)
