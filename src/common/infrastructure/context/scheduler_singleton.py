from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.jobstores.mongodb import MongoDBJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from loguru import logger
from pymongo import MongoClient

from src.common.helpers.singlenton import SingletonMeta


def instance_scheduler() -> BackgroundScheduler:
    logger.info("\n>>> Creating scheduler instance...\n")
    client = MongoClient(settings.MONGODB_URL)
    jobstores = {
        'default': MongoDBJobStore(client=client, database='apscheduler', collection='jobs')
    }
    executors = {
        'default': ThreadPoolExecutor(20),
    }
    scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors)
    # scheduler = BackgroundScheduler() # use this for debugging
    scheduler.start()
    return scheduler


class SchedulerSingleton(metaclass=SingletonMeta):
    instance: BackgroundScheduler = instance_scheduler()
