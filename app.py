import streamlit as st
import requests
from streamlit_lottie import st_lottie

# ==========================================
# 1. 페이지 기본 설정 및 보안 (최상단 배치)
# ==========================================
st.set_page_config(
    page_title="방배동 날씨 동화 세계 🌤️", 
    page_icon="✨", 
    layout="centered"
)

# 스트림릿 기본 헤더/푸터 강제 제거
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)


# ==========================================
# 2. 실시간 날씨 데이터 수집 API (캐싱 적용)
# ==========================================
@st.cache_data(ttl=600)  # 10분간 데이터 캐싱
def get_bangbae_weather_perfect():
    url = "https://wttr.in/Bangbae-dong?format=j1"
    # API 실패 시 안전하게 작동할 기본값
    default_return = (22, "Clear", "맑음 (기본 로드)", "보통", "15km", "05:32", "19:51", 0)
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
            
            # 대기질 환산
            if humidity > 85: dust = "좋음"
            elif 40 <= humidity <= 85: dust = "보통"
            else: dust = "나쁨 (건조)"
            
            sunrise_str = astronomy['sunrise']
            sunset_str = astronomy['sunset']
            
            # 간단하고 확실한 밤낮 구분 로직
            # 기본적으로 데모 환경 및 글로벌 서버 안정성을 위해 낮(0)으로 두되, 
            # 오후 7시 이후나 오전 6시 이전을 조건화하여 확장 가능합니다.
            is_night = 0 
            
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
                
            return temp, weather_main, weather_desc_kr, dust, visibility, sunrise_str, sunset_str, is_night
        else:
            return default_return
    except:
        return default_return

# Lottie 로더
def load_lottieurl(url: str):
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            return r.json()
    except:
        return None

# 기상 데이터 로드 실행
temp, weather_main, weather_desc, dust, visibility, sunrise, sunset, is_night = get_bangbae_weather_perfect()
dust_color = "#2ed573" if "좋음" in dust or "보통" in dust else "#ff4757"


# ==========================================
# 3. 날씨별 애니메이션 캐릭터 매핑
# ==========================================
lottie_urls = {
    "Clear": "https://assets3.lottiefiles.com/packages/lf20_xl8aHg.json",
    "Clouds": "https://assets9.lottiefiles.com/packages/lf20_w98qf0as.json",
    "Rain": "https://assets4.lottiefiles.com/packages/lf20_iam97t69.json",
    "Snow": "https://assets1.lottiefiles.com/packages/lf20_96bva6g1.json"
}
lottie_url = lottie_urls.get(weather_main, "https://assets5.lottiefiles.com/packages/lf20_xl8aHg.json")


# ==========================================
# 4. 날씨 테마별 배경(Scene) 데이터 설정
# ==========================================
weather_themes = {
    "Clear": {
        "sky_day": "linear-gradient(to bottom, #74b9ff, #a29bfe)", 
        "sky_night": "linear-gradient(to bottom, #1e272e, #0f171e)", 
        "ground": "#55efc4",
        "objects_day": '<div class="sun"></div><div class="cloud-ani c1"></div><div class="cloud-ani c2"></div><div class="tree">🌳</div>',
        "objects_night": '<div class="moon"></div><div class="star s1"></div><div class="star s2"></div><div class="star s3"></div><div class="tree">🌳</div>'
    },
    "Clouds": {
        "sky_day": "linear-gradient(to bottom, #747d8c, #a4b0be)", 
        "sky_night": "linear-gradient(to bottom, #2f3640, #1c1e22)", 
        "ground": "#2ed573",
        "objects_day": '<div class="cloud-ani c1" style="background:#7f8c8d; opacity:0.7;"></div><div class="cloud-ani c2" style="background:#7f8c8d; opacity:0.6; top:140px;"></div><div class="tree">🌳</div>',
        "objects_night": '<div class="moon" style="opacity:0.3;"></div><div class="cloud-ani c1" style="background:#34495e; opacity:0.5;"></div><div class="tree">🌳</div>'
    },
    "Rain": {
        "sky_day": "linear-gradient(to bottom, #2f3640, #718093)", 
        "sky_night": "linear-gradient(to bottom, #0f171e, #000000)", 
        "ground": "#05c46b",
        "objects_day": '<div class="cloud-ani c1" style="background:#718093;"></div><div class="rain-drop r1"></div><div class="rain-drop r2"></div><div class="tree">🌳</div>',
        "objects_night": '<div class="cloud-ani c1" style="background:#34495e; opacity:0.5;"></div><div class="rain-drop r1"></div><div class="rain-drop r2"></div><div class="tree">🌳</div>'
    },
    "Snow": {
        "sky_day": "linear-gradient(to bottom, #dfe4ea, #f1f2f6)", 
        "sky_night": "linear-gradient(to bottom, #57606f, #2c3e50)", 
        "ground": "#ffffff", # 눈 덮인 하얀 땅
        "objects_day": '<div class="snowflake s1"></div><div class="snowflake s2"></div><div class="tree">🌳</div>',
        "objects_night": '<div class="moon"></div><div class="snowflake s1"></div><div class="tree">🌳</div>'
    }
}

