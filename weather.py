import streamlit as st
import requests
from datetime import datetime

# ----------------------------
# 설정
# ----------------------------

API_KEY = "여기에_API_KEY"

LAT = 37.4816     # 방배동
LON = 126.9820

st.set_page_config(
    page_title="방배동 날씨",
    page_icon="🌤️",
    layout="wide"
)

# ----------------------------
# 데이터 가져오기
# ----------------------------

weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={LAT}&lon={LON}&appid={API_KEY}&units=metric&lang=kr"

air_url = f"https://api.openweathermap.org/data/2.5/air_pollution?lat={LAT}&lon={LON}&appid={API_KEY}"

weather = requests.get(weather_url).json()
air = requests.get(air_url).json()

temp = weather["main"]["temp"]
humidity = weather["main"]["humidity"]
visibility = weather["visibility"] / 1000

weather_id = weather["weather"][0]["id"]
description = weather["weather"][0]["description"]

sunrise = datetime.fromtimestamp(weather["sys"]["sunrise"]).strftime("%H:%M")
sunset = datetime.fromtimestamp(weather["sys"]["sunset"]).strftime("%H:%M")

aqi = air["list"][0]["main"]["aqi"]

# ----------------------------
# AQI
# ----------------------------

aqi_text = {
    1:"😀 좋음",
    2:"🙂 보통",
    3:"😷 나쁨",
    4:"🤢 매우 나쁨",
    5:"☠️ 최악"
}

# ----------------------------
# 복장 추천
# ----------------------------

def outfit(temp):

    if temp >= 28:
        return "🩳 민소매, 반바지, 슬리퍼"

    elif temp >= 23:
        return "👕 반팔 + 반바지"

    elif temp >= 20:
        return "👕 반팔 + 긴바지"

    elif temp >= 17:
        return "👔 얇은 셔츠, 가디건"

    elif temp >= 12:
        return "🧥 자켓"

    elif temp >= 9:
        return "🧥 트렌치코트"

    elif temp >= 5:
        return "🧥 코트"

    else:
        return "🧥 패딩, 목도리, 장갑"

# ----------------------------
# 배경
# ----------------------------

def background(weather_id):

    if weather_id == 800:

        return """
<style>

.stApp{
background:linear-gradient(#79c8ff,#d7f2ff);
}

.sky{
position:fixed;
font-size:70px;
top:5%;
left:5%;
animation:move 40s linear infinite;
}

.ground{
position:fixed;
bottom:0;
width:100%;
height:180px;
background:#4CAF50;
}

@keyframes move{
0%{transform:translateX(-100px);}
100%{transform:translateX(1500px);}
}

</style>

<div class='sky'>
☀️ ☁️ ☁️
</div>

<div class='ground'></div>

"""

    elif 200 <= weather_id < 600:

        return """
<style>

.stApp{
background:#6c7a89;
}

.sky{
position:fixed;
font-size:65px;
top:10%;
animation:rain 15s linear infinite;
}

.ground{
position:fixed;
bottom:0;
width:100%;
height:180px;
background:#2E7D32;
}

@keyframes rain{
0%{transform:translateY(-100px);}
100%{transform:translateY(100px);}
}

</style>

<div class='sky'>
🌧️ 🌧️ 🌧️ 🌧️
</div>

<div class='ground'></div>

"""

    elif 600 <= weather_id <700:

        return """
<style>

.stApp{
background:#dbefff;
}

.sky{
position:fixed;
font-size:60px;
top:10%;
animation:snow 10s linear infinite;
}

.ground{
position:fixed;
bottom:0;
width:100%;
height:180px;
background:white;
}

@keyframes snow{
0%{transform:translateY(-50px);}
100%{transform:translateY(150px);}
}

</style>

<div class='sky'>
❄️ ❄️ ☁️ ❄️
</div>

<div class='ground'></div>

"""

    else:

        return """
<style>

.stApp{
background:linear-gradient(#98b4d4,#eaf4ff);
}

.sky{
position:fixed;
font-size:70px;
top:10%;
animation:move 35s linear infinite;
}

.ground{
position:fixed;
bottom:0;
width:100%;
height:180px;
background:#66BB6A;
}

@keyframes move{
0%{transform:translateX(-300px);}
100%{transform:translateX(1600px);}
}

</style>

<div class='sky'>
☁️ ☁️ ☁️ 🌤️
</div>

<div class='ground'></div>

"""

st.markdown(background(weather_id),unsafe_allow_html=True)

# ----------------------------
# 제목
# ----------------------------

st.title("🌤️ 방배동 실시간 날씨")

st.subheader(description.capitalize())

c1,c2,c3,c4 = st.columns(4)

c1.metric("🌡️ 기온",f"{temp:.1f}°C")
c2.metric("💧 습도",f"{humidity}%")
c3.metric("👀 가시거리",f"{visibility:.1f} km")
c4.metric("🌫️ 미세먼지",aqi_text[aqi])

st.divider()

a,b = st.columns(2)

with a:
    st.metric("🌅 일출",sunrise)

with b:
    st.metric("🌇 일몰",sunset)

st.divider()

st.header("👕 추천 복장")

st.success(outfit(temp))
