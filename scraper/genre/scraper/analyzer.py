from konlpy.tag import Hannanum
from collections import Counter
import re

class LyricsAnalyzer:
    """가사 텍스트 분석 클래스"""
    
    def __init__(self):
        try:
            self.hannanum = Hannanum()
        except:
            print("Hannanum 초기화 실패. KoNLPy가 설치되어 있는지 확인하세요.")
            self.hannanum = None
        
        # 제외할 불용어 리스트
        self.stopwords = set([
            '것', '수', '등', '들', '안', '속', '때', '더', '곳', '중',
            '나', '너', '저', '우리', '그', '이', '저', '여기', '거기',
            '내', '네', '제', '뭐', '왜', '어디', '언제', '누구', '것들',
            '겁', '번', '잘', '막', '좀', '뭔', '날', '널', '걸', '건',
        ])
    
    def extract_nouns(self, text):
        """명사만 추출"""
        if not self.hannanum or not text or not text.strip():
            return []
        
        # 텍스트 전처리
        text = self._preprocess_text(text)
        
        try:
            # 형태소 분석으로 명사 추출
            nouns = self.hannanum.nouns(text)
            
            # 필터링: 한 글자 단어 제거, 불용어 제거
            filtered_nouns = [
                word for word in nouns 
                if len(word) > 1 and word not in self.stopwords
            ]
            
            return filtered_nouns
        except Exception as e:
            print(f"명사 추출 중 오류: {e}")
            return []
    
    def extract_morphs(self, text, pos_tags=['N', 'V', 'A']):
        """
        특정 품사만 추출
        N: 명사 (Noun)
        V: 동사 (Verb)
        A: 형용사 (Adjective)
        """
        if not self.hannanum or not text or not text.strip():
            return []
        
        text = self._preprocess_text(text)
        
        try:
            # 형태소 분석
            morphs = self.hannanum.pos(text)
            
            # 지정된 품사만 필터링
            result = []
            for word, pos in morphs:
                # 첫 글자가 지정된 품사에 해당하는지 확인
                if any(pos.startswith(tag) for tag in pos_tags):
                    if len(word) > 1 and word not in self.stopwords:
                        result.append((word, pos))
            
            return result
        except Exception as e:
            print(f"형태소 추출 중 오류: {e}")
            return []
    
    def get_word_frequency(self, words, top_n=100):
        """단어 빈도수 계산"""
        if not words:
            return []
        
        counter = Counter(words)
        return counter.most_common(top_n)
    
    def analyze_lyrics_batch(self, lyrics_list):
        """여러 가사를 한 번에 분석 - 명사만"""
        all_nouns = []
        
        for lyrics in lyrics_list:
            nouns = self.extract_nouns(lyrics)
            all_nouns.extend(nouns)
        
        return self.get_word_frequency(all_nouns)
    
    def analyze_by_pos(self, lyrics_list, pos_tags=['N']):
        """품사별로 분석"""
        all_words = []
        
        for lyrics in lyrics_list:
            words = self.extract_morphs(lyrics, pos_tags)
            all_words.extend([word for word, _ in words])
        
        return self.get_word_frequency(all_words)
    
    def _preprocess_text(self, text):
        """텍스트 전처리"""
        # 특수문자 제거 (한글, 영문, 숫자, 공백만 남김)
        text = re.sub(r'[^\w\s가-힣ㄱ-ㅎㅏ-ㅣ]', ' ', text)
        # 여러 공백을 하나로
        text = re.sub(r'\s+', ' ', text)
        # 앞뒤 공백 제거
        text = text.strip()
        return text
    
    def get_statistics(self, lyrics_list):
        """가사 통계 정보 반환"""
        total_songs = len(lyrics_list)
        if total_songs == 0:
            return {
                'total_songs': 0,
                'total_characters': 0,
                'total_words': 0,
                'unique_words': 0,
                'avg_words_per_song': 0,
            }
        
        total_chars = sum(len(lyrics) for lyrics in lyrics_list)
        
        all_nouns = []
        for lyrics in lyrics_list:
            all_nouns.extend(self.extract_nouns(lyrics))
        
        unique_words = len(set(all_nouns))
        total_words = len(all_nouns)
        
        return {
            'total_songs': total_songs,
            'total_characters': total_chars,
            'total_words': total_words,
            'unique_words': unique_words,
            'avg_words_per_song': round(total_words / total_songs, 2) if total_songs > 0 else 0,
        }
    
    def compare_genres(self, genre_lyrics_dict):
        """
        장르별 가사 비교 분석
        genre_lyrics_dict: {'hiphop': [lyrics1, lyrics2, ...], 'kpop': [...]}
        """
        comparison = {}
        
        for genre, lyrics_list in genre_lyrics_dict.items():
            stats = self.get_statistics(lyrics_list)
            word_freq = self.analyze_lyrics_batch(lyrics_list)
            
            comparison[genre] = {
                'statistics': stats,
                'top_words': word_freq[:20],  # 상위 20개 단어
            }
        
        return comparison