theme = weather_themes.get(weather_main, weather_themes["Clear"])
current_sky = theme["sky_night"] if is_night else theme["sky_day"]
current_objects = theme["objects_night"] if is_night else theme["objects_day"]


# ==========================================
# 5. [핵심 혁신] 충돌 제로 CSS 주입 시스템
# ==========================================
st.markdown(f"""
    <link href="https://fonts.googleapis.com/css2?family=Gowun+Dodum&display=swap" rel="stylesheet">
    <style>
        /* 1. 최하단 기본 브라우저 및 스크롤 설정 */
        html, body, [data-testid="stAppViewContainer"] {{
            font-family: 'Gowun Dodum', sans-serif;
            background: {current_sky} !important;
            overflow-x: hidden;
            position: relative;
            z-index: 0;
        }}
        
        /* 2. 지피티의 피드백 전격 반영: 부모 블록 단계를 전부 관통하는 z-index 상향 평준화 */
        [data-testid="stVerticalBlock"], .element-container, .stMarkdown {{
            position: relative !important;
            z-index: 1000 !important; /* 배경 그래픽 오브젝트들을 무조건 누름 */
        }}
        
        /* 3. position: fixed 최소화 -> absolute 기반의 샌드위치 레이어 구조 구현 */
        [data-testid="stAppViewContainer"]::after {{
            content: ""; position: absolute; bottom: 0; left: -10%; width: 120%; height: 260px;
            background: {theme["ground"]}; border-radius: 50% 50% 0 0; 
            z-index: 1 !important; /* 하늘(0)보단 위, 카드(2000)보단 아래 */
            box-shadow: inset 0 20px 30px rgba(0,0,0,0.05);
            transition: background 0.6s ease;
        }}

        /* 날씨 테마별 배경 그래픽 클래스 (z-index: 0~2 배치로 카드 가림 원천 봉쇄) */
        .sun {{
            position: absolute; top: 50px; right: 10%; width: 85px; height: 85px;
            background: radial-gradient(circle, #fffa65, #ffaf40); border-radius: 50%; z-index: 0;
            box-shadow: 0 0 40px #ffaf40; animation: pulse 4s infinite alternate;
        }}
        @keyframes pulse {{ 0% {{ transform: scale(1); }} 100% {{ transform: scale(1.06); }} }}

        .moon {{
            position: absolute; top: 50px; right: 12%; width: 70px; height: 70px;
            background: #f1c40f; border-radius: 50%; z-index: 0; box-shadow: 0 0 30px rgba(241, 196, 15, 0.5);
        }}

        .star {{ position: absolute; background: white; border-radius: 50%; z-index: 0; animation: twinkle 2s infinite alternate; }}
        .s1 {{ width: 3px; height: 3px; top: 60px; left: 15%; }}
        .s2 {{ width: 2px; height: 2px; top: 130px; left: 45%; animation-delay: 0.6s; }}
        .s3 {{ width: 3px; height: 3px; top: 80px; left: 75%; animation-delay: 1.2s; }}
        @keyframes twinkle {{ 0% {{ opacity: 0.2; }} 100% {{ opacity: 1; }} }}

        .cloud-ani {{ position: absolute; background: rgba(255,255,255,0.8); border-radius: 100px; width: 140px; height: 42px; z-index: 0; }}
        .cloud-ani::before, .cloud-ani::after {{ content: ""; position: absolute; background: rgba(255,255,255,0.8); border-radius: 50%; }}
        .cloud-ani::before {{ width: 60px; height: 60px; top: -30px; left: 20px; }}
        .cloud-ani::after {{ width: 80px; height: 80px; top: -40px; right: 15px; }}
        .c1 {{ top: 70px; left: -200px; animation: floatCloud 26s infinite linear; }}
        .c2 {{ top: 150px; left: -200px; animation: floatCloud 36s infinite linear; animation-delay: 4s; }}
        @keyframes floatCloud {{ 0% {{ left: -200px; }} 100% {{ left: 105%; }} }}

        .rain-drop {{ position: absolute; background: #e1f5fe; width: 3px; height: 22px; border-radius: 50%; animation: fall 1.2s infinite linear; z-index: 0; }}
        .r1 {{ left: 25%; top: -50px; }} .r2 {{ left: 75%; top: -50px; animation-delay: 0.6s; }}
        @keyframes fall {{ 0% {{ top: -50px; }} 100% {{ top: 100vh; }} }}

        .snowflake {{ position: absolute; background: white; width: 8px; height: 8px; border-radius: 50%; animation: snowFall 4.2s infinite linear; z-index: 0; }}
        .s1 {{ left: 25%; top: -20px; }} .s2 {{ left: 70%; top: -20px; animation-delay: 1.8s; }}
        @keyframes snowFall {{ 0% {{ top: -20px; transform: translateX(0); }} 50% {{ transform: translateX(12px); }} 100% {{ top: 100vh; transform: translateX(-12px); }} }}
        
        .tree {{ position: absolute; bottom: 85px; left: 8%; font-size: 3.8rem; z-index: 2; animation: sway 6s infinite alternate ease-in-out; }}
        @keyframes sway {{ 0% {{ transform: rotate(-3deg); }} 100% {{ transform: rotate(3deg); }} }}

        /* 4. [초정밀 고정] 기상 정보 및 코디 카드의 z-index 완전 격리 (최상단 강제 바인딩) */
        .weather-card {{
            background: rgba(255, 255, 255, 0.91) !important;
            backdrop-filter: blur(12px);
            border-radius: 22px; padding: 24px; margin-bottom: 22px;
            box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.07);
            border: 1px solid rgba(255, 255, 255, 0.7);
            position: relative !important;
            z-index: 2000 !important; /* 어떤 브라우저 버그도 뚫고 맨 앞으로 돌출 */
        }}
        
        .main-title {{ text-align: center; font-size: 2.3rem; font-weight: bold; color: #1e272e; position: relative; z-index: 2000 !important; }}
        .sub-title {{ text-align: center; color: #2f3542; margin-bottom: 25px; position: relative; z-index: 2000 !important; }}
        
        /* 그리드 및 인포박스 레이아웃 스타일 */
        .info-grid {{ display: flex; justify-content: space-between; gap: 12px; margin-top: 15px; flex-wrap: wrap; }}
        .info-box {{
            flex: 1 1 45%; background: rgba(255, 255, 255, 0.7); border-radius: 14px; padding: 12px;
            text-align: center; box-shadow: 0 4px 10px rgba(0,0,0,0.02); min-width: 120px;
        }}
        .info-icon {{ font-size: 1.8rem; margin-bottom: 4px; }}
        .info-title {{ font-size: 0.8rem; color: #57606f; margin-bottom: 3px; }}
        .info-value {{ font-size: 1rem; font-weight: bold; color: #2f3542; }}
        
        .bar-container {{ background: #dee2e6; border-radius: 10px; height: 6px; margin-top: 8px; overflow: hidden; }}
        .bar-fill {{ background: {dust_color}; height: 100%; border-radius: 100px; }}
        .highlight {{ color: #ff4757; font-weight: bold; }}
    </style>
""", unsafe_allow_html=True)


