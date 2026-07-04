# =========================
# STEP 1 - DATA + STYLE
# =========================
import streamlit as st
import requests
from streamlit_lottie import st_lottie

st.set_page_config(page_title="Weather", layout="centered")

@st.cache_data(ttl=600)
def get_weather():
    url = "https://wttr.in/Bangbae-dong?format=j1"
    default = (22, "Clear", "맑음", "보통", "15km", "05:32", "19:51")

    try:
        r = requests.get(url, timeout=5)
        data = r.json()

        cur = data["current_condition"][0]
        astro = data["weather"][0]["astronomy"][0]

        temp = int(cur["temp_C"])
        desc_en = cur["weatherDesc"][0]["value"].lower()

        weather = "Clear"
        if "cloud" in desc_en:
            weather = "Clouds"
        elif "rain" in desc_en:
            weather = "Rain"
        elif "snow" in desc_en:
            weather = "Snow"

        return temp, weather, cur["weatherDesc"][0]["value"], astro["sunrise"], astro["sunset"]

    except:
        return default


temp, weather, desc, sunrise, sunset = get_weather()

theme = {
    "Clear": {
        "sky": "linear-gradient(to bottom, #74b9ff, #a29bfe)",
        "ground": "#55efc4",
    },
    "Clouds": {
        "sky": "linear-gradient(to bottom, #636e72, #b2bec3)",
        "ground": "#2ecc71",
    },
    "Rain": {
        "sky": "linear-gradient(to bottom, #2d3436, #636e72)",
        "ground": "#27ae60",
    },
    "Snow": {
        "sky": "linear-gradient(to bottom, #dfe6e9, #ffffff)",
        "ground": "#ffffff",
    }
}[weather]


st.markdown(f"""
<style>

/* 배경 */
html, body, [data-testid="stAppViewContainer"] {{
    background: {theme["sky"]};
}}

/* 땅 (고정) */
[data-testid="stAppViewContainer"]::after {{
    content:"";
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 220px;
    background: {theme["ground"]};
    border-radius: 60% 60% 0 0;
    z-index: -10;
}}

/* =======================
   오브젝트 (핵심 수정)
   absolute → fixed 과도 사용 금지
======================= */

.sun {{
    position: fixed;
    top: 80px;
    right: 80px;
    width: 80px;
    height: 80px;
    background: yellow;
    border-radius: 50%;
    z-index: 1;
}}

.cloud {{
    position: fixed;
    top: 120px;
    width: 120px;
    height: 40px;
    background: white;
    border-radius: 50px;
    z-index: 1;
    animation: move 25s linear infinite;
}}

@keyframes move {{
    0% {{ left: -150px; }}
    100% {{ left: 110%; }}
}}

/* 비 (Rain일 때만 보이게) */
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

/* 카드 */
.card {{
    background: white;
    padding: 20px;
    border-radius: 15px;
    margin-top: 20px;
    z-index: 10;
    position: relative;
}}

/* 인덱스 안정화 */
.grid {{
    display: flex;
    gap: 10px;
    justify-content: space-between;
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

# 오브젝트 출력 (중요)
if weather == "Clear":
    st.markdown("<div class='sun'></div>", unsafe_allow_html=True)
    st.markdown("<div class='cloud'></div>", unsafe_allow_html=True)

elif weather == "Clouds":
    st.markdown("<div class='cloud'></div>", unsafe_allow_html=True)

elif weather == "Rain":
    st.markdown("<div class='cloud'></div>", unsafe_allow_html=True)
    for i in range(10):
        st.markdown("<div class='rain'></div>", unsafe_allow_html=True)

elif weather == "Snow":
    st.markdown("<div class='cloud'></div>", unsafe_allow_html=True)
    # =========================
# STEP 2 - UI
# =========================

st.title("🌤️ 방배동 실시간 날씨")

st.markdown(f"""
<div class="card">
    <h2>현재 온도: {temp}°C</h2>
    <p>상태: {desc}</p>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="card">
    <h3>📊 기상 인덱스 설명</h3>

    <div class="grid">
        <div class="box">
            🌅<br><b>일출</b><br>{sunrise}
        </div>

        <div class="box">
            🌇<br><b>일몰</b><br>{sunset}
        </div>

        <div class="box">
            🌡️<br><b>기온 상태</b><br>
            {"따뜻함" if temp > 20 else "쌀쌀함"}
        </div>
    </div>

    <p style="margin-top:10px;">
    👉 이 인덱스는 체감 날씨 + 시각 정보를 종합해 보여줍니다.
    </p>
</div>
""", unsafe_allow_html=True)

# 코디
if temp > 28:
    style = "민소매 + 반바지"
elif temp > 20:
    style = "반팔 + 얇은 셔츠"
else:
    style = "후드 / 자켓"

st.markdown(f"""
<div class="card">
    <h3>👕 추천 코디</h3>
    <p>{style}</p>
</div>
""", unsafe_allow_html=True)
