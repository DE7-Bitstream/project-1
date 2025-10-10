import csv
import os
import re
import datetime
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.dateparse import parse_date

from hitmakers.models import Creator, Album, Song, SongCreator, YearlyChart

# csv 파일 베이스 디렉토리 경로 및 파일명 정의
BASE_CSV_PATH = os.path.join('dataframes', 'hitmakers')
CSV_FILENAMES = {
    "creators": "melon_creator_info.csv",
    "albums": "melon_album_info.csv",
    "songs": "melon_song_info.csv",
    "yearly_charts": "melon_yearly_top100.csv",
}

def split_ids(cell):
    """ '|' 로 연결된 작사가, 작곡가, 편곡자 문자열을 리스트로 변환 """
    if not cell:
        return []
    return [c.strip() for c in cell.split("|") if c.strip()]


class Command(BaseCommand):
    help = "hitmakers 관련 데이터 전체 초기화 후 CSV에서 재적재"

    def handle(self, *args, **options):
        # CSV 파일 존재 여부 체크
        for key, fname in CSV_FILENAMES.items():
            path = os.path.join(BASE_CSV_PATH, fname)
            if not os.path.exists(path):
                self.stdout.write(self.style.ERROR(f"missing {path}"))
                return

        with transaction.atomic():
            # ==========================================================
            # 0) 기존 데이터 전체 삭제
            # 삭제 순서 중요 (FK 제약 역순)
            # ==========================================================
            self.stdout.write(self.style.WARNING("기존 데이터 삭제 중..."))

            YearlyChart.objects.all().delete()
            SongCreator.objects.all().delete()
            Song.objects.all().delete()
            Album.objects.all().delete()
            Creator.objects.all().delete()

            self.stdout.write(self.style.SUCCESS("✅ 기존 데이터 초기화 완료"))

            # ==========================================================
            # 1) Creators
            # ==========================================================
            creators_path = os.path.join(BASE_CSV_PATH, CSV_FILENAMES["creators"])
            with open(creators_path, encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for r in reader:
                    Creator.objects.create(
                        creator_id=r["creator_id"].strip(),
                        name=r.get("creator_name", "").strip() or "Unknown",
                    )
            self.stdout.write(self.style.SUCCESS("✅ creators imported"))

            # ==========================================================
            # 2) Albums
            # ==========================================================
            albums_path = os.path.join(BASE_CSV_PATH, CSV_FILENAMES["albums"])
            with open(albums_path, encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for r in reader:
                    Album.objects.create(
                        album_id=r["album_id"].strip(),
                        release_date=datetime.datetime.strptime(r.get("release_date", "").strip(), '%Y.%m.%d').date(),
                        genre=r.get("genre", "").strip(),
                        distributor=r.get("distributor", "").strip(),
                        entertainment=r.get("enterteinment", "").strip(),  # note: csv key spelling
                    )
            self.stdout.write(self.style.SUCCESS("✅ albums imported"))

            # ==========================================================
            # 3) Songs + SongCreator relations
            # ==========================================================
            songs_path = os.path.join(BASE_CSV_PATH, CSV_FILENAMES["songs"])
            with open(songs_path, encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for r in reader:
                    # album_id foreign 값 받아오기
                    album = None
                    album_id = r.get("album_id", "").strip()
                    if album_id:
                        album = Album.objects.filter(album_id=album_id).first()
                    # title에 '19금'으로 시작되는 부분 전처리
                    # 전처리 조건 : '19금'으로 시작 + 연속 공백 2개 이상
                    TITLE_REMOVE_PATTERN = re.compile(r'^19금\s{2,}.*')
                    title_str = r.get("title", "").strip()
                    if TITLE_REMOVE_PATTERN.match(title_str):
                        title_str = re.sub(r'^19금\s{2,}', '', title_str)
                    song = Song.objects.create(
                        song_id=r["song_id"].strip(),
                        album=album,
                        singer=r.get("singer", "").strip(),
                        title=title_str,
                        genre=r.get("genre", "").strip(),
                    )

                    # SongCreator 관계 생성
                    for col, role in (
                        ("lyricists", SongCreator.ROLE_LYRICIST),
                        ("composers", SongCreator.ROLE_COMPOSER),
                        ("arrangers", SongCreator.ROLE_ARRANGER),
                    ):
                        for cid in split_ids(r.get(col, "")):
                            creator = Creator.objects.filter(creator_id=cid).first()
                            if not creator:
                                creator = Creator.objects.create(creator_id=cid, name="Unknown")
                            SongCreator.objects.create(song=song, creator=creator, role=role)

            self.stdout.write(self.style.SUCCESS("✅ songs + songcreators imported"))

            # ==========================================================
            # 4) YearlyCharts
            # ==========================================================
            charts_path = os.path.join(BASE_CSV_PATH, CSV_FILENAMES["yearly_charts"])
            with open(charts_path, encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for r in reader:
                    year_text = r.get("year", r.get("year_text", "")).strip()
                    year = int(year_text)
                    song = Song.objects.filter(song_id=r["song_id"].strip()).first()
                    album = Album.objects.filter(album_id=r.get("album_id", "").strip()).first()

                    if not song:
                        self.stdout.write(
                            self.style.WARNING(f"⚠️ song not found for chart row: {r.get('song_id')}")
                        )
                        continue

                    YearlyChart.objects.create(
                        year=year,
                        rank=int(r.get("rank", 0)),
                        song=song,
                        album=album,
                    )
            self.stdout.write(self.style.SUCCESS("✅ yearly_charts imported"))
