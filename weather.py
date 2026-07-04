import streamlit as st
import requests

st.set_page_config(page_title="날씨", layout="centered")

# =========================
# 날씨 데이터
# =========================
@st.cache_data(ttl=600)
def get_weather():
    url = "https://wttr.in/Bangbae-dong?format=j1"

    default = (22, "맑음", "15km", "보통", "05:32", "19:51")

    try:
        r = requests.get(url, timeout=5)
        data = r.json()

        cur = data["current_condition"][0]
        astro = data["weather"][0]["astronomy"][0]

        temp = int(cur["temp_C"])
        desc_en = cur["weatherDesc"][0]["value"].lower()

        visibility = cur.get("visibility", "15") + "km"
        humidity = int(cur["humidity"])

        # 🌫️ 미세먼지 (간이 계산)
        if humidity > 80:
            dust = "좋음 😄"
        elif humidity > 50:
            dust = "보통 😐"
        else:
            dust = "나쁨 😷"

        # 🌤️ 날씨 분류
        if "cloud" in desc_en:
            weather = "구름"
        elif "rain" in desc_en:
            weather = "비"
        elif "snow" in desc_en:
            weather = "눈"
        else:
            weather = "맑음"

        return temp, weather, visibility, dust, astro["sunrise"], astro["sunset"]

    except:
        return default


temp, weather, visibility, dust, sunrise, sunset = get_weather()

# =========================
# 🌈 날씨별 "감정 배경"
# =========================
theme = {
    "맑음": {
        "bg": "linear-gradient(to bottom, #74b9ff, #a29bfe)",
        "ground": "#2ecc71",
        "clouds": 1,
        "dark": 0
    },
    "구름": {
        "bg": "linear-gradient(to bottom, #636e72, #b2bec3)",
        "ground": "#27ae60",
        "clouds": 4,
        "dark": 1
    },
    "비": {
        "bg": "linear-gradient(to bottom, #2d3436, #636e72)",
        "ground": "#1e824c",
        "clouds": 3,
        "dark": 2
    },
    "눈": {
        "bg": "linear-gradient(to bottom, #dfe6e9, #ffffff)",
        "ground": "#ffffff",
        "clouds": 2,
        "dark": 0
    }
}[weather]

# =========================
# CSS
# =========================
st.markdown(f"""
<style>

html, body, [data-testid="stAppViewContainer"] {{
    background: {theme["bg"]};
}}

/* 🌍 땅 */
.ground {{
    position: fixed;
    bottom: 0;
    width: 100%;
    height: 200px;
    background: {theme["ground"]};
    border-top-left-radius: 80px;
    border-top-right-radius: 80px;
    z-index: 0;
}}

/* ☁️ 구름 */
.cloud {{
    position: fixed;
    top: 120px;
    width: 120px;
    height: 40px;
    background: white;
    border-radius: 50px;
    opacity: 0.9;
    animation: move 30s linear infinite;
    z-index: 1;
}}

@keyframes move {{
    0% {{ left: -150px; }}
    100% {{ left: 110%; }}
}}

/* 🌧️ 비 */
.rain {{
    position: fixed;
    width: 2px;
    height: 15px;
    background: #74b9ff;
    animation: fall 1s linear infinite;
    z-index: 1;
}}

@keyframes fall {{
    0% {{ top: -20px; }}
    100% {{ top: 100vh; }}
}}

/* 🌫️ 어두움 오버레이 */
.dark {{
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0,0,0,{theme["dark"] * 0.15});
    z-index: 0;
}}

/* 카드 */
.card {{
    background: white;
    padding: 18px;
    border-radius: 15px;
    margin-top: 20px;
    position: relative;
    z-index: 5;
}}

.grid {{
    display: flex;
    gap: 10px;
}}

.box {{
    flex: 1;
    background: #f1f2f6;
    padding: 10px;
    border-radius: 10px;
    text-align: center;
}}

</style>
""", unsafe_allow_html=True)

# =========================
# 배경 요소 출력
# =========================
st.markdown("<div class='ground'></div>", unsafe_allow_html=True)
st.markdown("<div class='dark'></div>", unsafe_allow_html=True)

# 구름 개수 조절
for _ in range(theme["clouds"]):
    st.markdown("<div class='cloud'></div>", unsafe_allow_html=True)

# 비는 비일 때만
if weather == "비":
    for _ in range(8):
        st.markdown("<div class='rain'></div>", unsafe_allow_html=True)
        st.title("🌤️ 방배동 날씨")

st.markdown(f"""
<div class="card">
<h2>현재 온도: {temp}°C</h2>
<p>상태: {weather}</p>
</div>
""", unsafe_allow_html=True)

# =========================
# 📊 인덱스 (완전 복구)
# =========================
st.markdown(f"""
<div class="card">

<h3>📊 기상 인덱스</h3>

<div class="grid">

<div class="box">
🌅<br><b>일출</b><br>{sunrise}
</div>

<div class="box">
🌇<br><b>일몰</b><br>{sunset}
</div>

<div class="box">
👁️<br><b>가시거리</b><br>{visibility}
</div>

<div class="box">
😷<br><b>미세먼지</b><br>{dust}
</div>

</div>

<p style="margin-top:10px; color:gray;">
👉 가시거리는 하늘 상태를 기반으로 체감 시야를 나타냅니다.
<br>
👉 미세먼지는 습도 기반으로 추정된 실시간 환경 지표입니다.
</p>

</div>
""", unsafe_allow_html=True)
