import logging
from lyrics_mixer.lyrics_mixer import MixedLyrics

logger = logging.getLogger(__name__)


def tweet_random_lyrics(twitter_api, lyrics_mixer):
    logger.info('Tweeting random lyrics')

    mixed_lyrics = lyrics_mixer.mix_two_random_lyrics()

    if mixed_lyrics.has_content():
        try:
            twitter_api.update_status(str(mixed_lyrics))
        except:
            logger.error('Skipping tweet.', exc_info=True)


def reply_to_mentions(mention_history, composer):
    # TODO: rename since_last_persisted to since_last_replied ?
    mentions = mention_history.since_last_persisted()

    for mention in mentions:
        composer.reply(mention)
        mention_history.add(mention)

