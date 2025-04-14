from dataclasses import dataclass
from datetime import date
from io import FileIO
from typing import Optional

from src.common.domain.enums.locales import Language
from src.common.domain.enums.users import Gender


@dataclass
class DomainPersonMixin(object):
    first_name: Optional[str]
    paternal_surname: Optional[str]
    maternal_surname: Optional[str]
    birth_date: Optional[date]
    gender: Optional[Gender]

    @property
    def display_name(self) -> str:
        _display_name = ''
        if self.first_name:
            _display_name += self.first_name
        if self.paternal_surname:
            _display_name += f' {self.paternal_surname}'
        if self.maternal_surname:
            _display_name += f' {self.maternal_surname}'
        if not _display_name:
            _display_name = '---'
        return _display_name


@dataclass
class DomainProfileMixin(DomainPersonMixin):
    lang: Optional[Language]
    photo: Optional[FileIO]
    photo_url: Optional[str]
