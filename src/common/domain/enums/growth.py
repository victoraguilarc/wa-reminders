from src.common.domain import BaseEnum


class TenantLeadChannel(BaseEnum):
    MEMBERS_PAGE = 'MEMBERS_PAGE'
    EMAIL = 'EMAIL'
    WHATSAPP = 'WHATSAPP'
    CUSTOMER_REFERRAL = 'CUSTOMER_REFERRAL'


class TenantLeadStage(BaseEnum):
    CREATED = 'CREATED'
    CONTACTED = 'CONTACTED'
    QUALIFIED = 'QUALIFIED'
    IN_NEGOTIATION = 'IN_NEGOTIATION'
    LEAD_WON = 'LEAD_WON'
    LEAD_LOST = 'LEAD_LOST'
