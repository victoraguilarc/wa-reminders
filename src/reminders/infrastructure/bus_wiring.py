from src.common.infrastructure.context_builder import AppContextBuilder


def wire_handlers():
    app_context = AppContextBuilder.from_env()
    domain_context, bus = app_context.domain, app_context.bus
