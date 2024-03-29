from unittest.mock import Mock

import twitter_bot.jobs
from lyrics_mixer.song_titles_parser import (SongTitlesParser, SongTitlesSplitter)
from lyrics_mixer.tests.fixtures.mixer import mixed_lyrics
from twitter_bot.twitter import MentionHistory, Composer
from twitter_bot.tests.fixtures import tweet

tweet_parser = SongTitlesParser(SongTitlesSplitter())
lyrics_mixer = Mock()
reply_cursor = Mock()


def test_job_tweet_random_lyrics(mixed_lyrics):
    twitter_api = Mock()
    composer = Mock()

    lyrics_mixer.mix_two_random_lyrics.return_value = mixed_lyrics

    twitter_bot.jobs.tweet_random_lyrics(twitter_api, lyrics_mixer, composer)

    composer.tweet.assert_called_with(mixed_lyrics)


def test_job_reply_to_mentions(tweet, mixed_lyrics):
    twitter_api = Mock()

    twitter_api.mentions_since.return_value = [tweet]

    lyrics_mixer.mix_random_lyrics_by_artists.return_value = mixed_lyrics

    composer = Composer(twitter_api, tweet_parser, lyrics_mixer)

    mention_history = MentionHistory(twitter_api, reply_cursor)

    twitter_bot.jobs.reply_to_mentions(mention_history, composer)

    twitter_api.reply_tweet_with.assert_called_with(tweet, str(mixed_lyrics))
    reply_cursor.point_to.assert_called_with(tweet)