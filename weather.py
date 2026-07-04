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


theme = {
    "Clear": "#74b9ff",
    "Clouds": "#636e72",
    "Rain": "#2d3436",
    "Snow": "#dfe6e9"
}

bg = theme.get(weather_main, "#74b9ff")


st.markdown(f"""
<style>

.stApp {{
    background: {bg};
    overflow:hidden;
}}

.bg {{
    position:fixed;
    width:100%;
    height:100%;
    z-index:0;
}}

.sun {{
    position:absolute;
    top:80px;
    right:80px;
    width:80px;
    height:80px;
    background:yellow;
    border-radius:50%;
    box-shadow:0 0 40px orange;
}}

.cloud {{
    position:absolute;
    width:120px;
    height:40px;
    background:white;
    border-radius:50px;
    opacity:0.8;
}}

.ground {{
    position:fixed;
    bottom:0;
    width:100%;
    height:120px;
    background:#55efc4;
    border-radius:50% 50% 0 0;
    z-index:1;
}}

.card {{
    background:white;
    padding:20px;
    border-radius:20px;
    margin:15px;
    z-index:10;
    position:relative;
}}

</style>
""", unsafe_allow_html=True)


# ===== 배경 =====
bg_html = "<div class='bg'>"

if weather_main == "Clear":
    bg_html += "<div class='sun'></div>"
    bg_html += "<div class='cloud' style='top:120px; left:0px'></div>"
    bg_html += "<div class='cloud' style='top:200px; left:200px'></div>"

elif weather_main == "Clouds":
    bg_html += "<div class='cloud' style='top:120px; left:0px'></div>"
    bg_html += "<div class='cloud' style='top:200px; left:150px'></div>"

elif weather_main == "Rain":
    bg_html += "<div class='cloud' style='top:120px; left:0px'></div>"

bg_html += "</div><div class='ground'></div>"

st.markdown(bg_html, unsafe_allow_html=True)


# ===== UI =====
st.markdown(f"""
<div class='card'>
<h2>🌡 온도: {temp}°C</h2>
<p>날씨: {weather_desc}</p>
</div>

<div class='card'>
<h3>📊 인덱스</h3>
<p>🌅 일출: {sunrise}</p>
<p>🌇 일몰: {sunset}</p>
<p>😷 미세먼지: {dust}</p>
<p>👁 가시거리: {visibility}</p>
</div>
""", unsafe_allow_html=True)
