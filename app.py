import streamlit as st
import requests
from streamlit_lottie import st_lottie
import time

# ==========================================
# 1. 페이지 기본 설정 및 보안
# ==========================================
st.set_page_config(
    page_title="방배동 날씨 동화 세계 🌤️", 
    page_icon="✨", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 스트림릿 기본 헤더/푸터 숨기기 (더 몰입감 있는 배경을 위해)
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)


# ==========================================
# 2. 실시간 날씨 데이터 API (wttr.in 글로벌 소스)
# ==========================================
@st.cache_data(ttl=600) # 10분간 캐싱하여 성능 향상 및 API 부담 감소
def get_bangbae_weather_full():
    # 방배동 위경도 기반 글로벌 오픈 날씨 데이터 사용 (JSON 포맷)
    url = "https://wttr.in/Bangbae-dong?format=j1"
    
    # 서버 오류나 네트워크 단절 시 사용할 안전한 기본값 설정
    default_return = (22, "Clear", "맑음 (기본 로드)", "보통", "15km", "05:32", "19:51", 0) # 마지막 0은 밤낮 구분 (0: 낮, 1: 밤)
    
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
            
            # 습도를 활용한 대기 청정 지표 환산
            if humidity > 85: dust = "좋음"
            elif 40 <= humidity <= 85: dust = "보통"
            else: dust = "나쁨 (건조)"
            
            # 일출, 일몰 파싱 및 현재 시간과 비교하여 밤낮 구분
            sunrise_str = astronomy['sunrise']
            sunset_str = astronomy['sunset']
            
            # 간단한 밤낮 구분 로직 (실제 배포시는 시간 라이브러리 활용 권장)
            # 여기서는 시간만 추출해서 비교 (예: "05:32 AM" -> 5.5, "07:51 PM" -> 19.8)
            def parse_time(time_str):
                time_part, ampm = time_str.split(' ')
                hours, minutes = map(int, time_part.split(':'))
                if ampm == 'PM' and hours != 12: hours += 12
                if ampm == 'AM' and hours == 12: hours = 0
                return hours + minutes/60.0

            sunrise_f = parse_time(sunrise_str)
            sunset_f = parse_time(sunset_str)
            
            # 현재 시간 (서버 시간 기준이므로 배포 환경에 따라 보정 필요할 수 있음)
            # 여기서는 데모를 위해 고정된 낮 시간으로 설정 (실제 배포시 보정)
            current_f = 14.0 # 예: 오후 2시
            
            is_night = 1 if current_f < sunrise_f or current_f > sunset_f else 0
            
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


# ==========================================
# 3. Lottie 애니메이션 로드 기능
# ==========================================
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200: return None
    return r.json()


# ==========================================
# 4. 실시간 데이터 로드 (캐싱 활용)
# ==========================================
temp, weather_main, weather_desc, dust, visibility, sunrise, sunset, is_night = get_bangbae_weather_full()

# 미세먼지 등급별 색상 지정
dust_color = "#2ed573" if "좋음" in dust or "보통" in dust else "#ff4757"


# ==========================================
# 5. 날씨 테마 및 동적 CSS 시스템 정의 (구조 전면 재설계)
# ==========================================

# 날씨별 Lottie 캐릭터 매핑
lottie_urls = {
    "Clear": "https://assets3.lottiefiles.com/packages/lf20_xl8aHg.json",
    "Clouds": "https://assets9.lottiefiles.com/packages/lf20_w98qf0as.json",
    "Rain": "https://assets4.lottiefiles.com/packages/lf20_iam97t69.json",
    "Snow": "https://assets1.lottiefiles.com/packages/lf20_96bva6g1.json"
}
lottie_url = lottie_urls.get(weather_main, "https://assets5.lottiefiles.com/packages/lf20_xl8aHg.json")


