from django.contrib import admin
from .models import Genre, Album, Song, WordFrequency


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['display_name', 'name', 'song_count', 'album_count']
    search_fields = ['display_name', 'name']
    
    def song_count(self, obj):
        return obj.songs.count()
    song_count.short_description = '곡 수'
    
    def album_count(self, obj):
        return obj.albums.count()
    album_count.short_description = '음반 수'


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ['title', 'artist', 'genre', 'year', 'song_count', 'created_at']
    list_filter = ['genre', 'year']
    search_fields = ['title', 'artist']
    ordering = ['-year', 'title']
    
    def song_count(self, obj):
        return obj.songs.count()
    song_count.short_description = '수록곡 수'


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ['title', 'artist', 'genre', 'album', 'year', 'has_lyrics', 'created_at']
    list_filter = ['genre', 'year']
    search_fields = ['title', 'artist']
    ordering = ['-year', 'title']
    
    def has_lyrics(self, obj):
        return bool(obj.lyrics)
    has_lyrics.boolean = True
    has_lyrics.short_description = '가사 유무'


@admin.register(WordFrequency)
class WordFrequencyAdmin(admin.ModelAdmin):
    list_display = ['word', 'genre', 'frequency', 'pos', 'updated_at']
    list_filter = ['genre', 'pos']
    search_fields = ['word']
    ordering = ['-frequency']