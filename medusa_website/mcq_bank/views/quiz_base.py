from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import RedirectView, TemplateView

from medusa_website.mcq_bank.models import History, QuizSession
from medusa_website.mcq_bank.views.history import CategoryProgressTable


class IndexRedirectView(RedirectView, LoginRequiredMixin):
    permanent = False
    query_string = False
    pattern_name = "mcq_bank:quiz_index"


class QuizIndexView(TemplateView, LoginRequiredMixin):
    template_name = "mcq_bank/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        history, c = History.objects.get_or_create(user=self.request.user)
        context["category_progress_table"] = CategoryProgressTable(history.category_progress)
        context["has_current_session"] = True if QuizSession.get_current(self.request.user) else False
        return context
