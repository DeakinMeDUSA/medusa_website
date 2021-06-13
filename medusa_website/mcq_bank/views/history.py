from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from medusa_website.mcq_bank.models import History


class HistoryView(TemplateView):
    template_name = "mcq_bank/history.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(HistoryView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(HistoryView, self).get_context_data(**kwargs)
        history, c = History.objects.get_or_create(user=self.request.user)
        context["cat_scores"] = history.list_all_cat_scores
        context["sessions"] = history.sessions.all()
        print(f"history.sessions = {history.sessions}")
        return context
