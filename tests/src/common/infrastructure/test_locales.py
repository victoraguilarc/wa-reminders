import pytest
from freezegun import freeze_time

from src.common.domain.enums.locales import TimeZone
from src.common.domain.interfaces.locales import LocaleService
from src.common.helpers.time import TimeUtils
from src.common.infrastructure.time_formatter import RawTimeFormatter


@pytest.mark.skip
class RawTimeFormatterTests(object):
    @staticmethod
    def test_to_natural_time_one_year_ago_exactly():
        local_now = TimeUtils.local_datetime(
            year=2021,
            month=12,
            day=20,
            hour=12,
            minute=30,
            time_zone=str(TimeZone.MEXICO_CITY),
        )
        to_compare = TimeUtils.local_datetime(
            year=2020,
            month=12,
            day=20,
            hour=12,
            minute=30,
            time_zone=str(TimeZone.MEXICO_CITY),
        )

        with freeze_time(local_now):
            formatter = RawTimeFormatter(
                time_zone=TimeZone.MEXICO_CITY,
                locale_service=LocaleService(),
            )
            result = formatter.to_natural_time(to_compare)

        assert result == '1 years ago'

    @staticmethod
    def test_to_natural_more_than_one_year_ago():
        local_now = TimeUtils.local_datetime(
            year=2021,
            month=12,
            day=20,
            hour=12,
            minute=30,
            time_zone=str(TimeZone.MEXICO_CITY),
        )
        to_compare = TimeUtils.local_datetime(
            year=2019,
            month=6,
            day=10,
            hour=10,
            minute=10,
            time_zone=str(TimeZone.MEXICO_CITY),
        )

        with freeze_time(local_now):
            formatter = RawTimeFormatter(
                time_zone=TimeZone.MEXICO_CITY,
                locale_service=LocaleService(),
            )
            result = formatter.to_natural_time(to_compare)

        assert result == '2 years ago'

    @staticmethod
    def test_to_natural_time_one_month_ago_exactly():
        local_now = TimeUtils.local_datetime(
            year=2021,
            month=12,
            day=20,
            hour=12,
            minute=30,
            time_zone=str(TimeZone.MEXICO_CITY),
        )
        to_compare = TimeUtils.local_datetime(
            year=2021,
            month=11,
            day=20,
            hour=12,
            minute=30,
            time_zone=str(TimeZone.MEXICO_CITY),
        )

        with freeze_time(local_now):
            formatter = RawTimeFormatter(
                time_zone=TimeZone.MEXICO_CITY,
                locale_service=LocaleService(),
            )
            result = formatter.to_natural_time(to_compare)

        assert result == '4 weeks ago'

    # @staticmethod
    # def test_to_natural_time_months_ago():
    #     local_now = TimeUtils.local_datetime(
    #         year=2021, month=12, day=20, hour=12, minute=30,
    #         time_zone=TimeZone.MEXICO_CITY.value,
    #     )
    #     to_compare = TimeUtils.local_datetime(
    #         year=2021, month=10, day=10, hour=12, minute=30,
    #         time_zone=TimeZone.MEXICO_CITY.value,
    #     )
    #
    #     with freeze_time(local_now):
    #         formatter = RawTimeFormatter()
    #         result = formatter.to_natural_time(to_compare, TimeZone.MEXICO_CITY.value)
    #
    #     assert result == 'more than 2 months ago'
    #
    # @staticmethod
    # def test_to_natural_time_hours_ago():
    #     pass
    #
    # @staticmethod
    # def test_to_natural_currently():
    #     pass
    #
    # @staticmethod
    # def test_to_natural_in_minutes():
    #     pass
    #
    # @staticmethod
    # def test_to_natural_in_hours():
    #     pass
    #
    # @staticmethod
    # def test_to_natural_in_weeks():
    #     pass
    #
    # @staticmethod
    # def test_to_natural_in_years():
    #     pass
