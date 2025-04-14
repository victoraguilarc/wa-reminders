from django.views import View

from src.common.domain.context.bus import BusContext
from src.common.domain.context.domain import DomainContext
from src.common.infrastructure.context_builder import AppContextBuilder


class ActionView(View):
    domain_context: DomainContext
    bus_context: BusContext

    invalid_template_name = 'actions/common/invalid_pending_action.html'

    def setup(self, request, *args, **kwargs):
        app_context = AppContextBuilder.from_env()
        self.domain_context, self.bus_context = app_context.domain, app_context.bus
        super().setup(request, *args, **kwargs)
