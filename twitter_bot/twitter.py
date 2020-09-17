import tweepy
import logging
from os import environ


logger = logging.getLogger()


def create_tweepy_api():
    auth = tweepy.OAuthHandler(
        environ['TWITTER_CONSUMER_KEY'], environ['TWITTER_CONSUMER_SECRET'])
    auth.set_access_token(
        environ['TWITTER_ACCESS_TOKEN'], environ['TWITTER_ACCESS_TOKEN_SECRET'])

    return tweepy.API(auth)


class TwitterApi:
    MAX_TWEET_LENGTH = 280

    def __init__(self, api):
        self.api = api

    def mentions_since(self, since_id):
        tweets = tweepy.Cursor(self.api.mentions_timeline, since_id).items()
        return self.mentions(tweets)

    def mentions(self, tweets):
        mentions = filter(
            lambda tweet: tweet.in_reply_to_status_id is None, tweets)
        return map(lambda mention: Tweet(self, mention), mentions)

    def update_status(self, text):
        self.api.update_status(text[:self.MAX_TWEET_LENGTH])

    def reply_tweet_with(self, origin_tweet, reply_text):
        self.api.update_status(
            status=reply_text[:self.MAX_TWEET_LENGTH], in_reply_to_status_id=origin_tweet.id)


class Tweet:
    def __init__(self, twitter_api, tweet):
        self.api = twitter_api
        self.id = tweet.id
        self.tweet = tweet
        self.username = tweet.user.screen_name
        self.text = tweet.text

    def reply_with(self, reply_text):
        try:
            self.api.reply_tweet_with(self.tweet, reply_text)
        except Exception as e:
            logger.error(e)

    def __str__(self):
        return f"Author: @{self.username}, Text: {self.text}"


class TweetReply:
    def __init__(self, tweet):
        self.tweet = tweet

    def parse_with(self, tweet_parser):
        return ParsedTweet(self.tweet, tweet_parser.parse(self.tweet.text))


class ParsedTweet:
    def __init__(self, tweet, parsed_data_from_tweet):
        self.tweet = tweet
        self.parsed_data_from_tweet = parsed_data_from_tweet

    def compose_reply(self, lyrics_mixer):
        lyrics = self.parsed_data_from_tweet.mix_using(lyrics_mixer)
        return ComposedReply(self.tweet, lyrics)


class ComposedReply:
    def __init__(self, origin_tweet, reply_text):
        self.origin_tweet = origin_tweet
        self.id = origin_tweet.id
        self.text = str(reply_text)

    def send(self):
        logger.info(f"Replying to tweet: {self.origin_tweet}")
        self.origin_tweet.reply_with(self.text)

    def __eq__(self, other):
        return self.origin_tweet == other.origin_tweet and self.text == other.text