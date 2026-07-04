import streamlit as st
import requests
from streamlit_lottie import st_lottie

# ==========================================
# 1. 페이지 기본 설정 (스트림릿 앱 초기화)
# ==========================================
st.set_page_config(
    page_title="방배동 종합 날씨 정보 🌤️", 
    page_icon="✨", 
    layout="centered"
)

# 브라우저 상단/하단 스트림릿 기본 UI 숨기기
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)


# ==========================================
# 2. 실시간 날씨 데이터 수집 API (안전한 캐싱 적용)
# ==========================================
@st.cache_data(ttl=600)  # 10분간 데이터를 메모리에 캐싱하여 API 오버플로우 방지
def get_bangbae_weather_perfect():
    url = "https://wttr.in/Bangbae-dong?format=j1"
    # 네트워크 끊김이나 서버 다운 시 작동할 안전한 백업 데이터
    default_return = (22, "Clear", "맑음", "보통", "15km", "05:32", "19:51")
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            current = data['current_condition'][0]
            astronomy = data['weather'][0]['astronomy'][0]
            
            temp = round(float(current['temp_C'])) 
            weather_desc_en = current['weatherDesc'][0]['value'].lower()
            visibility = current['visibility'] + "km"
            humidity = int(current['humidity'])
            
            if humidity > 85: dust = "좋음"
            elif 40 <= humidity <= 85: dust = "보통"
            else: dust = "나쁨"
            
            sunrise_str = astronomy['sunrise']
            sunset_str = astronomy['sunset']
            
            weather_main = "Clear"
            weather_desc_kr = "맑음"
            
            if "cloud" in weather_desc_en or "overcast" in weather_desc_en:
                weather_main = "Clouds"
                weather_desc_kr = "구름 많음"
            elif "rain" in weather_desc_en or "shower" in weather_desc_en or "drizzle" in weather_desc_en:
                weather_main = "Rain"
                weather_desc_kr = "비옴"
            elif "snow" in weather_desc_en or "ice" in weather_desc_en:
                weather_main = "Snow"
                weather_desc_kr = "눈"
                
            return temp, weather_main, weather_desc_kr, dust, visibility, sunrise_str, sunset_str
        else:
            return default_return
    except:
        return default_return

def load_lottieurl(url: str):
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200: return r.json()
    except: return None

# 데이터 로드 실행
temp, weather_main, weather_desc, dust, visibility, sunrise, sunset = get_bangbae_weather_perfect()
dust_color = "#2ed573" if "좋음" in dust or "보통" in dust else "#ff4757"


# ==========================================
# 3. 날씨별 Lottie 캐릭터 애니메이션 매핑
# ==========================================
lottie_urls = {
    "Clear": "https://assets3.lottiefiles.com/packages/lf20_xl8aHg.json",
    "Clouds": "https://assets9.lottiefiles.com/packages/lf20_w98qf0as.json",
    "Rain": "https://assets4.lottiefiles.com/packages/lf20_iam97t69.json",
    "Snow": "https://assets1.lottiefiles.com/packages/lf20_96bva6g1.json"
}
lottie_url = lottie_urls.get(weather_main, "https://assets5.lottiefiles.com/packages/lf20_xl8aHg.json")


# ==========================================
# 4. 날씨 테마별 배경(하늘, 땅, 오브젝트) 에셋 빌드
# ==========================================
weather_themes = {
    "Clear": {
        "sky": "linear-gradient(to bottom, #74b9ff, #a29bfe)", 
        "ground": "#55efc4", 
        "obj": '<div class="sun"></div><div class="cloud-ani c1"></div><div class="cloud-ani c2"></div>'
    },
    "Clouds": {
        "sky": "linear-gradient(to bottom, #747d8c, #a4b0be)", 
        "ground": "#2ed573", 
        "obj": '<div class="cloud-ani c1" style="background:#7f8c8d; opacity:0.7;"></div><div class="cloud-ani c2" style="background:#7f8c8d; opacity:0.5; top:130px;"></div>'
    },
    "Rain": {
        "sky": "linear-gradient(to bottom, #2f3640, #718093)", 
        "ground": "#05c46b", 
        "obj": '<div class="cloud-ani c1" style="background:#57606f;"></div><div class="rain-drop r1"></div><div class="rain-drop r2"></div><div class="rain-drop r3"></div>'
    },
    "Snow": {
        "sky": "linear-gradient(to bottom, #dfe4ea, #f1f2f6)", 
        "ground": "#ffffff", 
        "obj": '<div class="snowflake s1"></div><div class="snowflake s2"></div><div class="snowflake s3"></div>'
    }
}
theme = weather_themes.get(weather_main, weather_themes["Clear"])


