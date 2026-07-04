import streamlit as st
import requests

st.set_page_config(page_title="Weather World", layout="centered")


@st.cache_data(ttl=600)
def get_weather():
    url = "https://wttr.in/Bangbae-dong?format=j1"

    default = (22, "Clear", "맑음", "보통", "15km", "05:32", "19:51")

    try:
        r = requests.get(url, timeout=5)
        data = r.json()

        c = data["current_condition"][0]
        a = data["weather"][0]["astronomy"][0]

        temp = round(float(c["temp_C"]))
        desc = c["weatherDesc"][0]["value"].lower()
        visibility = c["visibility"] + "km"
        humidity = int(c["humidity"])

        dust = "좋음" if humidity > 85 else "보통" if humidity > 40 else "나쁨"

        sunrise = a["sunrise"]
        sunset = a["sunset"]

        weather = "Clear"
        kr = "맑음"

        if "cloud" in desc:
            weather = "Clouds"
            kr = "구름"
        elif "rain" in desc:
            weather = "Rain"
            kr = "비"
        elif "snow" in desc:
            weather = "Snow"
            kr = "눈"

        return temp, weather, kr, dust, visibility, sunrise, sunset

    except:
        return default


temp, weather_main, weather_desc, dust, visibility, sunrise, sunset = get_weather()

dust_color = "#2ed573" if dust in ["좋음", "보통"] else "#ff4757"
st.markdown(f"""
<style>

.stApp {{
    background: {{
        "Clear": "linear-gradient(to bottom,#74b9ff,#a29bfe)",
        "Clouds": "linear-gradient(to bottom,#636e72,#b2bec3)",
        "Rain": "linear-gradient(to bottom,#2d3436,#636e72)",
        "Snow": "linear-gradient(to bottom,#dfe6e9,#ffffff)"
    }}.get("{weather_main}", "#74b9ff");
    overflow:hidden;
}}

/* ===== 태양 ===== */
.sun {{
    position: fixed;
    top: 80px;
    right: 80px;
    width: 90px;
    height: 90px;
    background: radial-gradient(circle,#fff176,#ff9800);
    border-radius: 50%;
    box-shadow: 0 0 40px orange;
    animation: pulse 3s infinite;
}}

@keyframes pulse {{
    0% {{ transform: scale(1); }}
    50% {{ transform: scale(1.15); }}
    100% {{ transform: scale(1); }}
}}

/* ===== 구름 ===== */
.cloud {{
    position: fixed;
    width: 120px;
    height: 40px;
    background: white;
    border-radius: 50px;
    opacity: 0.8;
    animation: move 25s linear infinite;
}}

@keyframes move {{
    0% {{ left: -200px; }}
    100% {{ left: 110%; }}
}}

/* ===== 비 ===== */
.rain {{
    position: fixed;
    width: 2px;
    height: 20px;
    background: #74b9ff;
    animation: rain 1s linear infinite;
}}

@keyframes rain {{
    0% {{ top: -20px; }}
    100% {{ top: 100vh; }}
}}

/* ===== 땅 ===== */
.ground {{
    position: fixed;
    bottom: 0;
    width: 100%;
    height: 130px;
    background: #55efc4;
    border-radius: 50% 50% 0 0;
    z-index: 1;
}}

/* ===== 카드 ===== */
.card {{
    background: white;
    padding: 20px;
    margin: 15px;
    border-radius: 20px;
    position: relative;
    z-index: 10;
}}

</style>
""", unsafe_allow_html=True)
bg = "<div>"

if weather_main == "Clear":
    bg += "<div class='sun'></div>"
    bg += "<div class='cloud' style='top:120px;'></div>"
    bg += "<div class='cloud' style='top:200px; animation-duration:35s;'></div>"

elif weather_main == "Clouds":
    bg += "<div class='cloud' style='top:120px;'></div>"
    bg += "<div class='cloud' style='top:200px;'></div>"

elif weather_main == "Rain":
    bg += "<div class='cloud' style='top:120px;'></div>"
    for i in range(20):
        bg += f"<div class='rain' style='left:{i*5}%'></div>"

bg += "</div><div class='ground'></div>"

st.markdown(bg, unsafe_allow_html=True)
st.markdown(f"""
<div class='card'>
<h2>🌡 온도: {temp}°C</h2>
<p>날씨: {weather_desc}</p>
</div>

<div class='card'>
<h3>📊 기상 인덱스</h3>

<p>🌅 일출: {sunrise}</p>
<p>🌇 일몰: {sunset}</p>

<p>😷 미세먼지: {dust}</p>
<p>👁 가시거리: {visibility}</p>
</div>
""", unsafe_allow_html=True)
