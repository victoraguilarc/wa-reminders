from dataclasses import dataclass
from typing import List, Optional

import requests

from src.common.domain.enums.tenants import WhatsappSessionStatus
from src.common.domain.entities.wa_session import (
    WhatsappSession,
    WhatsappAccount,
    WhatsappSessionQRCode,
    WhatsappSessionWebhook,
)
from src.tenants.domain.services.wa_session_manager import (
    WhatsappSessionManager,
)


@dataclass
class HttpWhatsappSessionManager(WhatsappSessionManager):
    api_hostanme: str
    api_key: str

    def create_session(
        self,
        session_id: str,
        session_name: str,
        webhooks: List[WhatsappSessionWebhook] = None,
    ) -> WhatsappSession:
        webhooks = webhooks or []
        response = requests.post(
            url=f'{self.api_hostanme}/api/sessions',
            headers=self._get_headers(),
            json={
                'name': session_name,
                'start': True,
                'config': {
                    'metadata': {
                        'session.id': session_id,
                    },
                    'proxy': None,
                    'debug': False,
                    'noweb': {
                        'store': {
                            'enabled': True,
                            'fullSync': False
                        }
                    },
                    'webhooks': [
                        webhook.to_dict
                        for webhook in webhooks
                    ],
                },
            },
        )
        response.raise_for_status()
        response_json = response.json()

        return WhatsappSession(
            session_name=response_json['name'],
            status=WhatsappSessionStatus.from_value(response_json['status']),
            config=response_json['config'],
        )

    def get_auth_qr(self, session_name: str) -> WhatsappSessionQRCode:
        value_format = 'raw'
        response = requests.get(
            url=f'{self.api_hostanme}/api/{session_name}/auth/qr?format={value_format}',
            headers=self._get_headers(),
        )
        response.raise_for_status()
        response_json = response.json()

        return WhatsappSessionQRCode(
            session_name=session_name,
            format=value_format,
            value=response_json['value'],
        )


    def get_session(self, session_name: str) -> Optional[WhatsappSession]:
        try:
            response = requests.get(
                url=f'{self.api_hostanme}/api/sessions/{session_name}',
                headers=self._get_headers(),
            )
            response.raise_for_status()
            response_json = response.json()

            return self._build_session(response_json)
        except requests.exceptions.HTTPError as exc:
            if exc.response.status_code == 404:
                return None
            raise exc


    def update_session(self, instance: WhatsappSession) -> WhatsappSession:
        response = requests.put(
            url=f'{self.api_hostanme}/api/sessions/{instance.session_name}',
            headers=self._get_headers(),
            json={'config': instance.config},
        )
        response.raise_for_status()
        response_json = response.json()

        return self._build_session(response_json)

    def delete_session(self, session_name: str):
        response = requests.delete(
            url=f'{self.api_hostanme}/api/sessions/{session_name}',
            headers=self._get_headers(),
        )
        response.raise_for_status()

    def _get_headers(self) -> dict:
        return {
            'accept': 'application/json',
            'X-Api-Key': self.api_key,
            'Content-Type': 'application/json',
        }


    @classmethod
    def _build_session(cls, response_json: dict) -> WhatsappSession:
        me_json = response_json.get('me', {})
        return WhatsappSession(
            session_name=response_json['name'],
            status=WhatsappSessionStatus.from_value(response_json['status']),
            config=response_json['config'],
            me=(
                WhatsappAccount(
                    id=me_json.get('id'),
                    push_name=me_json.get('pushName'),
                ) if response_json.get('me') else None
            ),
        )
