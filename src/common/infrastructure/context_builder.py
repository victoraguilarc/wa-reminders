from dataclasses import dataclass

from apscheduler.schedulers.blocking import BlockingScheduler
from django.conf import settings

from src.common.domain.context.bus import BusContext
from src.common.domain.context.domain import DomainContext
from src.common.domain.enums.config import AppConfigEnv
from src.common.helpers.singlenton import SingletonMeta


@dataclass
class AppContext(metaclass=SingletonMeta):
    domain: DomainContext
    bus: BusContext
    scheduler: BlockingScheduler


class AppContextBuilder(object):
    @classmethod
    def from_env(cls, env: str = settings.ENV) -> AppContext:
        environment = AppConfigEnv.from_value(env)
        if environment.is_production or environment.is_development:
            from src.common.infrastructure.context.bus_singleton import BusSingleton
            from src.common.infrastructure.context.domain_singleton import DomainSingleton
            from src.common.infrastructure.context.scheduler_singleton import SchedulerSingleton

            return AppContext(
                domain=DomainSingleton.instance,
                bus=BusSingleton.instance,
                scheduler=SchedulerSingleton.instance,
            )

        elif environment.is_testing:
            from src.common.infrastructure.context.bus_singleton_mock import MockBusSingleton
            from src.common.infrastructure.context.domain_singleton_mock import MockDomainSingleton
            from src.common.infrastructure.context.scheduler_singleton_mock import MockSchedulerSingleton

            return AppContext(
                domain=MockDomainSingleton.instance,
                bus=MockBusSingleton.instance,
                scheduler=MockSchedulerSingleton.instance,
            )
        else:
            raise NotImplementedError('Invalid environment: {}'.format(env))
