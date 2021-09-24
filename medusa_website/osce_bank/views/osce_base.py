from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import RedirectView, TemplateView

from medusa_website.osce_bank.models import OSCEHistory, OSCEStation
from medusa_website.osce_bank.views.history import CategoryProgressTable


class OSCEIndexRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False
    query_string = False
    pattern_name = "osce_bank:index"


class OSCEIndexView(LoginRequiredMixin, TemplateView):
    template_name = "osce_bank/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        history, c = OSCEHistory.objects.get_or_create(user=self.request.user)
        # context["category_progress_table"] = CategoryProgressTable(history.category_progress)
        return context
