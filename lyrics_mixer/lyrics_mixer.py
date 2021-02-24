import logging
from itertools import groupby

from songs.model import Song, Lyrics

logger = logging.getLogger()


class LyricsMixer:
    def __init__(self, lyrics_library, lyrics_mix_strategy):
        self.lyrics_library = lyrics_library
        self.lyrics_mix_strategy = lyrics_mix_strategy

    def mix_two_random_lyrics(self):
        return self.mix_lyrics(ManyLyricsPicker(
            RandomLyricsPicker(), 
            RandomLyricsPicker()))

    def mix_random_lyrics_by_artists(self, artist1, artist2):
        return self.mix_lyrics(ManyLyricsPicker(
            RandomByArtistLyricsPicker(artist1), 
            RandomByArtistLyricsPicker(artist2)))

    def mix_two_specific_lyrics(self, artist1, title1, artist2, title2):
        return self.mix_lyrics(ManyLyricsPicker(
            SpecificLyricsPicker(artist1, title1), 
            SpecificLyricsPicker(artist2, title2)))

    def mix_lyrics(self, lyrics_picker):
        try:
            songs = lyrics_picker.pick(self.lyrics_library)
            return self.lyrics_mix_strategy.mix(songs[0], songs[1])
        except Exception:
            logger.error('Returning empty lyrics.', exc_info=True)
            return MixedLyrics.empty()


class ManyLyricsPicker:
    def __init__(self, *pickers):
        self.pickers = pickers

    def pick(self, library):
        return list(map(lambda picker: picker.pick(library), self.pickers))


class RandomLyricsPicker:
    def pick(self, library):
        return library.get_random_lyrics()


class RandomByArtistLyricsPicker:
    def __init__(self, artist):
        self.artist = artist

    def pick(self, library):
        return library.get_random_lyrics_by_artist(self.artist)


class SpecificLyricsPicker:
    def __init__(self, artist, title):
        self.artist = artist
        self.title = title

    def pick(self, library):
        return library.get_lyrics(self.artist, self.title)


class LineInterleaveLyricsMix:
    def mix(self, song1, song2):
        # see: https://stackoverflow.com/questions/7946798/interleave-multiple-lists-of-the-same-length-in-python
        lines = [val for pair in zip(
            song1.lyrics.lines(), song2.lyrics.lines()) for val in pair]
        # see https://stackoverflow.com/questions/14529523/python-split-for-lists
        paragraphs = ['\n'.join(list(l)) for k, l in groupby(
            lines, lambda x: x == '') if not k]
        return MixedLyrics(song1, song2, lines, paragraphs)


class ParagraphInterleaveLyricsMix:
    def mix(self, song1, song2):
        # see: https://stackoverflow.com/questions/7946798/interleave-multiple-lists-of-the-same-length-in-python
        paragraphs = [val for pair in zip(
            song1.lyrics.paragraphs(), song2.lyrics.paragraphs()) for val in pair]
        lines = [lines.split('\n') for lines in paragraphs]
        # see: https://stackoverflow.com/questions/952914/how-to-make-a-flat-list-out-of-list-of-lists
        flat_list = [item for sublist in lines for item in sublist]
        return MixedLyrics(song1, song2, flat_list, paragraphs)


class MixedLyrics(Lyrics):
    @staticmethod
    def empty():
        return MixedLyrics(Song.none(), Song.none(), '', '')

    def __init__(self, song1, song2, lines, paragraphs):
        self.song1, self.song2, self.lines, self.paragraphs = song1, song2, lines, paragraphs
        self.songs = [self.song1, self.song2]
        self.artist1 = self.song1.artist
        self.artist2 = self.song2.artist
        self.title = f"{song1.artist} - {song1.title}, {song2.artist} - {song2.title}"
        self.text = '\n\n'.join(paragraphs)

    def __str__(self):
        return self.title + '\n\n' + self.text

    def has_content(self):
        return self != MixedLyrics.empty()
