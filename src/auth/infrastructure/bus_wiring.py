from src.auth.application.handlers.get_user_session_token import GetUserSessionTokenHandler
from src.auth.infrastructure.session_token.jwt_builder import JWTUserSessionTokenBuilder
from src.common.application.queries.auth import GetUserSessionTokenQuery
from src.common.infrastructure.context_builder import AppContextBuilder


def wire_handlers():
    app_context = AppContextBuilder.from_env()
    domain_context, bus = app_context.domain, app_context.bus

    #  Q U E R I E S

    bus.query_bus.subscribe(
        query=GetUserSessionTokenQuery,
        handler=GetUserSessionTokenHandler(
            token_builder=JWTUserSessionTokenBuilder(),
        ),
    )

    #  C O M M A N D S
