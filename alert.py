from __future__ import absolute_import
from __future__ import print_function

import logging
import os
import boto3

import tweepy

from tweet import Tweet

logger = logging.getLogger(__name__)

s3 = boto3.resource('s3')
ses = boto3.client('ses')

CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
CONSUMER_KEY = os.environ['CONSUMER_KEY']
MAX_ITEMS = 100

BUCKET = os.environ['BUCKET']
KEY = os.environ['KEY']
TO_ADDRESS = os.environ['TO_ADDRESS'].split(',')
FROM_ADDRESS = os.environ('FROM_ADDRESS')

def get_latest_id():
    val = '849546118659593216'
    try:
        obj = s3.Object(BUCKET, KEY)
        val = obj.get()['Body'].read().decode('utf-8')
    except:
        pass

    return val


def set_latest_id(id):
    obj = s3.Object(BUCKET, KEY)
    obj.put(Body=str(id))


def configure_logging():
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.setLevel(logging.INFO)
    logger.addHandler(ch)


def build_api():
    consumer_key = CONSUMER_KEY
    consumer_secret = CONSUMER_SECRET
    auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
    api = tweepy.API(auth)
    return api


def is_interesting_tweet(tweet):
    return '26' in tweet.lines


def parse_timeline(api):
    results = []
    last_id = get_latest_id()
    for status in tweepy.Cursor(api.user_timeline, screen_name='GVB_actueel', since_id=last_id or 0).items(MAX_ITEMS):
        t = Tweet.from_tweet(status)
        if is_interesting_tweet(t):
            logger.debug("interesting: %r", t)
            results.append(t)
    if results:
        set_latest_id(results[0].id)
    return results


def get_body(results):
    lines = []
    for t in results:
        lines.append("{created_at} Type:{type} Details: {text} Affects: {lines}"
                     .format(created_at=t.created_at, type=t.event_type, text=t.text, lines=','.join(t.lines)))
    return "\n".join(lines)


def handler(event, context):
    logger.debug(event)
    configure_logging()
    api = build_api()
    results = parse_timeline(api)

    if results:
        ses.send_email(
            Source=FROM_ADDRESS,
            Destination={
                'ToAddresses': TO_ADDRESS
            },
            Message={
                'Subject': {
                    'Data': 'new gvb tweets: ' + str(len(results))
                },
                'Body': {
                    'Text': {
                        'Data': get_body(results)
                    }
                }
            }
        )

    return 'OK'


if __name__ == '__main__':
    configure_logging()
    api = build_api()
    results = parse_timeline(api)