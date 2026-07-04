import streamlit as st
import requests

st.set_page_config(page_title="방배동 날씨", layout="centered")

# =========================
# 날씨 함수 (여기 포함)
# =========================
@st.cache_data(ttl=600)
def get_weather():
    url = "https://wttr.in/Bangbae-dong?format=j1"

    try:
        r = requests.get(url, timeout=5)
        data = r.json()

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


# =========================
# 데이터 로드
# =========================
temp, weather, humidity, dust, visibility, sunrise, sunset = get_weather()

# =========================
# 배경
# =========================
sky = {
    "Clear": "#74b9ff",
    "Clouds": "#636e72",
    "Rain": "#2d3436",
    "Snow": "#dfe6e9"
}.get(weather)

ground = {
    "Clear": "#55efc4",
    "Clouds": "#a4b0be",
    "Rain": "#2ecc71",
    "Snow": "#ffffff"
}.get(weather)


# =========================
# CSS
# =========================
st.markdown(f"""
<style>

body {{
    background: {sky};
}}

.ground {{
    position: fixed;
    bottom: 0;
    width: 100%;
    height: 180px;
    background: {ground};
    border-radius: 50% 50% 0 0;
    z-index: -1;
}}

.card {{
    background: white;
    padding: 20px;
    border-radius: 20px;
    margin-top: 30px;
}}

.sky {{
    position: fixed;
    top: 0;
    width: 100%;
    height: 60vh;
    overflow: hidden;
}}

.sun {{
    position: absolute;
    top: 50px;
    right: 50px;
    width: 70px;
    height: 70px;
    background: yellow;
    border-radius: 50%;
    box-shadow: 0 0 30px yellow;
}}

.cloud {{
    position: absolute;
    width: 120px;
    height: 40px;
    background: white;
    border-radius: 50px;
}}

.rain {{
    position: absolute;
    width: 2px;
    height: 15px;
    background: #74b9ff;
    animation: fall 1s linear infinite;
}}

@keyframes fall {{
    0% {{ transform: translateY(0); }}
    100% {{ transform: translateY(60vh); }}
}}

</style>
""", unsafe_allow_html=True)


# =========================
# 오브젝트
# =========================
obj = ""

if weather == "Clear":
    obj = "<div class='sun'></div><div class='cloud' style='top:120px; left:0'></div>"
elif weather == "Clouds":
    obj = "<div class='cloud' style='top:80px; left:0'></div><div class='cloud' style='top:140px; left:150px'></div>"
elif weather == "Rain":
    obj = "<div class='cloud' style='top:80px'></div><div class='rain' style='left:40%'></div><div class='rain' style='left:60%'></div>"

# =========================
# UI
# =========================
st.markdown("<div class='ground'></div>", unsafe_allow_html=True)
st.markdown(f"<div class='sky'>{obj}</div>", unsafe_allow_html=True)

st.title("🌤️ 방배동 날씨")

st.markdown(f"""
<div class='card'>
<h2>{temp}°C</h2>
<p>미세먼지: {dust}</p>
<p>가시거리: {visibility} km</p>
<p>습도: {humidity}%</p>
<p>일출: {sunrise} / 일몰: {sunset}</p>
</div>
""", unsafe_allow_html=True)
