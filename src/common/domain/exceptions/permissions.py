from src.common.domain.exceptions.common import BadRequest



class TenantRoleNotFoundError(BadRequest):
    pass


class InvalidPermissionError(BadRequest):
    pass
