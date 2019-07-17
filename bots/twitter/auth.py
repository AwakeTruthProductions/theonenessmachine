#!/usr/bin/env python3

import json
import logging
import tweepy
from utils.aws import ssm

logger = logging.getLogger()


def initalize_auth():
    raw_creds = ssm.get_secure_parameter('oneness-machine-twitter-access')
    t_creds = json.loads(raw_creds)
    consumer_key = t_creds['consumer_key']
    consumer_secret = t_creds['consumer_secret']
    access_token = t_creds['access_token']
    access_token_secret = t_creds['access_token_secret']

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(
        auth, wait_on_rate_limit=True,
        wait_on_rate_limit_notify=True
    )
    try:
        api.verify_credentials()
    except Exception as e:
        logger.error("Error creating API", exc_info=True)
        raise e
    logger.info("API created")
    return api

if __name__ == "__main__":
    initalize_auth()