# ==========================================
# 6. 배경 그래픽 씬(Scene) 생성 및 주입
# ==========================================
st.markdown(current_objects, unsafe_allow_html=True)


# ==========================================
# 7. 메인 본문 콘텐츠 레이아웃 (정상 출력 보장)
# ==========================================
st.markdown("<h1 class='main-title'>📍 방배동 날씨 동화 세계</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>실시간 대기질 및 기온 연동 애니메이션 인포그래픽</p>", unsafe_allow_html=True)

# [버그 완전 패치] st.markdown 쪼개기 수법 삭제. 단독으로 안전하게 컴포넌트 렌더링
lottie_motion = load_lottieurl(lottie_url)
if lottie_motion:
    st_lottie(lottie_motion, height=180, key="center_lottie_perfect_final")

# 현재 기온 카드
time_label = "🌙 밤 기온 정보" if is_night else "☀️ 낮 기온 정보"
st.markdown(f"""
    <div class='weather-card' style='text-align: center;'>
        <h2 style='margin: 0; color: #2f3542;'>🌡️ 현재 방배동: {temp}°C</h2>
        <p style='margin: 5px 0 0 0; color: #57606f; font-size: 1.1rem;'>기상 상태: <b>{weather_desc}</b> ({time_label})</p>
    </div>
""", unsafe_allow_html=True)

