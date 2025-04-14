from dataclasses import dataclass
from typing import Optional

import pydenticon

from src.common.application.queries.resources import GenerateIdenticonQuery
from src.common.domain.messaging.queries import QueryHandler


@dataclass
class GenerateIdenticonHandler(QueryHandler):
    def execute(
        self,
        query: GenerateIdenticonQuery,
    ) -> Optional[bytes]:
        padding = (50, 50, 50, 50)
        background = "rgb(239,239,239)"
        foreground = [
            "rgb(26,188,156)",
            "rgb(52,152,219)",
            "rgb(155,89,182)",
            "rgb(52,73,94)",
            "rgb(241,196,15)",
            "rgb(230,126,34)",
            "rgb(231,76,60)",
            "rgb(127,140,141)",
            "rgb(108,92,231)",
            "rgb(232,67,147)",
        ]
        generator = pydenticon.Generator(
            rows=5, columns=5,
            background=background,
            foreground=foreground,
        )
        return generator.generate(
            query.label, 240, 240,
            padding=padding,
        )




