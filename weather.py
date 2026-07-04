import requests

def get_weather():
    url = "https://wttr.in/Bangbae-dong?format=j1"

    default = (22, "Clear", "맑음", "보통", "15km", "05:32", "19:51")

    try:
        r = requests.get(url, timeout=5)
        data = r.json()

        current = data["current_condition"][0]
        astro = data["weather"][0]["astronomy"][0]

        temp = round(float(current["temp_C"]))
        desc_en = current["weatherDesc"][0]["value"].lower()

        visibility = current["visibility"] + "km"
        humidity = int(current["humidity"])

        if humidity > 85:
            dust = "좋음"
        elif humidity > 40:
            dust = "보통"
        else:
            dust = "나쁨"

        sunrise = astro["sunrise"]
        sunset = astro["sunset"]

        weather_main = "Clear"
        weather_desc = "맑음"

        if "cloud" in desc_en or "overcast" in desc_en:
            weather_main = "Clouds"
            weather_desc = "구름 많음"

        elif "rain" in desc_en or "drizzle" in desc_en:
            weather_main = "Rain"
            weather_desc = "비"

        elif "snow" in desc_en:
            weather_main = "Snow"
            weather_desc = "눈"

        return temp, weather_main, weather_desc, dust, visibility, sunrise, sunset

    except:
        return default
        import streamlit as st
from weather_engine import get_weather

# =========================
# 1. 기본 설정
# =========================
st.set_page_config(page_title="날씨 월드", layout="centered")

temp, weather_main, weather_desc, dust, visibility, sunrise, sunset = get_weather()

dust_color = "#2ed573" if dust in ["좋음", "보통"] else "#ff4757"


# =========================
# 2. 날씨 테마 (핵심 수정)
# =========================
theme = {
    "Clear": {
        "sky": "linear-gradient(to bottom, #74b9ff, #a29bfe)",
        "sun": True,
        "rain": False,
        "cloud": True
    },
    "Clouds": {
        "sky": "linear-gradient(to bottom, #636e72, #b2bec3)",
        "sun": False,
        "rain": False,
        "cloud": True
    },
    "Rain": {
        "sky": "linear-gradient(to bottom, #2d3436, #636e72)",
        "sun": False,
        "rain": True,
        "cloud": True
    },
    "Snow": {
        "sky": "linear-gradient(to bottom, #dfe6e9, #ffffff)",
        "sun": False,
        "rain": False,
        "cloud": True
    }
}

t = theme.get(weather_main, theme["Clear"])


# =========================
# 3. CSS (중요: z-index 완전 고정)
# =========================
st.markdown(f"""
<style>

html, body {{
    margin:0;
    padding:0;
}}

.stApp {{
    background: {t["sky"]};
    overflow:hidden;
}}

/* ===== 배경 레이어 ===== */
.bg-layer {{
    position: fixed;
    width:100%;
    height:100%;
    z-index:0;
    pointer-events:none;
}}

/* 태양 */
.sun {{
    position:absolute;
    top:80px;
    right:80px;
    width:80px;
    height:80px;
    background: radial-gradient(circle,#fff176,#ff9800);
    border-radius:50%;
    animation: pulse 3s infinite;
}}

@keyframes pulse {{
    0% {{ transform: scale(1); }}
    50% {{ transform: scale(1.1); }}
    100% {{ transform: scale(1); }}
}}

/* 구름 */
.cloud {{
    position:absolute;
    background:#fff;
    width:120px;
    height:40px;
    border-radius:50px;
    opacity:0.8;
    animation: moveCloud 20s linear infinite;
}}

.cloud::before, .cloud::after {{
    content:"";
    position:absolute;
    background:#fff;
    border-radius:50%;
}}

.cloud::before {{
    width:60px;
    height:60px;
    top:-20px;
    left:10px;
}}

.cloud::after {{
    width:50px;
    height:50px;
    top:-15px;
    right:10px;
}}

@keyframes moveCloud {{
    0% {{ left:-200px; }}
    100% {{ left:110%; }}
}}

/* 비 */
.rain {{
    position:absolute;
    width:2px;
    height:20px;
    background:#74b9ff;
    animation: rainFall 1s linear infinite;
}}

@keyframes rainFall {{
    0% {{ top:-20px; }}
    100% {{ top:100vh; }}
}}

/* 땅 */
.ground {{
    position:fixed;
    bottom:0;
    width:100%;
    height:140px;
    background:#55efc4;
    border-radius:50% 50% 0 0;
    z-index:1;
}}

/* 카드 */
.card {{
    background:white;
    padding:20px;
    border-radius:20px;
    margin:20px 0;
    z-index:10;
    position:relative;
}}

</style>
""", unsafe_allow_html=True)


# =========================
# 4. 배경 렌더링 (핵심)
# =========================
bg_html = "<div class='bg-layer'>"

if t["sun"]:
    bg_html += "<div class='sun'></div>"

if t["cloud"]:
    for i in range(3):
        bg_html += f"<div class='cloud' style='top:{80+i*60}px; animation-duration:{15+i*5}s'></div>"

if t["rain"]:
    for i in range(30):
        bg_html += f"<div class='rain' style='left:{i*3}%'></div>"

bg_html += "</div>"

bg_html += "<div class='ground'></div>"

st.markdown(bg_html, unsafe_allow_html=True)


# =========================
# 5. UI (인덱스 + 설명 강화)
# =========================
st.markdown(f"""
<div class='card'>
<h2>🌡 현재 온도: {temp}°C</h2>
<p>날씨 상태: {weather_desc}</p>
</div>

<div class='card'>
<h3>📊 기상 인덱스</h3>
<p>🌅 일출: {sunrise}</p>
<p>🌇 일몰: {sunset}</p>
<p>😷 미세먼지: {dust}</p>
<p>👁 가시거리: {visibility}</p>
</div>
""", unsafe_allow_html=True)
