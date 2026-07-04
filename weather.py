import streamlit as st
import requests
from datetime import datetime
import time

st.set_page_config(
    page_title="방배동 날씨",
    page_icon="🌤️",
    layout="wide"
)

API_KEY = st.secrets["OPENWEATHER_API_KEY"]

LAT = 37.4816
LON = 126.9820

st.markdown("""
<style>

html,body,.stApp{
margin:0;
padding:0;
overflow-x:hidden;
background:#87CEEB;
font-family:Arial,Helvetica,sans-serif;
}

.block-container{
padding-top:1rem;
padding-bottom:2rem;
max-width:1200px;
}

.card{
background:rgba(255,255,255,.18);
backdrop-filter:blur(18px);
border-radius:25px;
padding:20px;
box-shadow:0 10px 25px rgba(0,0,0,.2);
}

.metric{
background:rgba(255,255,255,.15);
padding:18px;
border-radius:20px;
text-align:center;
font-size:22px;
margin-bottom:15px;
}

.sky{
position:fixed;
left:0;
top:0;
width:100%;
height:100%;
z-index:-10;
background:linear-gradient(#67c6ff,#dff4ff);
}

.sun{
position:absolute;
top:70px;
right:140px;
width:120px;
height:120px;
background:#FFD93D;
border-radius:50%;
box-shadow:0 0 80px #FFD93D;
animation:sun 6s ease-in-out infinite;
}

.cloud{
position:absolute;
font-size:80px;
animation:cloud linear infinite;
}

.c1{
top:90px;
left:-250px;
animation-duration:45s;
}

.c2{
top:180px;
left:-500px;
animation-duration:60s;
}

.c3{
top:280px;
left:-800px;
animation-duration:75s;
}

.ground{
position:fixed;
bottom:0;
left:0;
width:100%;
height:180px;
background:#55b85c;
z-index:-5;
}

@keyframes cloud{
0%{transform:translateX(0);}
100%{transform:translateX(2200px);}
}

@keyframes sun{
0%{transform:translateY(0);}
50%{transform:translateY(-12px);}
100%{transform:translateY(0);}
}

.title{
font-size:48px;
font-weight:bold;
color:white;
text-shadow:2px 2px 10px black;
}

.sub{
font-size:22px;
color:white;
margin-bottom:25px;
}

</style>

<div class="sky">
<div class="sun"></div>
<div class="cloud c1">☁️</div>
<div class="cloud c2">☁️</div>
<div class="cloud c3">☁️</div>
</div>

<div class="ground"></div>

""",unsafe_allow_html=True)

weather_url=(
"https://api.openweathermap.org/data/2.5/weather"
f"?lat={LAT}"
f"&lon={LON}"
f"&appid={API_KEY}"
"&units=metric"
"&lang=kr"
)

air_url=(
"https://api.openweathermap.org/data/2.5/air_pollution"
f"?lat={LAT}"
f"&lon={LON}"
f"&appid={API_KEY}"
)

weather=requests.get(weather_url).json()
air=requests.get(air_url).json()

if "main" not in weather:
    st.error(weather)
    st.stop()

temp=weather["main"]["temp"]
feel=weather["main"]["feels_like"]
humidity=weather["main"]["humidity"]
pressure=weather["main"]["pressure"]
visibility=weather["visibility"]/1000
wind=weather["wind"]["speed"]

description=weather["weather"][0]["description"]
weather_id=weather["weather"][0]["id"]

sunrise=datetime.fromtimestamp(
weather["sys"]["sunrise"]
).strftime("%H:%M")

sunset=datetime.fromtimestamp(
weather["sys"]["sunset"]
).strftime("%H:%M")

aqi=air["list"][0]["main"]["aqi"]

aqi_text={
1:"😀 좋음",
2:"🙂 보통",
3:"😷 나쁨",
4:"🤢 매우 나쁨",
5:"☠️ 최악"
}

st.markdown(
f"""
<div class="title">🌤️ 방배동 실시간 날씨</div>
<div class="sub">{description}</div>
""",
unsafe_allow_html=True
)

c1,c2,c3,c4=st.columns(4)

with c1:
    st.metric("🌡️ 기온",f"{temp:.1f}°C")

with c2:
    st.metric("🤗 체감",f"{feel:.1f}°C")

with c3:
    st.metric("💧 습도",f"{humidity}%")

with c4:
    st.metric("💨 풍속",f"{wind:.1f}m/s")
    c5,c6,c7,c8=st.columns(4)

with c5:
    st.metric("👀 가시거리",f"{visibility:.1f} km")

with c6:
    st.metric("🌫️ 미세먼지",aqi_text[aqi])

with c7:
    st.metric("🌅 일출",sunrise)

with c8:
    st.metric("🌇 일몰",sunset)

st.divider()

# ==========================
# 추천 복장
# ==========================

