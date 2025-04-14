# -*- coding: utf-8 -*-

from src.common.domain.enums.locales import Days


def test_days():
    choices = Days.choices()
    assert str(choices) == str(
        [
            (0, 'MONDAY'),
            (1, 'TUESDAY'),
            (2, 'WEDNESDAY'),
            (3, 'THURSDAY'),
            (4, 'FRIDAY'),
            (5, 'SATURDAY'),
            (6, 'SUNDAY'),
        ]
    )
