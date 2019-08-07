import logging

from datetime import datetime
from apscheduler.schedulers.background import BlockingScheduler
from bots import twitter, facebook, instagram, image_generator
from utils.banner import banner

logging.basicConfig()
logger = logging.getLogger(__name__).setLevel(logging.DEBUG)


def engage():
    banner.print_banner()
    oneness_scheduler = BlockingScheduler({
        'apscheduler.executors.processpool': {
            'class': 'apscheduler.executors.pool:ProcessPoolExecutor',
            'max_workers': '20'
        },
        'job_defaults': {
            'coalesce': False,
            'executor': 'processpool'
        }
    })

    oneness_scheduler.add_executor('processpool')
    t_retweet = oneness_scheduler.add_job(
        twitter.retweet.start,
        'interval', minutes=60,
        id='twitter_retweet_bot'
    )
    t_follow = oneness_scheduler.add_job(
        twitter.follow.start,
        'interval', minutes=10,
        id='twitter_follow_bot'
    )

    # quoted_im_generator = oneness_scheduler.add_job(
    #     image_generator.quoted_image.start,
    #     'interval', minutes=300,
    #     id='quoted_im_generator',
    #     kwargs={'overlay_flag': True}
    # )

    im_with_quote_generator = oneness_scheduler.add_job(
        image_generator.quoted_image.start,
        'interval', minutes=120,
        id='image_with_quote_generator',
        kwargs={'overlay_flag': False}
    )

    try:
        # oneness_scheduler.start()
        for job in oneness_scheduler.get_jobs():
            job.modify(next_run_time=datetime.now())
        oneness_scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        oneness_scheduler.shutdown()