def outfit(temp):

    if temp >= 30:
        return (
            "🥵 매우 더움\n\n"
            "👕 민소매\n"
            "🩳 반바지\n"
            "🩴 슬리퍼\n"
            "🧴 선크림 필수"
        )

    elif temp >= 25:
        return (
            "☀️ 더운 날씨\n\n"
            "👕 반팔\n"
            "👖 얇은 바지\n"
            "🧢 모자 추천"
        )

    elif temp >= 20:
        return (
            "😊 따뜻함\n\n"
            "👕 반팔\n"
            "👖 긴바지"
        )

    elif temp >= 17:
        return (
            "🙂 선선함\n\n"
            "👔 셔츠\n"
            "🧥 얇은 가디건"
        )

    elif temp >= 12:
        return (
            "🍂 조금 쌀쌀\n\n"
            "🧥 자켓"
        )

    elif temp >= 9:
        return (
            "🥶 쌀쌀함\n\n"
            "🧥 트렌치코트"
        )

    elif temp >= 5:
        return (
            "❄️ 추움\n\n"
            "🧥 코트\n"
            "🧣 목도리"
        )

    else:
        return (
            "🥶 매우 추움\n\n"
            "🧥 패딩\n"
            "🧤 장갑\n"
            "🧣 목도리"
        )

st.subheader("👕 오늘의 추천 복장")
st.success(outfit(temp))

st.divider()

# ==========================
# 현재 상태
# ==========================

left,right=st.columns([2,1])

with left:

    st.markdown("## 📊 현재 기상 정보")

    st.write(f"**현재 날씨 :** {description}")
    st.write(f"**기온 :** {temp:.1f}°C")
    st.write(f"**체감온도 :** {feel:.1f}°C")
    st.write(f"**습도 :** {humidity}%")
    st.write(f"**기압 :** {pressure} hPa")
    st.write(f"**풍속 :** {wind:.1f} m/s")
    st.write(f"**가시거리 :** {visibility:.1f} km")
    st.write(f"**미세먼지 :** {aqi_text[aqi]}")

with right:

    st.markdown("## ☀️ 태양")

    st.metric("🌅 일출",sunrise)

    st.metric("🌇 일몰",sunset)

st.divider()

st.markdown(
"""
### 🌎 실시간 방배동 날씨

현재 정보는 OpenWeather API를 이용하여
실시간으로 불러오고 있습니다.
"""
)
# ==========================
# 날씨별 배경 변경
# ==========================

def weather_background(weather_id):

    # 맑음
    if weather_id == 800:

        st.markdown("""
        <style>

        .sky{
            background:linear-gradient(#68c8ff,#dff6ff);
        }

        .sun{
            display:block;
        }

        </style>
        """,unsafe_allow_html=True)

    # 구름
    elif 801 <= weather_id <= 804:

        st.markdown("""
        <style>

        .sky{
            background:linear-gradient(#9eb7c9,#e8f0f7);
        }

        .sun{
            opacity:.4;
        }

        </style>
        """,unsafe_allow_html=True)

    # 비
    elif 500 <= weather_id <= 531:

        st.markdown("""
        <style>

        .sky{
            background:linear-gradient(#58677d,#9aa7b8);
        }

        .rain{
            position:fixed;
            top:0;
            left:0;
            width:100%;
            height:100%;
            pointer-events:none;
            z-index:-4;
            font-size:28px;
            animation:rain 1.2s linear infinite;
        }

        @keyframes rain{
            from{transform:translateY(-100px);}
            to{transform:translateY(100vh);}
        }

        </style>

        <div class="rain">
        🌧️ 🌧️ 🌧️ 🌧️ 🌧️ 🌧️ 🌧️ 🌧️ 🌧️ 🌧️ 🌧️ 🌧️
        </div>

        """,unsafe_allow_html=True)

    # 눈
    elif 600 <= weather_id <= 622:

        st.markdown("""
        <style>

        .sky{
            background:linear-gradient(#d7e6f5,#f6fbff);
        }

        .snow{
            position:fixed;
            top:0;
            left:0;
            width:100%;
            height:100%;
            pointer-events:none;
            z-index:-4;
            font-size:28px;
            animation:snow 6s linear infinite;
        }

        @keyframes snow{
            from{transform:translateY(-100px);}
            to{transform:translateY(100vh);}
        }

        </style>

        <div class="snow">
        ❄️ ❄️ ❄️ ❄️ ❄️ ❄️ ❄️ ❄️ ❄️ ❄️ ❄️
        </div>

        """,unsafe_allow_html=True)

    # 천둥
    elif 200 <= weather_id <= 232:

        st.markdown("""
        <style>

        .sky{
            background:#444;
        }

        .flash{

            position:fixed;

            inset:0;

            background:white;

            opacity:0;

            animation:flash 4s infinite;

            z-index:-3;

        }

        @keyframes flash{

            0%,92%,100%{
                opacity:0;
            }

            94%{
                opacity:.8;
            }

            96%{
                opacity:0;
            }

        }

        </style>

        <div class="flash"></div>

        """,unsafe_allow_html=True)


weather_background(weather_id)

# ==========================
# 자동 새로고침
# ==========================

st.caption("🔄 5분마다 자동으로 새로고침됩니다.")

time.sleep(300)

st.rerun()
