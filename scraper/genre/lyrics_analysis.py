# 안전한 스트리밍 저장 (곡 단위) - Jupyter에서 사용 권장
import os
import re
import gc
import time
import pandas as pd
from konlpy.tag import Okt
from tqdm.notebook import tqdm

# 설정
INPUT_CSV = r"C:\Users\yoond\OneDrive\바탕 화면\MyProject\lyrics_analysis\melon_genre_steady_songs_with_lyrics.csv"
OUT_CSV   = r"C:\Users\yoond\Web Scrapping\csv\melon_song_words.csv"
BATCH_SLEEP = 0.05   # 각 곡 처리 후 짧게 쉬기
SAVE_EVERY = 50      # 이 값만큼 곡 처리할 때마다 파일에 한번 더 flush(안전성)

EN_STOP = {"the","and","a","to","of","in","on","for","you","i","me","my","is","it","we","be","that","this"}

okt = Okt()

def extract_words_light(lyrics: str):
    """
    한 곡을 안전하게 처리:
     - 한국어: Okt로 명사/동사/형용사만 추출, 한 글자 단어 제거
     - 영어: 간단 토큰화 (정규표현식), 소문자화, 짧은 불용어 제거
    반환: list of words (str)
    """
    if not isinstance(lyrics, str) or not lyrics.strip():
        return []

    # 1) 간단 정리: HTML 잔여/특수문자 제거(한글+영어+공백만 남김)
    text = re.sub(r"[^가-힣A-Za-z\s]", " ", lyrics)

    words = []

    # 한국어 처리 (곡 단위)
    ko_text = " ".join(re.findall(r"[가-힣]+", text))
    if ko_text:
        try:
            tokens = okt.pos(ko_text, stem=True)
            for w, pos in tokens:
                if pos in ("Noun","Verb","Adjective") and len(w) > 1:
                    words.append(w)
        except Exception:
            # Konlpy 가끔 에러 날 수 있으므로 방어
            pass

    # 영어 처리 (가볍게)
    en_text = " ".join(re.findall(r"[A-Za-z]+", text))
    if en_text:
        en_tokens = re.findall(r"[A-Za-z]{2,}", en_text)  # 두 글자 이상만
        for t in en_tokens:
            t = t.lower()
            if t not in EN_STOP:
                words.append(t)

    return words

df = pd.read_csv(INPUT_CSV)
os.makedirs(os.path.dirname(OUT_CSV), exist_ok=True)

processed_ids = set()
if os.path.exists(OUT_CSV):
    try:
        tmp = pd.read_csv(OUT_CSV, usecols=["songId"])
        processed_ids = set(tmp["songId"].astype(str).unique())
        print(f"[INFO] 이미 처리된 songId {len(processed_ids)}개 발견 — 재시작 시 스킵합니다.")
    except Exception:
        processed_ids = set()

write_header = not os.path.exists(OUT_CSV)

row_buffer = []
count = 0
total = len(df)
for idx, row in tqdm(df.iterrows(), total=total, desc="Processing songs"):
    try:
        song_id = str(row.get("songId",""))
        if song_id == "" or song_id in processed_ids:
            continue  # 이미 처리했거나 id 없음

        title = row.get("title","")
        artist = row.get("artist","")
        genre = row.get("genre","")
        lyrics = row.get("lyrics","")

        words = extract_words_light(lyrics)
        if not words:
            # 가사 없거나 추출 단어 없으면 빈 상태로 기록하지 않고 넘어감 (필요하면 기록하도록 조정 가능)
            print(f"[WARN] 단어 없음 → {title} - {artist}")
            processed_ids.add(song_id)
            continue

        for w in words:
            row_buffer.append({"songId": song_id, "title": title, "artist": artist, "genre": genre, "word": w})

        count += 1
        processed_ids.add(song_id)

        # 배치마다 파일에 append(디스크에 flush)
        if count % SAVE_EVERY == 0 or len(row_buffer) > 5000:
            df_chunk = pd.DataFrame(row_buffer)
            df_chunk.to_csv(OUT_CSV, mode="a", header=write_header, index=False, encoding="utf-8-sig")
            write_header = False
            row_buffer = []
            # 강제 GC
            gc.collect()
            print(f"[INFO] {count}곡 처리 — 중간저장 완료")

        # 각 곡 사이에 아주 짧게 쉼 (부하 완화)
        time.sleep(BATCH_SLEEP)

    except Exception as e:
        print(f"[ERROR] songId={row.get('songId','?')} 에러: {e}")
        # 에러 나도 멈추지 않도록 continue

# 루프 종료 시 남은 버퍼 저장
if row_buffer:
    df_chunk = pd.DataFrame(row_buffer)
    df_chunk.to_csv(OUT_CSV, mode="a", header=write_header, index=False, encoding="utf-8-sig")
    row_buffer = []
    gc.collect()

print("전체 처리 완료. 출력 파일:", OUT_CSV)

# 워드클라우드 시각화 추가
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# 저장된 단어 CSV에서 단어만 추출
words_df = pd.read_csv(OUT_CSV)
all_words = words_df['word'].tolist()
text = ' '.join(all_words)

# 워드클라우드 생성 (폰트 경로를 절대경로로 지정)
font_path = os.path.join(os.path.dirname(__file__), 'Pretendard-ExtraBold.otf')
wc = WordCloud(font_path=font_path, width=800, height=400, background_color='white').generate(text)

plt.figure(figsize=(15, 7))
plt.imshow(wc, interpolation='bilinear')
plt.axis('off')
plt.title('가사 워드클라우드', fontsize=20)
plt.savefig('wordcloud.png', bbox_inches='tight')  # 이미지 파일로 저장
plt.show()
print('워드클라우드 이미지가 wordcloud.png로 저장되었습니다.')