# 날씨 테마별 배경(하늘, 땅) 및 무빙 오브젝트 설정
# 지피티 추천 기능 반영: 낮/밤, 맑음/흐림/비/눈에 따른 동적 변경
weather_themes = {
    "Clear": {
        "sky_day": "linear-gradient(to bottom, #74b9ff, #a29bfe)",
        "sky_night": "linear-gradient(to bottom, #2c3e50, #000000)",
        "ground": "#55efc4",
        "objects_day": '<div class="sun"></div><div class="cloud-ani c1"></div><div class="cloud-ani c2"></div><div class="tree">🌳</div>',
        "objects_night": '<div class="moon"></div><div class="star s1"></div><div class="star s2"></div><div class="star s3"></div><div class="tree">🌳</div>',
    },
    "Clouds": {
        "sky_day": "linear-gradient(to bottom, #747d8c, #a4b0be)",
        "sky_night": "linear-gradient(to bottom, #2f3640, #1c1e22)",
        "ground": "#2ed573",
        "objects_day": '<div class="cloud-ani c1" style="opacity: 0.9; background: #7f8c8d;"></div><div class="cloud-ani c2" style="transform: scale(1.4); top: 22%; animation-duration: 28s; background: #7f8c8d;"></div><div class="tree">🌳</div>',
        "objects_night": '<div class="moon" style="opacity: 0.5;"></div><div class="cloud-ani c1" style="opacity: 0.5; background: #34495e;"></div><div class="tree">🌳</div>',
    },
    "Rain": {
        "sky_day": "linear-gradient(to bottom, #2f3640, #718093)",
        "sky_night": "linear-gradient(to bottom, #1c1e22, #000000)",
        "ground": "#05c46b",
        "objects_day": '<div class="cloud-ani c1" style="background: #718093;"></div><div class="rain-drop r1"></div><div class="rain-drop r2"></div><div class="rain-drop r3"></div><div class="tree_wet">🌳</div>',
        "objects_night": '<div class="cloud-ani c1" style="opacity: 0.5; background: #34495e;"></div><div class="rain-drop r1"></div><div class="rain-drop r2"></div><div class="tree_wet">🌳</div>',
    },
    "Snow": {
        "sky_day": "linear-gradient(to bottom, #dfe4ea, #f1f2f6)",
        "sky_night": "linear-gradient(to bottom, #747d8c, #2c3e50)",
        "ground": "#ffffff", # 눈 덮인 하얀 땅
        "objects_day": '<div class="snowflake s1"></div><div class="snowflake s2"></div><div class="snowflake s3"></div><div class="tree_snow">🌳</div>',
        "objects_night": '<div class="moon"></div><div class="snowflake s1"></div><div class="snowflake s2"></div><div class="tree_snow">🌳</div>',
    }
}

theme = weather_themes.get(weather_main, weather_themes["Clear"])
current_sky = theme["sky_night"] if is_night else theme["sky_day"]
current_objects = theme["objects_night"] if is_night else theme["objects_day"]


