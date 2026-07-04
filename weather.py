import streamlit as st
import requests

st.set_page_config(page_title="날씨", layout="centered")

# =========================
# 날씨 데이터
# =========================
@st.cache_data(ttl=600)
def get_weather():
    url = "https://wttr.in/Bangbae-dong?format=j1"
    default = (22, "맑음", "맑음", "보통", "15km", "05:32", "19:51")

    try:
        r = requests.get(url, timeout=5)
        data = r.json()

        cur = data["current_condition"][0]
        astro = data["weather"][0]["astronomy"][0]

        temp = int(cur["temp_C"])
        desc_en = cur["weatherDesc"][0]["value"].lower()

        # 🌤️ 영어 → 한글 변환 (핵심 수정)
        if "cloud" in desc_en:
            weather = "구름"
        elif "rain" in desc_en:
            weather = "비"
        elif "snow" in desc_en:
            weather = "눈"
        else:
            weather = "맑음"

        return temp, weather, astro["sunrise"], astro["sunset"]

    except:
        return default


temp, weather, sunrise, sunset = get_weather()

# =========================
# CSS (땅 포함 완전 안정)
# =========================
st.markdown(f"""
<style>

/* 배경 */
html, body, [data-testid="stAppViewContainer"] {{
    background: linear-gradient(to bottom, #74b9ff, #a29bfe);
}}

/* =========================
   🌍 진짜 "땅바닥"
========================= */
.ground {{
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 180px;
    background: linear-gradient(to top, #2ecc71, #27ae60);
    border-top-left-radius: 80px;
    border-top-right-radius: 80px;
    box-shadow: 0 -10px 30px rgba(0,0,0,0.2);
    z-index: 0;
}}

/* 태양 */
.sun {{
    position: fixed;
    top: 60px;
    right: 60px;
    width: 80px;
    height: 80px;
    background: #ffe066;
    border-radius: 50%;
    box-shadow: 0 0 40px #ffe066;
    z-index: 1;
}}

/* 구름 */
.cloud {{
    position: fixed;
    top: 120px;
    width: 120px;
    height: 40px;
    background: white;
    border-radius: 50px;
    animation: move 25s linear infinite;
    z-index: 1;
}}

@keyframes move {{
    0% {{ left: -150px; }}
    100% {{ left: 110%; }}
}}

/* 카드 */
.card {{
    background: white;
    padding: 18px;
    border-radius: 15px;
    margin-top: 20px;
    position: relative;
    z-index: 5;
    box-shadow: 0 5px 20px rgba(0,0,0,0.1);
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

if weather == "맑음":
    st.markdown("<div class='sun'></div>", unsafe_allow_html=True)
    st.markdown("<div class='cloud'></div>", unsafe_allow_html=True)

elif weather == "구름":
    st.markdown("<div class='cloud'></div>", unsafe_allow_html=True)
    st.title("🌤️ 방배동 날씨")

# =========================
# 현재 날씨 카드
# =========================
st.markdown(f"""
<div class="card">
    <h2>현재 온도: {temp}°C</h2>
    <p>상태: {weather}</p>
</div>
""", unsafe_allow_html=True)

# =========================
# 📊 기상 인덱스 (완전 한글화)
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
🌡️<br><b>체감</b><br>
{"따뜻함 ☀️" if temp >= 23 else "선선함 🍃" if temp >= 15 else "추움 ❄️"}
</div>

</div>

<p style="margin-top:10px; color:gray;">
👉 이 인덱스는 실제 체감 날씨와 시간 정보를 기반으로 계산됩니다.
</p>

</div>
""", unsafe_allow_html=True)

# =========================
# 코디 추천
# =========================
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
