import pytest
from app.lyrics_merge import RandomLyricsMerger
from app.random_lyrics_downloader import RandomLyricsDownloader
from wikia.random_song_url_parser import WikiaRandomSongUrlParser
from wikia.lyrics_api_adapter import WikiaLyricsApiClient
from app.lyrics_merge import LyricsEditor


def test_merge_random_lyrics_by_artists():
    downloader = RandomLyricsDownloader(WikiaRandomSongUrlParser(), WikiaLyricsApiClient())
    merger = RandomLyricsMerger(downloader, LyricsEditor())
    merged_lyrics = merger.merge_two_random_lyrics()
    assert merged_lyrics.title != ''
    assert merged_lyrics.text != ''