# 통합 CSS 시스템 (구조 전면 재설계: 배경 레이어 관리 및 z-index 문제 근본 해결)
# 카드 선명도 및 반응형 디자인 보강
st.markdown(f"""
    <link href="https://fonts.googleapis.com/css2?family=Gowun+Dodum&display=swap" rel="stylesheet">
    <style>
        /* [핵심] 배경 레이어 통합 관리: 모든 스트림릿 콘텐츠 뒤에 배치 */
        #root {{
            position: relative;
            z-index: 1;
        }}

        /* 1. 설정 및 기본 배경 (하늘) */
        html, body, [data-testid="stAppViewContainer"] {{
            font-family: 'Gowun Dodum', sans-serif;
            background: {current_sky} !important;
            overflow-x: hidden;
            position: relative;
            z-index: 0; /* 최하위 레이어 */
        }}
        
        /* 2. 땅 (배경 레이어의 일부) */
        [data-testid="stAppViewContainer"]::after {{
            content: ""; position: fixed; bottom: -150px; left: -10%; width: 120%; height: 320px;
            background: {theme["ground"]}; border-radius: 50% 50% 0 0; 
            z-index: -1 !important; /* 콘텐츠 바로 뒤, 하늘 위 */
            box-shadow: inset 0 20px 30px rgba(0,0,0,0.05);
            transition: background 0.8s ease;
        }}

        /* 3. 동적 오브젝트 (배경 레이어의 일부) */
        /* 낮 오브젝트 */
        .sun {{
            position: fixed; top: 10%; right: 10%; width: 85px; height: 85px;
            background: radial-gradient(circle, #fffa65, #ffaf40); border-radius: 50%; z-index: -1;
            box-shadow: 0 0 40px #ffaf40; animation: pulse 4s infinite alternate;
        }}
        @keyframes pulse {{ 0% {{ transform: scale(1); }} 100% {{ transform: scale(1.06); }} }}

        .cloud-ani {{ position: fixed; background: rgba(255,255,255,0.8); border-radius: 100px; width: 150px; height: 45px; z-index: -1; }}
        .cloud-ani::before, .cloud-ani::after {{ content: ""; position: absolute; background: rgba(255,255,255,0.8); border-radius: 50%; }}
        .cloud-ani::before {{ width: 65px; height: 65px; top: -30px; left: 20px; }}
        .cloud-ani::after {{ width: 85px; height: 85px; top: -40px; right: 15px; }}
        .c1 {{ top: 15%; left: -200px; animation: floatCloud 24s infinite linear; }}
        .c2 {{ top: 28%; left: -200px; animation: floatCloud 34s infinite linear; animation-delay: 5s; }}
        @keyframes floatCloud {{ 0% {{ left: -200px; }} 100% {{ left: 105%; }} }}

        /* 밤 오브젝트 */
        .moon {{
            position: fixed; top: 10%; right: 12%; width: 70px; height: 70px;
            background: #f1c40f; border-radius: 50%; z-index: -1;
            box-shadow: 0 0 30px rgba(241, 196, 15, 0.5);
        }}
        .star {{ position: fixed; background: white; border-radius: 50%; z-index: -1; animation: twinkle 2s infinite alternate; }}
        .s1 {{ width: 3px; height: 3px; top: 15%; left: 20%; animation-delay: 0s; }}
        .s2 {{ width: 2px; height: 2px; top: 25%; left: 50%; animation-delay: 0.5s; }}
        .s3 {{ width: 3px; height: 3px; top: 10%; left: 80%; animation-delay: 1s; }}
        @keyframes twinkle {{ 0% {{ opacity: 0.3; }} 100% {{ opacity: 1; }} }}

        /* 비/눈 효과 */
        .rain-drop {{ position: fixed; background: #e1f5fe; width: 3px; height: 20px; border-radius: 50%; animation: fall 1.3s infinite linear; z-index: -1; }}
        .r1 {{ left: 15%; top: -50px; }} .r2 {{ left: 50%; top: -50px; animation-delay: 0.4s; }} .r3 {{ left: 85%; top: -50px; animation-delay: 0.8s; }}
        @keyframes fall {{ 0% {{ top: -50px; }} 100% {{ top: 85vh; }} }}

        .snowflake {{ position: fixed; background: white; width: 8px; height: 8px; border-radius: 50%; animation: snowFall 4s infinite linear; z-index: -1; }}
        .s1 {{ left: 20%; top: -20px; }} .s2 {{ left: 60%; top: -20px; animation-delay: 1.5s; }} .s3 {{ left: 85%; top: -20px; animation-delay: 2.5s; }}
        @keyframes snowFall {{ 0% {{ top: -20px; transform: translateX(0); }} 50% {{ transform: translateX(15px); }} 100% {{ top: 85vh; transform: translateX(-15px); }} }}
        
        /* 나무 */
        .tree, .tree_wet, .tree_snow {{ position: fixed; bottom: 120px; left: 15%; font-size: 4rem; z-index: -1; animation: sway 5s infinite alternate ease-in-out; }}
        .tree_wet {{ filter: drop-shadow(0 0 5px rgba(0,0,0,0.3)); }}
        .tree_snow::after {{ content: "❄️"; position: absolute; top: -10px; left: 10px; font-size: 1.5rem; }}
        @keyframes sway {{ 0% {{ transform: rotate(-3deg); }} 100% {{ transform: rotate(3deg); }} }}


        /* ---------------------------------- */
        /* 4. 스트림릿 카드 및 콘텐츠 레이어 (z-index 관리 핵심) */
        /* ---------------------------------- */
        
        /* [핵심] 모든 스트림릿 블록 콘텐츠를 배경보다 앞으로 가져오기 */
        [data-testid="stVerticalBlock"] {{
            position: relative;
            z-index: 10 !important; /* 배경(-1, -2)보다 훨씬 앞으로 */
        }}

        /* 메인 텍스트 스타일 */
        .main-title {{ text-align: center; font-size: 2.3rem; font-weight: bold; color: #1e272e; position: relative; text-shadow: 0 2px 4px rgba(255,255,255,0.5); }}
        .sub-title {{ text-align: center; color: #2f3542; margin-bottom: 25px; position: relative; text-shadow: 0 1px 2px rgba(255,255,255,0.5); }}
        
        /* 반투명 글래스모피즘 카드 레이아웃 (선명도 및 가독성 극대화) */
        .weather-card {{
            background: rgba(255, 255, 255, 0.85); /* 투명도를 살짝 낮춰 글씨 선명도 업 */
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 22px;
            box-shadow: 0px 8px 24px rgba(0, 0, 0, 0.06);
            border: 1px solid rgba(255, 255, 255, 0.5);
            margin-bottom: 20px;
            position: relative;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}
        .weather-card:hover {{
            transform: translateY(-3px);
            box-shadow: 0px 12px 30px rgba(0, 0, 0, 0.1);
        }}
        
        /* 인포그래픽 그리드 및 반응형 */
        .info-grid {{ display: flex; justify-content: space-between; gap: 12px; margin-top: 15px; flex-wrap: wrap; }}
        .info-box {{
            flex: 1 1 45%; /* 모바일에서 2개씩 배치되도록 설정 */
            background: rgba(255, 255, 255, 0.6); border-radius: 14px; padding: 12px;
            text-align: center; box-shadow: 0 4px 10px rgba(0,0,0,0.02);
            min-width: 120px;
        }}
        .info-icon {{ font-size: 1.8rem; margin-bottom: 4px; }}
        .info-title {{ font-size: 0.8rem; color: #57606f; margin-bottom: 3px; }}
        .info-value {{ font-size: 1rem; font-weight: bold; color: #2f3542; }}
        
        /* 미세먼지 등 게이지 바 */
        .bar-container {{ background: #dee2e6; border-radius: 10px; height: 6px; margin-top: 8px; overflow: hidden; }}
        .bar-fill {{ background: {dust_color}; height: 100%; border-radius: 100px; transition: width 1s ease-in-out; }}

        /* 하이라이트 텍스트 */
        .highlight {{ color: #ff4757; font-weight: bold; }}
        
        /* 반응형 폰트 크기 조절 (모바일 우선) */
        @media (max-width: 768px) {{
            .main-title {{ font-size: 1.8rem; }}
            .sub-title {{ font-size: 0.9rem; }}
            .weather-card {{ padding: 15px; }}
            .info-icon {{ font-size: 1.5rem; }}
            .info-value {{ font-size: 0.9rem; }}
        }}
    </style>
""", unsafe_allow_html=True)

