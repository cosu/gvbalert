import datetime
import unittest

from tweet import Tweet


class MockTweet(object):
    def __init__(self, id, created_at, text):
        self.id = id
        self.created_at = created_at
        self.text = text


class TestTweet(unittest.TestCase):
    def test_parse(self):
        raw_text = 'Verstoring bus 48 en 65 door extreme drukte. Kijk op https://t.co/VtTXVEd4vF'

        response = MockTweet(**{'text': raw_text,
                                'id': 1,
                                'created_at': datetime.datetime.now()
                                })

        t = Tweet.from_tweet(response)

        self.assertEqual(['48', '65'], t.lines)
