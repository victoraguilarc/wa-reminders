import csv
from dataclasses import dataclass
from decimal import Decimal
from io import StringIO
from typing import List

from src.common.domain.enums.users import TenantCustomerStatus
from src.common.domain.interfaces.services import UseCase
from src.common.helpers.time import TimeUtils
from src.users.domain.types.import_item import TenantCustomerImportItem


@dataclass
class TenantCustomerImportItemsParser(UseCase):
    document: StringIO

    def execute(self) -> List[TenantCustomerImportItem]:
        import_items: List[TenantCustomerImportItem] = []
        document_file = csv.DictReader(self.document)
        row: dict
        for row in document_file:
            import_items.append(
                TenantCustomerImportItem(
                    alias=row.get('alias'),
                    first_name=self._get_or_none(row, 'first_name'),
                    paternal_surname=self._get_or_none(row, 'paternal_surname'),
                    maternal_surname=self._get_or_none(row, 'maternal_surname'),
                    email=self._get_or_none(row, 'email'),
                    dial_code=self._get_or_none(row, 'dial_code'),
                    phone_number=row.get('phone_number'),
                    status=(
                        TenantCustomerStatus.from_value(row.get('status'))
                        if self._get_or_none(row, 'status')
                        else TenantCustomerStatus.ACTIVE
                    ),
                    created_at=(
                        TimeUtils.instance_datetime_from_string(row.get('created_at'))
                        if self._get_or_none(row, 'created_at')
                        else None
                    ),
                    finishes_at=(
                        TimeUtils.instance_datetime_from_string(row.get('finishes_at'))
                        if self._get_or_none(row, 'finishes_at')
                        else None
                    ),
                    num_passes=self._get_or_none(row, 'num_passes'),
                    plan_alias=self._get_or_none(row, 'plan_alias'),
                    initial_amount=(
                        Decimal(row.get('initial_amount'))
                        if self._get_or_none(row, 'initial_amount')
                        else None
                    ),
                )
            )
        return import_items

    @classmethod
    def _get_or_none(cls, data: dict, key: str):
        return data.get(key, '').strip() if bool(data.get(key)) else None
