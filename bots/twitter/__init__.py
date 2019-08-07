#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import multiprocessing
from bots.twitter import follow, retweet


# Using apscheduler in favor of multiprocessing
# retweet_bot = multiprocessing.Process(
#     name='retweet_bot', target=retweet.start
# )
# follow_bot = multiprocessing.Process(
#     name='follow_bot', target=follow.start
# )
