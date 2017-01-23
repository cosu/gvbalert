import attr

from parsing import extract_event_type, extract_lines, extract_ride_type, extract_reason, remove_links, extract_destination

DISTURBANCE = {'en': ['disturbance'], 'nl': ['verstoring']}
DELAY = {'en': ['delay'], 'nl': ['langzaam', 'vertraging', 'dienstregeling']}
CROWDED = {'en': 'crowded', 'nl': ['druk']}
RECOVERED = {'en': 'recovered', 'nl': ''}
UNKNOWN = {'en': 'n/a', 'nl': ['n/a']}
OTHER = {'en': 'other', 'nl': ['other']}
DETOUR = {'en': 'detour', 'nl': ['omleiding']}
EVENT_TYPES = [DISTURBANCE, DELAY, CROWDED, RECOVERED, UNKNOWN, DETOUR]


@attr.s
class Tweet(object):
    event_type = attr.ib()
    text = attr.ib()
    created_at = attr.ib()
    id = attr.ib()
    lines = attr.ib()
    ride_type = attr.ib()
    destination = attr.ib()
    reason = attr.ib()

    @classmethod
    def from_tweet(cls, tweet):
        """
        :param tweet:  the tweet
        :type
        :return:
        :rtype Tweet
        """

        cleaned_text = remove_links(tweet.text.lower())
        event_type = extract_event_type(cleaned_text)
        reason = extract_reason(cleaned_text)
        lines = extract_lines(cleaned_text)
        ride_type = extract_ride_type(cleaned_text)
        destination = extract_destination(cleaned_text)

        return cls(created_at=tweet.created_at,
                   id=tweet.id,
                   text=tweet.text,
                   event_type=event_type,
                   reason=reason,
                   lines=lines,
                   ride_type=ride_type,
                   destination=destination)
