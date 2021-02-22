import pytest

import songs.tests.song_factory as song_factory
from lyrics_mixer.lyrics_mixer import LineInterleaveLyricsMix

line_interleave_mix = LineInterleaveLyricsMix()

@pytest.fixture
def lyrics_mix():
    return line_interleave_mix

@pytest.fixture
def mixed_song1_song2():
    song1 = song_factory.create_stairway_to_heaven()
    song2 = song_factory.create_born_to_be_wild() 
    return line_interleave_mix.mix(song1, song2)