#!/usr/bin/env python3
# theonenessmachine/bots/retweet.py

import json
import logging
import time
import tweepy
from bots.twitter.auth import initalize_auth

from requests.exceptions import Timeout, ConnectionError
from requests.packages.urllib3.exceptions import (
    ReadTimeoutError, ProtocolError
)

PER_SESSION_MAX_TWEET_COUNT = 5
WAIT_TIME = 14400  # 4 hours (6 times/day)
# expecting ~30 retweets/day

STREAM_FILTER = [
    ['Oneness'],
    [
        '45655928', '154679666', '2734953286', '14592008', '137542528',
        '43464948', '40059734', '188166216'
    ]
]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RetweetListener(tweepy.StreamListener):
    def __init__(self, api, scheduler=None):
        self.tweet_count = 0
        self.me = api.me()
        self.api = api
        self.scheduler = scheduler

    def on_status(self, tweet):
        logger.info(f'Processing tweet id {tweet.id}')
        if tweet.in_reply_to_status_id is not None or \
                tweet.user.id == self.me.id:  # or tweet.retweeted_status:
                    return
        try:
            tweet.favorite()
            tweet.retweet()
            self.tweet_count += 1
            if self.tweet_count >= PER_SESSION_MAX_TWEET_COUNT:
                logger.info('max tweet per session count reached')
                if self.scheduler:
                    self.scheduler.remove_job('twitter_retweet_bot')
                    logger.info('shutting down twitter_retweet_bot scheduler')
                return False
            else:
                return True
        except Exception as e:
            logger.error('Error on fav and retweet', exc_info=True)

    def on_error(self, status):
        logger.error(status)


def start_stream(stream, **kwargs):
    try:
        logger.info('starting retweet stream')
        stream.filter(**kwargs)
    except ReadTimeoutError:
        stream.disconnect()
        logger.exception('ReadTimeoutError exception')
        start_stream(stream, **kwargs)
    except Exception:
        stream.disconnect()
        logger.exception('Fatal exception. Consult logs.')
        start_stream(stream, **kwargs)


def start(filter_data=STREAM_FILTER, scheduler=None):
    api = initalize_auth()
    logger.info('setting up retweet stream')
    streamListener = RetweetListener(api, scheduler)
    stream = tweepy.Stream(auth=api.auth, listener=streamListener)
    followIds = filter_data[1]
    keywords = filter_data[0]
    start_stream(
        stream, follow=followIds, languages=['en']
    )

if __name__ == '__main__':
    start(filter_data=STREAM_FILTER)
