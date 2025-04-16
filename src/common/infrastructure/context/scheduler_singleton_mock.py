# -*- coding: utf-8 -*-

from unittest.mock import MagicMock

from apscheduler.schedulers.blocking import BlockingScheduler

from src.common.helpers.singlenton import SingletonMeta


class MockSchedulerSingleton(metaclass=SingletonMeta):
    instance: BlockingScheduler = MagicMock()
