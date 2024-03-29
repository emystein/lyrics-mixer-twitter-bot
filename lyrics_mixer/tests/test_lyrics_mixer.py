from unittest.mock import Mock

from lyrics_mixer.lyrics_mix_strategies import LineInterleaveLyricsMix
from lyrics_mixer.lyrics_mixer import LyricsMixer
from songs.tests import song_factory

stairway_to_heaven_lyrics = song_factory.stairway_to_heaven_lyrics()
born_to_be_wild_lyrics = song_factory.born_to_be_wild_lyrics()

expected_lyrics = [stairway_to_heaven_lyrics, born_to_be_wild_lyrics]


class MockLyricsLibrary(Mock):
    def expect_get_random_lyrics(self, *return_lyrics):
        for lyrics in return_lyrics:
            self.get_random_lyrics.return_value = lyrics

    def expect_get_random_lyrics_by_artist(self, *return_lyrics):
        for lyrics in return_lyrics:
            self.get_random_lyrics_by_artist.return_value = lyrics

    def expect_get_lyrics(self, *return_lyrics):
        for lyrics in return_lyrics:
            self.get_lyrics.return_value = lyrics


def test_mix_two_random_lyrics():
    lyrics_library = MockLyricsLibrary()

    mixer = create_mixer(lyrics_library)

    lyrics_library.expect_get_random_lyrics(*expected_lyrics)

    assert mixer.mix_two_random_lyrics().has_content()


def test_mix_random_lyrics_by_artists():
    lyrics_library = MockLyricsLibrary()

    mixer = create_mixer(lyrics_library)

    lyrics_library.expect_get_random_lyrics_by_artist(*expected_lyrics)

    assert mixer.mix_random_lyrics_by_artists('Led Zeppelin', 'Steppenwolf').has_content()


def test_mix_specific_lyrics():
    lyrics_library = MockLyricsLibrary()

    mixer = create_mixer(lyrics_library)

    lyrics_library.expect_get_lyrics(*expected_lyrics)

    assert mixer.mix_specific_lyrics(*expected_lyrics).has_content()


def test_exception_on_mix_lyrics():
    mock_lyrics_picker = Mock()

    mixer = LyricsMixer(MockLyricsLibrary(), LineInterleaveLyricsMix())

    mock_lyrics_picker.pick.side_effect = RuntimeError('Download error')

    assert mixer.mix_lyrics(mock_lyrics_picker).is_empty()


def create_mixer(lyrics_library):
    return LyricsMixer(lyrics_library, LineInterleaveLyricsMix())

