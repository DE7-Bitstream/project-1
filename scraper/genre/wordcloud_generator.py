from wordcloud import WordCloud
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os
from django.conf import settings
import io
import base64

class WordCloudGenerator:
    """워드클라우드 생성 클래스"""
    
    def __init__(self):
        self.font_path = self._get_korean_font()
        self.genre_colors = {
            'hiphop': 'Reds',
            'indie_rock': 'Blues',
            'kpop': 'RdPu',
        }
    
    def _get_korean_font(self):
        """한글 폰트 경로 찾기"""
        # Windows
        if os.name == 'nt':
            font_paths = [
                'C:/Windows/Fonts/malgun.ttf',  # 맑은 고딕
                'C:/Windows/Fonts/gulim.ttc',   # 굴림
                'C:/Windows/Fonts/batang.ttc',  # 바탕
            ]
        # Mac
        elif os.name == 'posix' and os.uname().sysname == 'Darwin':
            font_paths = [
                '/System/Library/Fonts/AppleSDGothicNeo.ttc',
                '/Library/Fonts/AppleGothic.ttf',
            ]
        # Linux
        else:
            font_paths = [
                '/usr/share/fonts/truetype/nanum/NanumGothic.ttf',
                '/usr/share/fonts/truetype/nanum/NanumBarunGothic.ttf',
            ]
        
        for path in font_paths:
            if os.path.exists(path):
                return path
        
        return None
    
    def generate(self, word_freq_dict, genre='hiphop', width=1200, height=800):
        """
        워드클라우드 생성
        word_freq_dict: {단어: 빈도수} 딕셔너리
        """
        if not word_freq_dict:
            return None
        
        # 장르별 색상 테마
        colormap = self.genre_colors.get(genre, 'viridis')
        
        # 워드클라우드 설정
        wc = WordCloud(
            font_path=self.font_path,
            width=width,
            height=height,
            background_color='white',
            colormap=colormap,
            max_words=150,
            relative_scaling=0.5,
            min_font_size=12,
            prefer_horizontal=0.7,
        )
        
        # 워드클라우드 생성
        wc.generate_from_frequencies(word_freq_dict)
        
        return wc
    
    def save_to_file(self, wordcloud, filepath):
        """워드클라우드를 파일로 저장"""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        plt.figure(figsize=(15, 10))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.tight_layout(pad=0)
        plt.savefig(filepath, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
    
    def get_base64_image(self, wordcloud):
        """워드클라우드를 base64 인코딩된 이미지로 변환"""
        plt.figure(figsize=(15, 10))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.tight_layout(pad=0)
        
        # 이미지를 메모리 버퍼에 저장
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight', facecolor='white')
        buffer.seek(0)
        
        # base64 인코딩
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
        
        return f"data:image/png;base64,{image_base64}"
    
    def generate_comparison(self, word_freq_dicts, genres):
        """
        여러 장르의 워드클라우드를 한 번에 비교
        word_freq_dicts: 장르별 {단어: 빈도수} 딕셔너리 리스트
        genres: 장르 이름 리스트
        """
        num_genres = len(genres)
        fig, axes = plt.subplots(1, num_genres, figsize=(6*num_genres, 6))
        
        if num_genres == 1:
            axes = [axes]
        
        for idx, (word_freq, genre) in enumerate(zip(word_freq_dicts, genres)):
            if word_freq:
                wc = self.generate(word_freq, genre, width=800, height=600)
                if wc:
                    axes[idx].imshow(wc, interpolation='bilinear')
                    axes[idx].set_title(
                        self._get_genre_display_name(genre), 
                        fontproperties=fm.FontProperties(fname=self.font_path, size=20),
                        pad=20
                    )
                    axes[idx].axis('off')
        
        plt.tight_layout()
        
        # base64로 변환
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight', facecolor='white')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
        
        return f"data:image/png;base64,{image_base64}"
    
    def _get_genre_display_name(self, genre):
        """장르 코드를 표시 이름으로 변환"""
        names = {
            'hiphop': '힙합 / 랩',
            'indie_rock': '인디 / 락',
            'kpop': 'K-POP',
        }
        return names.get(genre, genre)