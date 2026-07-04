import streamlit as st
import requests
from datetime import datetime

st.set_page_config(
    page_title="방배동 날씨 월드",
    page_icon="🌤️",
    layout="centered"
)

# =========================
# 날씨 데이터
# =========================
@st.cache_data(ttl=600)
def get_weather():
    url = "https://wttr.in/Bangbae-dong?format=j1"
    default = (22, "Clear", "맑음", "보통", "15km", "05:32", "19:51")

    try:
        data = requests.get(url, timeout=5).json()

        cur = data["current_condition"][0]
        astro = data["weather"][0]["astronomy"][0]

        temp = int(float(cur["temp_C"]))
        desc = cur["weatherDesc"][0]["value"].lower()
        humidity = int(cur["humidity"])
        visibility = cur["visibility"] + "km"

        sunrise = astro["sunrise"]
        sunset = astro["sunset"]

        # 대기
        if humidity > 85:
            dust = "좋음"
        elif humidity > 40:
            dust = "보통"
        else:
            dust = "나쁨"

        # 날씨
        weather = "Clear"
        if "cloud" in desc:
            weather = "Clouds"
        elif "rain" in desc:
            weather = "Rain"
        elif "snow" in desc:
            weather = "Snow"

        return temp, weather, desc, dust, visibility, sunrise, sunset

    except:
        return default


temp, weather_main, weather_desc, dust, visibility, sunrise, sunset = get_weather()

dust_color = "#2ed573" if dust in ["좋음", "보통"] else "#ff4757"


# =========================
# 낮/밤 판단 (진짜 버전)
# =========================
def is_night_time():
    now = datetime.now().hour
    return now < 6 or now > 18

is_night = is_night_time()
st.markdown(f"""
<style>

/* =========================
   BACKGROUND
========================= */
html, body {{
    margin: 0;
    padding: 0;
}}

[data-testid="stAppViewContainer"] {{
    background: {"#0b1a2f" if is_night else "#74b9ff"};
    position: relative;
}}

/* =========================
   GROUND (절대 고정)
========================= */
[data-testid="stAppViewContainer"]::after {{
    content: "";
    position: fixed;
    bottom: -120px;
    left: 0;
    width: 100%;
    height: 260px;
    background: {"#1e5631" if is_night else "#55efc4"};
    border-radius: 50% 50% 0 0;
    z-index: 0;
}}

/* =========================
   OBJECT LAYER (완전 fixed)
========================= */
.layer {{
    position: fixed;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: 0;
}}

.sun {{
    position: fixed;
    top: 80px;
    right: 80px;
    width: 80px;
    height: 80px;
    background: radial-gradient(circle,#ffeaa7,#fdcb6e);
    border-radius: 50%;
}}

.moon {{
    position: fixed;
    top: 80px;
    right: 80px;
    width: 70px;
    height: 70px;
    background: #f1f2f6;
    border-radius: 50%;
}}

.cloud {{
    position: fixed;
    top: 120px;
    left: -200px;
    width: 120px;
    height: 40px;
    background: white;
    border-radius: 50px;
    animation: move 30s linear infinite;
}}

@keyframes move {{
    from {{ left: -200px; }}
    to {{ left: 110%; }}
}}

/* 비 */
.rain {{
    position: fixed;
    width: 2px;
    height: 18px;
    background: #74b9ff;
    animation: fall 1s linear infinite;
}}

@keyframes fall {{
    0% {{ transform: translateY(-10%); }}
    100% {{ transform: translateY(110vh); }}
}}

/* 눈 */
.snow {{
    position: fixed;
    width: 6px;
    height: 6px;
    background: white;
    border-radius: 50%;
    animation: fall 3s linear infinite;
}}

/* =========================
   UI (절대 안정)
========================= */
.card {{
    background: white;
    border-radius: 16px;
    padding: 18px;
    margin-top: 14px;
    box-shadow: 0 6px 25px rgba(0,0,0,0.1);
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
    border-radius: 12px;
    height: 85px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    text-align: center;
}}

.title {{
    text-align: center;
    font-size: 26px;
    font-weight: bold;
    color: white;
}}

</style>
""", unsafe_allow_html=True)


# =========================
# 3. 배경 렌더링 (완전 조건 분리)
# =========================
st.markdown('<div class="layer">', unsafe_allow_html=True)

if is_night:
    st.markdown('<div class="moon"></div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="sun"></div>', unsafe_allow_html=True)

st.markdown('<div class="cloud"></div>', unsafe_allow_html=True)

if weather_main == "Rain":
    st.markdown('<div class="rain"></div>', unsafe_allow_html=True)

if weather_main == "Snow":
    st.markdown('<div class="snow"></div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)


# =========================
# 4. UI
# =========================
st.markdown("<div class='title'>🌤 방배동 날씨 월드</div>", unsafe_allow_html=True)

st.markdown(f"""
<div class="card">
<h2>🌡 {temp}°C / {weather_desc}</h2>
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
👗 코디 추천<br><br>
<b>{
"반팔 OK" if temp > 23 else "겉옷 필수"
}</b>
</div>
""", unsafe_allow_html=True)
