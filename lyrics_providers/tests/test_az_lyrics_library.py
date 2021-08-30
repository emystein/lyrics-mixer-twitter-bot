import pytest
from lyrics_providers.azlyrics import AZLyricsLibrary
from songs.model import SongTitle


lyrics_library = AZLyricsLibrary()


@pytest.mark.slow_integration_test
@pytest.mark.vcr()
def test_get_specific_lyrics():
    song_title = SongTitle('Led Zeppelin', 'Stairway to Heaven')

    assert lyrics_library.get_lyrics(song_title).has_lyrics()


@pytest.mark.slow_integration_test
def test_get_random_lyrics():
    assert lyrics_library.get_random_lyrics().has_lyrics()


@pytest.mark.slow_integration_test
def test_get_random_lyrics_by_artist():
    song = lyrics_library.get_random_lyrics_by_artist('Led Zeppelin')

    assert song.title.artist == 'Led Zeppelin'
    assert song.has_lyrics()