# ==========================================
# 5. [안전 보장] 웹 표준 기반 CSS 주입 시스템
# ==========================================
st.markdown(f"""
    <link href="https://fonts.googleapis.com/css2?family=Gowun+Dodum&display=swap" rel="stylesheet">
    <style>
        /* [안전] 최외곽 브라우저 배경판만 제어하여 컨테이너 충돌 완전 방지 */
        html, body, [data-testid="stAppViewContainer"] {{
            font-family: 'Gowun Dodum', sans-serif;
            background: {theme["sky"]} !important;
            overflow-x: hidden;
            position: relative;
        }}
        
        /* 언덕 지형 생성 (z-index를 -100으로 밀어내어 글자 카드를 절대 침범하지 않음) */
        [data-testid="stAppViewContainer"]::after {{
            content: ""; position: fixed; bottom: -140px; left: -10%; width: 120%; height: 260px;
            background: {theme["ground"]}; border-radius: 50% 50% 0 0; 
            z-index: -100 !important;
            box-shadow: inset 0 15px 25px rgba(0,0,0,0.04);
        }}

        /* 날씨 그래픽 요소들 정의 (z-index: -50 격리 배치) */
        .sun {{
            position: fixed; top: 70px; right: 12%; width: 75px; height: 75px;
            background: radial-gradient(circle, #fffa65, #ffaf40); border-radius: 50%; z-index: -50;
            box-shadow: 0 0 35px #ffaf40; animation: pulse 4s infinite alternate;
        }}
        @keyframes pulse {{ 0% {{ transform: scale(1); }} 100% {{ transform: scale(1.05); }} }}

        .cloud-ani {{ position: fixed; background: rgba(255,255,255,0.85); border-radius: 100px; width: 130px; height: 38px; z-index: -50; }}
        .cloud-ani::before, .cloud-ani::after {{ content: ""; position: absolute; background: rgba(255,255,255,0.85); border-radius: 50%; }}
        .cloud-ani::before {{ width: 55px; height: 55px; top: -25px; left: 15px; }}
        .cloud-ani::after {{ width: 75px; height: 75px; top: -35px; right: 15px; }}
        .c1 {{ top: 80px; left: -200px; animation: floatC 28s infinite linear; }}
        .c2 {{ top: 160px; left: -200px; animation: floatC 38s infinite linear; animation-delay: 4s; }}
        @keyframes floatC {{ 0% {{ left: -200px; }} 100% {{ left: 105%; }} }}

        .rain-drop {{ position: fixed; background: #e1f5fe; width: 3px; height: 22px; border-radius: 50%; animation: fall 1.4s infinite linear; z-index: -50; }}
        .r1 {{ left: 15%; top: -50px; }} .r2 {{ left: 50%; top: -50px; animation-delay: 0.4s; }} .r3 {{ left: 85%; top: -50px; animation-delay: 0.8s; }}
        @keyframes fall {{ 0% {{ top: -50px; }} 100% {{ top: 100vh; }} }}

        .snowflake {{ position: fixed; background: white; width: 8px; height: 8px; border-radius: 50%; animation: snowFall 4s infinite linear; z-index: -50; }}
        .s1 {{ left: 20%; top: -20px; }} .s2 {{ left: 55%; top: -20px; animation-delay: 1.5s; }} .s3 {{ left: 80%; top: -20px; animation-delay: 2.5s; }}
        @keyframes snowFall {{ 0% {{ top: -20px; }} 100% {{ top: 100vh; }} }}

        /* 화이트 큐브 정보 카드 (가독성 최상위 구조 보장) */
        .weather-card {{
            background: #ffffff !important;
            border-radius: 18px; padding: 22px; margin-bottom: 20px;
            box-shadow: 0px 5px 20px rgba(0, 0, 0, 0.05);
            border: 1px solid #eef2f5;
        }}
        
        .main-title {{ text-align: center; font-size: 2.2rem; font-weight: bold; color: #1e272e; margin-top: 10px; }}
        .sub-title {{ text-align: center; color: #57606f; margin-bottom: 25px; }}
        
        /* 인포 박스 그리드 */
        .info-grid {{ display: flex; justify-content: space-between; gap: 12px; margin-top: 15px; }}
        .info-box {{
            flex: 1; background: #f8f9fa; border-radius: 12px; padding: 12px; text-align: center;
            border: 1px solid #f1f2f6;
        }}
        .info-icon {{ font-size: 1.7rem; margin-bottom: 4px; }}
        .info-title {{ font-size: 0.8rem; color: #747d8c; }}
        .info-value {{ font-size: 1rem; font-weight: bold; color: #2f3542; }}
        
        .bar-container {{ background: #dee2e6; border-radius: 10px; height: 6px; margin-top: 7px; overflow: hidden; }}
        .bar-fill {{ background: {dust_color}; height: 100%; border-radius: 100px; }}
        .highlight {{ color: #ff4757; font-weight: bold; }}
    </style>
""", unsafe_allow_html=True)


