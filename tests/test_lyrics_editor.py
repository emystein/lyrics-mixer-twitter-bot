import pytest
from app.lyrics_merge import LyricsEditor
from app.song import Song
from app.lyrics import Lyrics

@pytest.fixture
def lyrics_editor():
    return LyricsEditor()

def test_merge_with_same_number_of_paragraphs(lyrics_editor):
    song1 = Song('artist1', 'title1', 'lyrics 1 first paragraph\n\nlyrics 1 second paragraph')
    song2 = Song('artist2', 'title2', 'lyrics 2 first paragraph\n\nlyrics 2 second paragraph')
    merged_lyrics = lyrics_editor.merge(song1, song2)
    assert merged_lyrics.paragraphs == ['lyrics 1 first paragraph', 'lyrics 2 first paragraph',
                             'lyrics 1 second paragraph', 'lyrics 2 second paragraph']


def test_merge_with_first_lyrics_with_2_paragraphs_and_second_lyrics_with_1_paragraph(lyrics_editor):
    song1 = Song('artist1', 'title1', 'lyrics 1 first paragraph\n\nlyrics 1 second paragraph')
    song2 = Song('artist2', 'title2', 'lyrics 2 first paragraph')
    merged_lyrics = lyrics_editor.merge(song1, song2)
    assert merged_lyrics.paragraphs == ['lyrics 1 first paragraph', 'lyrics 2 first paragraph']


def test_merge_with_first_lyrics_with_1_paragraph_and_second_lyrics_with_2_paragraphs(lyrics_editor):
    song1 = Song('artist1', 'title1', 'lyrics 1 first paragraph')
    song2 = Song('artist2', 'title2', 'lyrics 2 first paragraph\n\nlyrics 2 second paragraph')
    merged_lyrics = lyrics_editor.merge(song1, song2)
    assert merged_lyrics.paragraphs == ['lyrics 1 first paragraph', 'lyrics 2 first paragraph']
