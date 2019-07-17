import multiprocessing
from bots import twitter, facebook, instagram


def engage():
    twitter.retweet_bot.start()
    twitter.follow_bot.start()
    # facebook.engage()
    # instagram.engage()
