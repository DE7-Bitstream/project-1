from datetime import datetime, timedelta

def calculate_weeks(year):
    # 1월 1일의 요일 확인
    jan_first = datetime(year, 1, 1)
    jan_first_weekday = jan_first.weekday()  # 0: 월요일, 6: 일요일

    # 해당 연도의 첫째 주 시작일 계산
    # 목요일(3)이 포함되어 있다면 그 주가 첫째 주, 아니면 다음 주 월요일이 첫째 주
    if jan_first_weekday <= 3:  # 월(0), 화(1), 수(2), 목(3)
        start_date = jan_first - timedelta(days=jan_first_weekday)
    else:
        start_date = jan_first + timedelta(days=(7 - jan_first_weekday))

    # 마지막 날짜는 해당 연도의 12월 31일
    end_date = datetime(year, 12, 31)

    weeks = []

    while start_date <= end_date:
        week_start = start_date
        week_end = start_date + timedelta(days=6)

        # 주차 계산 (해당 월의 첫째 주 기준)
        ref_date = week_start + timedelta(days=3)  # 목요일 기준으로 주 소속 결정
        week_year = ref_date.year
        week_month = ref_date.month

        # 해당 월의 첫째 주 계산
        first_day_of_month = datetime(week_year, week_month, 1)
        first_day_weekday = first_day_of_month.weekday()

        if first_day_weekday <= 3:  # 목요일 포함 여부
            month_week1_start = first_day_of_month - timedelta(days=first_day_weekday)
        else:
            month_week1_start = first_day_of_month + timedelta(days=(7 - first_day_weekday))

        week_number_in_month = ((week_start - month_week1_start).days // 7) + 1

        week_start_day = week_start.strftime('%Y%m%d')
        week_end_day = week_end.strftime('%Y%m%d')
        weeks.append((week_year, week_month, week_number_in_month, week_start_day, week_end_day))

        start_date += timedelta(days=7)

    return weeks


if __name__ == "__main__":
    # for debugging
    year = 2022
    weeks = calculate_weeks(year)
    
    for week_year, week_month, week_number_in_month, week_start_day, week_end_day in weeks:
        print(f"{week_year}Y {week_month}M {week_number_in_month}TH: {week_start_day} ~ {week_end_day}")