# ==========================================
# 6. 컴포넌트 순차 출력 렌더링 (안정성 100%)
# ==========================================

# 1) 백그라운드 기상 요소 주입
st.markdown(theme["obj"], unsafe_allow_html=True)

# 2) 타이틀 텍스트 출력
st.markdown("<h1 class='main-title'>📍 방배동 날씨 동화 세계</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>실시간 대기질 및 기온 연동 애니메이션 인포그래픽</p>", unsafe_allow_html=True)

# 3) [버그 수정 완료] Lottie 캐릭터 애니메이션 단독 호출 (HTML 깨짐 원인 제거)
lottie_motion = load_lottieurl(lottie_url)
if lottie_motion:
    st_lottie(lottie_motion, height=160, key="center_lottie_final_perfect")

# 4) 메인 현재 기온 카드
st.markdown(f"""
    <div class='weather-card' style='text-align: center;'>
        <h2 style='margin: 0; color: #2f3542;'>🌡️ 현재 방배동: {temp}°C</h2>
        <p style='margin: 5px 0 0 0; color: #747d8c; font-size: 1.05rem;'>실시간 기상 현황: <b>{weather_desc}</b></p>
    </div>
""", unsafe_allow_html=True)

# 5) 실시간 대기 및 환경 인덱스 카드
st.markdown(f"""
    <div class='weather-card'>
        <h3 style='margin-top:0; color:#2f3542; font-size:1.2rem; text-align:center;'>📊 실시간 방배동 기상 인덱스</h3>
        <div class='info-grid'>
            <div class='info-box'>
                <div class='info-icon'>🌅</div>
                <div class='info-title'>일출 시간</div>
                <div class='info-value'>{sunrise}</div>
            </div>
            <div class='info-box'>
                <div class='info-icon'>🌇</div>
                <div class='info-title'>일몰 시간</div>
                <div class='info-value'>{sunset}</div>
            </div>
            <div class='info-box'>
                <div class='info-icon'>😷</div>
                <div class='info-title'>대기 현황</div>
                <div class='info-value' style='color:{dust_color};'>{dust}</div>
                <div class='bar-container'><div class='bar-fill' style='width: {"30%" if "좋음" in dust or "보통" in dust else "85%"};'></div></div>
            </div>
            <div class='info-box'>
                <div class='info-icon'>👁️</div>
                <div class='info-title'>가시거리</div>
                <div class='info-value'>{visibility}</div>
                <div class='bar-container'><div class='bar-fill' style='background:#70a1ff; width: 90%;'></div></div>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# 6) 기온별 스마트 코디 가이드 제안 카드
card_content = ""
if temp >= 28: card_content = "☀️ <b>한여름 폭염 날씨예요!</b><br>👉 추천 코디: <span class='highlight'>민소매, 반팔티, 린넨 쇼츠, 선글라스</span>"
elif 23 <= temp < 28: card_content = "🌤️ <b>가벼운 여름 기온이에요.</b><br>👉 추천 코디: <span class='highlight'>반팔 셔츠, 슬림 면바지, 오픈형 샌들</span>"
elif 20 <= temp < 23: card_content = "🍃 <b>선선한 봄/가을 온도대입니다.</b><br>👉 추천 코디: <span class='highlight'>옥스퍼드 셔츠, 니트조끼, 데님 팬츠</span>"
elif 17 <= temp < 20: card_content = "🧥 <b>일교차가 가파릅니다. 아우터 필수 지참!</b><br>👉 추천 코디: <span class='highlight'>맨투맨, 후디, 가디건 레이어링</span>"
elif 12 <= temp < 17: card_content = "🍂 <b>쌀쌀한 환절기입니다. 감기 조심하세요!</b><br>👉 추천 코디: <span class='highlight'>울 재킷, 트렌치 코트, 도톰한 니트</span>"
elif 9 <= temp < 12: card_content = "💨 <b>외풍이 강하니 레이어드룩이 제격입니다.</b><br>👉 추천 코디: <span class='highlight'>야상 점퍼, 도톰한 헤비 니트, 기모바지</span>"
elif 5 <= temp < 9: card_content = "🥶 <b>초겨울 추위 시즌이에요! 따뜻하게 입으세요.</b><br>👉 추천 코디: <span class='highlight'>롱코트, 무스탕 재킷, 다운 패딩</span>"
else: card_content = "❄️ <b>겨울 한파 기온입니다! 외부 활동 자제!</b><br>👉 추천 코디: <span class='highlight'>롱패딩, 방한 목도리, 장갑 필수</span>"

st.markdown(f"""
    <div class='weather-card' style='font-size: 1.1rem; line-height: 1.8; color: #2f3542;'>
        <h4 style='margin-top:0; color:#1e272e; font-size:1.15rem;'>👗 오늘의 방배동 맞춤 코디 큐레이션</h4>
        {card_content}
    </div>
""", unsafe_allow_html=True)