# 실시간 기후 요소 오브젝트(태양, 구름, 비, 눈, 나무 등) 배경층에 주입
st.markdown(current_objects, unsafe_allow_html=True)

# ------------------------------------------
# 1단계 코드 끝. 2단계 코드로 이어집니다.
# ------------------------------------------
# ==========================================
# 6. 상단 대시보드 타이틀 및 헤더 구성
# ==========================================
st.markdown("<h1 class='main-title'>📍 방배동 날씨 동화 세계</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>실시간 대기질 및 기온 연동 애니메이션 인포그래픽</p>", unsafe_allow_html=True)

# 7. 중앙 날씨 캐릭터 Lottie 애니메이션 매핑 및 출력
lottie_motion = load_lottieurl(lottie_url)
if lottie_motion:
    # 카드 레이어 위로 안전하게 출력하기 위한 래퍼 디브 적용
    st.markdown("<div style='position:relative; z-index:10; text-align:center;'>", unsafe_allow_html=True)
    st_lottie(lottie_motion, height=180, key="center_lottie_final")
    st.markdown("</div>", unsafe_allow_html=True)


# ==========================================
# 8. 현재 기온 메인 정보 카드 출력
# ==========================================
# 낮과 밤에 따라 카드 상단 아이콘 문구를 다르게 매핑
time_icon = "🌙 밤 기온" if is_night else "☀️ 낮 기온"
st.markdown(f"""
    <div class='weather-card' style='text-align: center;'>
        <h2 style='margin: 0; color: #2f3542;'>🌡️ 현재 방배동: {temp}°C</h2>
        <p style='margin: 5px 0 0 0; color: #57606f; font-size: 1.1rem;'>현재 상태: <b>{weather_desc}</b> ({time_icon})</p>
    </div>
""", unsafe_allow_html=True)


