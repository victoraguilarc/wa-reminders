# -*- coding: utf-8 -*-

from dataclasses import dataclass

from src.common.domain.entities.user import User


@dataclass
class ProfilePresenter(object):
    instance: User

    @property
    def to_dict(self):
        return {
            'email': self.instance.email,
            'first_name': self.instance.first_name,
            'paternal_surname': self.instance.paternal_surname,
            'maternal_surname': self.instance.maternal_surname,
            'photo': self.instance.photo_url,
            'tenants': [],
        }
