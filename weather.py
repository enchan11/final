import streamlit as st
import requests
from datetime import datetime

st.set_page_config(
    page_title="방배동 날씨 월드 🌤️",
    page_icon="🌈",
    layout="centered"
)

# =========================
# 날씨 API
# =========================
@st.cache_data(ttl=600)
def get_weather():
    url = "https://wttr.in/Bangbae-dong?format=j1"

    # ✅ 반드시 9개 맞춤 (이게 핵심)
    default = (
        22,
        "Clear",
        "맑음",
        "기본 날씨 데이터입니다",
        "보통",
        "일반적인 공기 상태입니다",
        "15km",
        "05:32",
        "19:51"
    )

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

        # 공기질
        if humidity > 85:
            dust = "좋음"
            dust_desc = "공기가 매우 깨끗한 상태입니다"
        elif humidity > 40:
            dust = "보통"
            dust_desc = "일상 활동에 무리 없는 상태입니다"
        else:
            dust = "나쁨"
            dust_desc = "건조하거나 탁한 공기입니다"

        # 날씨
        weather = "Clear"
        weather_desc = "맑음"
        weather_detail = "하늘이 맑고 햇빛이 좋은 날씨입니다"

        if "cloud" in desc:
            weather = "Clouds"
            weather_desc = "구름 많음"
            weather_detail = "구름이 하늘을 덮고 있습니다"
        elif "rain" in desc:
            weather = "Rain"
            weather_desc = "비"
            weather_detail = "현재 비가 내리고 있습니다"
        elif "snow" in desc:
            weather = "Snow"
            weather_desc = "눈"
            weather_detail = "눈이 내리는 겨울 날씨입니다"

        return temp, weather, weather_desc, weather_detail, dust, dust_desc, visibility, sunrise, sunset

    except:
        return default


temp, weather_main, weather_desc, weather_detail, dust, dust_desc, visibility, sunrise, sunset = get_weather()

dust_color = "#2ed573" if dust in ["좋음", "보통"] else "#ff4757"

is_night = datetime.now().hour < 6 or datetime.now().hour > 18
st.markdown(f"""
<style>

/* =========================
   BACKGROUND
========================= */
[data-testid="stAppViewContainer"] {{
    background: {"#0b1a2f" if is_night else "#74b9ff"};
}}

/* =========================
   GROUND
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
   OBJECT LAYER (완전 분리)
========================= */
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
    top: 140px;
    left: -200px;
    width: 120px;
    height: 40px;
    background: white;
    border-radius: 50px;
    animation: move 28s linear infinite;
}

@keyframes move {{
    from {{ left: -200px; }}
    to {{ left: 110%; }}
}}

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

/* =========================
   UI CARD (안정화 핵심)
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
    height: 95px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    text-align: center;
}}

.small {{
    font-size: 12px;
    color: #636e72;
    margin-top: 4px;
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
# 배경 오브젝트
# =========================
if is_night:
    st.markdown('<div class="moon"></div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="sun"></div>', unsafe_allow_html=True)

st.markdown('<div class="cloud"></div>', unsafe_allow_html=True)

if weather_main == "Rain":
    st.markdown('<div class="rain"></div>', unsafe_allow_html=True)


# =========================
# UI
# =========================
st.markdown("<div class='title'>🌤 방배동 날씨 월드</div>", unsafe_allow_html=True)

st.markdown(f"""
<div class="card">
<h2>🌡 현재 {temp}°C / {weather_desc}</h2>
<p class="small">{weather_detail}</p>
</div>
""", unsafe_allow_html=True)


# =========================
# 인덱스 (완전 업그레이드)
# =========================
st.markdown(f"""
<div class="card">
<h3 style="text-align:center;">📊 기상 인덱스</h3>

<div class="grid">

    <div class="box">
        🌅 일출
        <div>{sunrise}</div>
        <div class="small">하루가 시작되는 시간</div>
    </div>

    <div class="box">
        🌇 일몰
        <div>{sunset}</div>
        <div class="small">하루가 끝나는 시간</div>
    </div>

    <div class="box">
        😷 대기
        <div style="color:{dust_color}; font-weight:bold;">{dust}</div>
        <div class="small">{dust_desc}</div>
    </div>

    <div class="box">
        👁 가시거리
        <div>{visibility}</div>
        <div class="small">시야 확보 상태</div>
    </div>

</div>
</div>
""", unsafe_allow_html=True)


# =========================
# 코디 추천 (업그레이드)
# =========================
style = ""
if temp >= 28:
    style = "민소매 + 반바지"
elif temp >= 23:
    style = "반팔 + 가벼운 바지"
elif temp >= 17:
    style = "긴팔 + 얇은 외투"
else:
    style = "두꺼운 외투 필수"

st.markdown(f"""
<div class="card">
👗 오늘의 코디 추천<br><br>
<b>{style}</b>
</div>
""", unsafe_allow_html=True)