# ==========================================
# 9. 실시간 대기 환경 및 일출·일몰 인덱스 카드 출력
# ==========================================
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
                <div class='bar-container'>
                    <div class='bar-fill' style='width: {"30%" if "좋음" in dust or "보통" in dust else "85%"};'></div>
                </div>
            </div>
            <div class='info-box'>
                <div class='info-icon'>👁️</div>
                <div class='info-title'>가시거리</div>
                <div class='info-value'>{visibility}</div>
                <div class='bar-container'>
                    <div class='bar-fill' style='background:#70a1ff; width: 90%;'></div>
                </div>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)


# ==========================================
# 10. 기온별 스마트 코디 큐레이션 가이드 카드 출력
# ==========================================
card_content = ""
if temp >= 28:
    card_content = "☀️ <b>한여름 폭염 날씨예요! 무더위를 조심하세요.</b><br>👉 추천 코디: <span class='highlight'>민소매, 반팔티, 린넨 쇼츠, 선글라스</span>"
elif 23 <= temp < 28:
    card_content = "🌤️ <b>산뜻하고 가벼운 여름 기온이에요. 활동하기 좋습니다.</b><br>👉 추천 코디: <span class='highlight'>반팔 셔츠, 슬림 면바지, 오픈형 샌들</span>"
elif 20 <= temp < 23:
    card_content = "🍃 <b>선선하고 부드러운 봄/가을 온도대입니다. 딱 좋은 날씨!</b><br>👉 추천 코디: <span class='highlight'>옥스퍼드 셔츠, 니트조끼, 데님 팬츠</span>"
elif 17 <= temp < 20:
    card_content = "🧥 <b>일교차가 가파릅니다. 입고 벗기 편한 겉옷을 챙기세요.</b><br>👉 추천 코디: <span class='highlight'>맨투맨, 후디, 가디건 레이어링</span>"
elif 12 <= temp < 17:
    card_content = "🍂 <b>찬 기운이 옷깃을 가르는 쌀쌀한 환절기입니다. 감기 조심!</b><br>👉 추천 코디: <span class='highlight'>울 재킷, 트렌치 코트, 도톰한 니트</span>"
elif 9 <= temp < 12:
    card_content = "💨 <b>외풍이 강하니 여러 겹 레이어드룩이 제격입니다.</b><br>👉 추천 코디: <span class='highlight'>야상 점퍼, 도톰한 헤비 니트, 기모바지</span>"
elif 5 <= temp < 9:
    card_content = "🥶 <b>서리가 내리는 초겨울 추위 시즌이에요! 방한에 신경 쓰세요.</b><br>👉 추천 코디: <span class='highlight'>롱코트, 무스탕 재킷, 다운 패딩, 발열내의</span>"
else:
    card_content = "❄️ <b>동파 사고를 조심해야 하는 겨울 한파 침공 기온입니다!</b><br>👉 추천 코디: <span class='highlight'>롱패딩, 방한 목도리, 귀도리, 장갑 필수</span>"

st.markdown(f"""
    <div class='weather-card' style='font-size: 1.15rem; line-height: 1.9; color: #2f3542;'>
        <h4 style='margin-top:0; color:#1e272e; font-size:1.2rem;'>👗 오늘의 방배동 맞춤 코디 큐레이션</h4>
        {card_content}
    </div>
""", unsafe_allow_html=True)