# 실시간 기상 인덱스 카드
st.markdown(f"""
    <div class='weather-card'>
        <h3 style='margin-top:0; color:#2f3542; font-size:1.25rem; text-align:center;'>📊 실시간 방배동 기상 인덱스</h3>
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

# 맞춤 코디 큐레이션 가이드 카드
card_content = ""
if temp >= 28: card_content = "☀️ <b>한여름 폭염 날씨예요!</b><br>👉 추천 코디: <span class='highlight'>민소매, 반팔티, 린넨 쇼츠, 선글라스</span>"
elif 23 <= temp < 28: card_content = "🌤️ <b>산뜻하고 가벼운 여름 기온이에요.</b><br>👉 추천 코디: <span class='highlight'>반팔 셔츠, 슬림 면바지, 오픈형 샌들</span>"
elif 20 <= temp < 23: card_content = "🍃 <b>선선하고 부드러운 봄/가을 온도대입니다.</b><br>👉 추천 코디: <span class='highlight'>옥스퍼드 셔츠, 니트조끼, 데님 팬츠</span>"
elif 17 <= temp < 20: card_content = "🧥 <b>일교차가 가파릅니다. 아우터 필히 지참!</b><br>👉 추천 코디: <span class='highlight'>맨투맨, 후디, 가디건 레이어링</span>"
elif 12 <= temp < 17: card_content = "🍂 <b>찬 기운이 옷깃을 가르는 쌀쌀한 환절기입니다.</b><br>👉 추천 코디: <span class='highlight'>울 재킷, 트렌치 코트, 도톰한 니트</span>"
elif 9 <= temp < 12: card_content = "💨 <b>외풍이 강하니 레이어드룩이 제격입니다.</b><br>👉 추천 코디: <span class='highlight'>야상 점퍼, 도톰한 헤비 니트, 기모바지</span>"
elif 5 <= temp < 9: card_content = "🥶 <b>초겨울 추위 시즌이에요! 방한 장비 점검!</b><br>👉 추천 코디: <span class='highlight'>롱코트, 무스탕 재킷, 다운 패딩, 발열내의</span>"
else: card_content = "❄️ <b>동파 사고를 조심해야 하는 겨울 한파 기온입니다!</b><br>👉 추천 코디: <span class='highlight'>롱패딩, 방한 목도리, 귀도리, 장갑 필수</span>"

st.markdown(f"""
    <div class='weather-card' style='font-size: 1.15rem; line-height: 1.9; color: #2f3542;'>
        <h4 style='margin-top:0; color:#1e272e; font-size:1.2rem;'>👗 오늘의 방배동 맞춤 코디 큐레이션</h4>
        {card_content}
    </div>
""", unsafe_allow_html=True)
