# 음악 데이터 분석 플랫폼 🎵

## 📌 프로젝트 개요
대중 음악 정보 시각화 서비스는 Melon에서 스크랩한 정보를 바탕으로 새로운 인사이트를 제공하기 위해 기획되었습니다. 

### 주요 기능
- **장르별 가사 분석**: wordcloud를 통한 시각화
- **계절별 유행 분석**: 계절별 상위 곡 및 장르 확인
- **주간 차트 추이**: 곡별 주간 차트 추이 시각화
- **히트메이커 분석**: 연간 차트 상위곡 제작자 분석

## 🏗️ 프로젝트 구조
```
project-1/
├── scraper/          # 데이터 크롤링 관련 파일
│   ├── genre/        # 장르별 가사 분석
│   ├── monthly/      # 월간 차트
│   ├── weekly_chart/ # 주간 차트
│   └── yearly/       # 연간 차트
│
└── web/              # Django 웹서비스
    ├── bitstream/    # Django 프로젝트 설정
    ├── weekly_chart/ # 주간 차트 앱
    ├── hitmakers/    # 히트메이커 분석 앱
    ├── lyrics/       # 가사 분석 앱
    └── season/       # 계절별 분석 앱
```

## 🛠️ 기술 스택
- **언어**: Python 3.13.x
- **프레임워크**: Django 5.2.6
- **데이터베이스**: SQLite
- **크롤링**: Selenium, Requests, BeautifulSoup4
- **데이터 처리**: Pandas, KoNLPy
- **시각화**: Chart.js, WordCloud, Matplotlib

## 🚀 설치 및 실행 방법

### 1. 환경 설정
```bash
# 프로젝트 클론
git clone <repository-url>
cd project-1

# 가상환경 생성 (권장)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치 - 스크래퍼
cd scraper
pip install -r requirements.txt

# 의존성 설치 - 웹서비스
cd ../web
pip install -r requirements.txt
```

### 2. 데이터 수집 (선택사항)
```bash
cd scraper

# 장르별 가사 데이터 수집
cd genre
python melon_songs.py
python melon_songs_lyrics.py

# 주간 차트 데이터 수집
cd ../weekly_chart
python melon_weekly_crawler.py

# 연간 차트 데이터 수집
cd ../yearly
python melon_yearly_charts.py
```

### 3. 웹서비스 실행
```bash
cd web

# 데이터베이스 마이그레이션
python manage.py makemigrations
python manage.py migrate

# CSV 데이터 로드
python manage.py load_weekly_chart    # 주간 차트
python manage.py load_hitmakers_data  # 히트메이커
python manage.py season_table_create  # 계절별 분석

# 개발 서버 실행
python manage.py runserver
```

서버가 실행되면 브라우저에서 `http://localhost:8000` 접속

## 📊 데이터 흐름
```
Melon 웹사이트
    ↓ (크롤링)
Python 스크래퍼 (Selenium, BeautifulSoup)
    ↓
CSV 파일 저장
    ↓
Django Management Commands
    ↓
SQLite 데이터베이스
    ↓
Django Views & Templates (Chart.js)
    ↓
사용자 웹 브라우저
```

## 🔍 주요 모듈 설명

### Scraper 모듈
- **genre/**: 장르별 스테디셀러 곡 정보 및 가사 수집
- **monthly/**: 월간 TOP 100 차트 데이터 수집
- **weekly_chart/**: 주간 차트 데이터 수집 및 날짜 계산
- **yearly/**: 연도별 차트 TOP 100 수집

### Web 앱
- **weekly_chart**: 주간 차트 추이 시각화
- **hitmakers**: 제작자(작곡가, 작사가, 기획사, 유통사) 분석
- **lyrics**: 장르별 가사 워드클라우드 생성
- **season**: 계절별 유행 장르 및 곡 분석

## ⚠️ 주의사항
- 웹 스크래핑은 해당 사이트의 이용약관을 확인하고 준수해야 합니다
- 과도한 요청은 IP 차단의 원인이 될 수 있으므로 적절한 딜레이를 설정하세요
- 프로덕션 환경 배포 시 `settings.py`의 SECRET_KEY와 DEBUG 설정을 반드시 변경하세요
- KoNLPy 사용을 위해서는 Java JDK 설치가 필요합니다

## 🤝 기여자
프로그래머스 데브코스 7기 1차 6팀

## 📝 라이선스
이 프로젝트는 교육 목적으로 제작되었습니다.
