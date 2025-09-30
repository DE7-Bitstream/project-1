import csv
import os
from django.core.management.base import BaseCommand, CommandError
from weekly_chart.models import WeeklyChart

BASE_CSV_PATH = os.path.join('data', 'weekly')
MELON_FUNC = lambda year : f'melon_chart_weekly_{year}.csv'
YEARS = [ 2020, 2021, 2022, 2023, 2024, 2025 ]
#####################

class Command(BaseCommand):
    help = 'weekly_chart 데이터 로드'

    def add_arguments(self, parser):
        # 기존 데이터 삭제 여부
        parser.add_argument(
            '--clear',        
            action='store_true', # 인자 없이 플래그만 있으면 True로 저장
            help='저장 전 기존 데이터 삭제, 기본적으로 False입니다.',
        )
    
    def handle(self, *args, **options):    
        should_clear = options['clear'] if options['clear'] else False

        try:
            if should_clear:
                self.stdout.write(self.style.WARNING('Clearing existing WeeklyChart data...'))
                WeeklyChart.objects.all().delete()
                self.stdout.write(self.style.WARNING('Data cleared.'))
  

            for year in YEARS:
                csv_path = os.path.join(BASE_CSV_PATH, MELON_FUNC(year))
                
                # 파일 존재 여부 확인
                if not os.path.exists(csv_path):
                    raise CommandError(f'File not found at: {csv_path}')

                self.stdout.write(self.style.SUCCESS(f'Starting data loading from: {csv_path}'))

                with open(csv_path, mode='r', encoding='utf-8-sig') as file:
                    reader = csv.DictReader(file)
                    total_rows = 0
                    created_count = 0
                    
                    # bulk_create를 위한 리스트
                    chart_objects = []
                    
                    for row in reader:
                        total_rows += 1
                        
                        # CSV 행 데이터를 모델 필드에 맞게 변환하고 객체 리스트에 추가
                        try:
                            chart_objects.append(WeeklyChart(
                                rank=int(row['rank']),
                                year=int(row['year']),
                                month=int(row['month']),
                                week_number_in_month=int(row['week_number_in_month']),
                                song=row['song_name'],
                                artist=row['song_performer']
                            ))
                            
                        except KeyError as e:
                            # CSV 컬럼 이름이 모델 필드와 다를 경우
                            self.stdout.write(self.style.ERROR(f"Missing column in CSV: {e}"))
                            return
                        except ValueError as e:
                            # 데이터 타입 변환 오류 처리
                            self.stdout.write(self.style.ERROR(f"Data type error on row {total_rows}: {e}. Skipping row."))
                            continue # 건너뛰기


                    # bulk_create를 사용하여 대량 삽입
                    created_objects = WeeklyChart.objects.bulk_create(chart_objects)
                    created_count = len(created_objects)

                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Successfully processed {total_rows} rows. Created {created_count} WeeklyChart entries.'
                        )
                    )

        except Exception as e:
            raise CommandError(f'An error occurred during data loading: {e}')