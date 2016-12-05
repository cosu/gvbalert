from __future__ import print_function
from __future__ import absolute_import

import tweepy
import pickle
import os
import logging

from gvbalert import tweet

logger = logging.getLogger(__name__)


def configure_logging():
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(ch)


def build_api():
    logger.debug('building api')
    consumer_key = os.getenv('CONSUMER_KEY')
    consumer_secret = os.getenv('CONSUMER_SECRET')
    auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
    api = tweepy.API(auth)
    logger.debug('built api')
    return api


def dump_to_pkl():
    tweets = []
    for status in tweepy.Cursor(api.user_timeline, screen_name='GVB_actueel').items(2000):
        tweets.append(status)
    pickle.dump(tweets, open("tweets.p", "wb"))


def parse_timeline(api):
    i = 0
    logger.debug('starting to parse timeline')
    for status in tweepy.Cursor(api.user_timeline, screen_name='GVB_actueel').items(100):
        t = tweet.Tweet.from_tweet(status)
        if '26' in t.lines:
            i += 1
            logger.debug("%s %s %s %s", t.event_type, t.lines, t.text, t.created_at)
    logger.debug('done parsing %s' % i)


if __name__ == '__main__':
    configure_logging()
    api = build_api()
    parse_timeline(api)
