import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="Weather World", layout="centered")

# =========================
# 날씨 API
# =========================
@st.cache_data(ttl=600)
def get_weather():
    url = "https://wttr.in/Bangbae-dong?format=j1"

    try:
        r = requests.get(url, timeout=5)
        data = r.json()

        cur = data["current_condition"][0]
        astro = data["weather"][0]["astronomy"][0]

        temp = int(cur["temp_C"])
        desc = cur["weatherDesc"][0]["value"].lower()
        humidity = int(cur["humidity"])
        visibility = int(cur.get("visibility", 15))

        # 날씨 분류
        if "rain" in desc:
            weather = "비"
        elif "cloud" in desc:
            weather = "구름"
        elif "snow" in desc:
            weather = "눈"
        else:
            weather = "맑음"

        # 미세먼지 (간이)
        if humidity > 80:
            dust = "좋음 😄"
        elif humidity > 50:
            dust = "보통 😐"
        else:
            dust = "나쁨 😷"

        return temp, weather, visibility, dust, astro["sunrise"], astro["sunset"]

    except:
        return 22, "맑음", 15, "보통 😐", "05:32", "19:51"


temp, weather, visibility, dust, sunrise, sunset = get_weather()

# =========================
# ⏰ 시간 기반 분위기
# =========================
hour = datetime.now().hour

if 5 <= hour < 8:
    sky = "linear-gradient(to bottom, #6c5ce7, #a29bfe)"  # 새벽
elif 8 <= hour < 17:
    sky = "linear-gradient(to bottom, #74b9ff, #81ecec)"  # 낮
elif 17 <= hour < 19:
    sky = "linear-gradient(to bottom, #fdcb6e, #e17055)"  # 노을
else:
    sky = "linear-gradient(to bottom, #2d3436, #000000)"  # 밤

st.markdown(f"""
<style>

/* 🌍 배경 */
html, body, [data-testid="stAppViewContainer"] {{
    background: {sky};
}}

/* 🌫️ 미세먼지 오버레이 */
.haze {{
    position: fixed;
    top:0;
    left:0;
    width:100%;
    height:100%;
    background: rgba(255,255,255,
        {"0.05" if "좋음" in dust else "0.12" if "보통" in dust else "0.25"}
    );
    z-index: 0;
}}

/* 🌍 땅 */
.ground {{
    position: fixed;
    bottom:0;
    width:100%;
    height:200px;
    background: linear-gradient(to top, #27ae60, #2ecc71);
    border-top-left-radius:80px;
    border-top-right-radius:80px;
    z-index: 1;
}}

/* ☁️ 구름 */
.cloud {{
    position: fixed;
    width:120px;
    height:40px;
    background:white;
    border-radius:50px;
    animation: move 30s linear infinite;
}}

@keyframes move {{
    0% {{ left:-150px; }}
    100% {{ left:110%; }}
}}

/* 🌧️ 비 */
.rain {{
    position: fixed;
    width:2px;
    height:15px;
    background:#74b9ff;
    animation: fall 1s linear infinite;
}}

@keyframes fall {{
    0% {{ top:-20px; }}
    100% {{ top:100vh; }}
}}

/* 카드 */
.card {{
    background:white;
    padding:18px;
    border-radius:15px;
    margin-top:20px;
    position:relative;
    z-index:5;
}}

.grid {{
    display:flex;
    gap:10px;
}}

.box {{
    flex:1;
    background:#f1f2f6;
    padding:10px;
    border-radius:10px;
    text-align:center;
}}

</style>
""", unsafe_allow_html=True)

# =========================
# 렌더링
# =========================
st.markdown("<div class='haze'></div>", unsafe_allow_html=True)
st.markdown("<div class='ground'></div>", unsafe_allow_html=True)

if weather == "맑음":
    st.markdown("<div class='cloud'></div>", unsafe_allow_html=True)

elif weather == "구름":
    for _ in range(3):
        st.markdown("<div class='cloud'></div>", unsafe_allow_html=True)

elif weather == "비":
    for _ in range(6):
        st.markdown("<div class='cloud'></div>", unsafe_allow_html=True)
        st.markdown("<div class='rain'></div>", unsafe_allow_html=True)

elif weather == "눈":
    st.markdown("<div class='cloud'></div>", unsafe_allow_html=True)
    
st.title("🌤️ Weather World - 방배동")

st.markdown(f"""
<div class="card">
<h2>{temp}°C · {weather}</h2>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="card">

<h3>📊 기상 인덱스</h3>

<div class="grid">

<div class="box">🌅<br><b>일출</b><br>{sunrise}</div>
<div class="box">🌇<br><b>일몰</b><br>{sunset}</div>
<div class="box">👁️<br><b>가시거리</b><br>{visibility} km</div>
<div class="box">😷<br><b>미세먼지</b><br>{dust}</div>

</div>

<p style="margin-top:10px; color:gray;">
👉 하늘 상태 + 습도 + 시간 기반으로 계산된 실시간 환경 지표입니다.
</p>

</div>
""", unsafe_allow_html=True)

# 코디
if temp >= 28:
    outfit = "민소매 + 반바지"
elif temp >= 20:
    outfit = "반팔 + 셔츠"
else:
    outfit = "후드 / 자켓"

st.markdown(f"""
<div class="card">
<h3>👕 코디 추천</h3>
<p>{outfit}</p>
</div>
""", unsafe_allow_html=True)
