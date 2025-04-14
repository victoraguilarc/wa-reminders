# -*- coding: utf-8 -*-

from src.common.domain.enums.locales import Language
from src.common.domain.enums.notifications import NotificationTemplateCategory

DEFAULT_NOTIFICATION_TEMPLATES = {
    NotificationTemplateCategory.PENDING_INVOICE_REMINDER: {
        Language.ES: (
            'Hola, recuerda que este {deadline} debes renovar tu registro a:  "{class_name}."'
            ' El monto a pagar es {invoice_price}! '
        ),
        Language.EN: (
            'Hello, remember that this {deadline} you need to renew your membership to your {class_name}'
            ' The amount to pay is {invoice_price} '
        ),
    }
}
