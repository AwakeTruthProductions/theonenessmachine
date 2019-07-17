#!/usr/bin/env python
# theonenessmachine/bots/follow.py

import tweepy
import logging
from bots.twitter.auth import initalize_auth
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def follow_back(api):
    logger.info('Getting followers')
    for follower in tweepy.Cursor(api.followers).items():
        if not follower.following:
            logger.info(f'Now following {follower.name}')
            follower.follow()


def start():
    api = initalize_auth()
    while True:
        follow_back(api)
        logger.info("Waiting...")
        time.sleep(60)

if __name__ == "__main__":
    start()
