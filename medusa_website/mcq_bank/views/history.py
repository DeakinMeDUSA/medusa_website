import django_tables2 as tables
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from medusa_website.mcq_bank.models import History, QuizSession


class CategoryProgressTable(tables.Table):
    class Meta:
        attrs = {
            "class": "table tablesorter-metro-dark",  # Sorting is handled by js to avoid refresh
            "id": "category-progress-table",
        }

    category_name = tables.Column(linkify=False, verbose_name="Category", orderable=False)
    cat_qs_num = tables.Column(verbose_name="Nº questions total", empty_values=(), orderable=False)
    attempted_num = tables.Column(verbose_name="Nº questions attempted", empty_values=(), orderable=False)
    cat_average_score = tables.Column(verbose_name="Attempts correct avg (%)", empty_values=(), orderable=False)

    def render_attempted_num(self, value, record):
        return f"{value} ({record['attempted_percent'] or 0} %)"

    def render_cat_average_score(self, value, record):
        return f"{value or 0} %"


class SessionHistoryTable(tables.Table):
    class Meta:
        attrs = {
            "class": "table tablesorter-metro-dark",  # Sorting is handled by js to avoid refresh
            "id": "session-history-table",
        }

    id = tables.Column(verbose_name="ID", orderable=False)
    is_complete = tables.Column(verbose_name="Is complete", empty_values=(), orderable=False)
    started = tables.Column(verbose_name="Started datetime", empty_values=(), orderable=False)
    finished = tables.Column(verbose_name="Finished datetime", empty_values=(), orderable=False)
    total_session_qs = tables.Column(verbose_name="Nº questions total", empty_values=(), orderable=False)
    attempted = tables.Column(verbose_name="Nº attempted questions", empty_values=(), orderable=False)
    correct_answers = tables.Column(verbose_name="Nº correct answers", empty_values=(), orderable=False)

    def render_correct_answers(self, value, record):
        return f"{value} ({record['correct_answers_percent'] or 0} %)"

    # def render_cat_average_score(self, value, record):
    #     return f"{value or 0} %"


class HistoryView(TemplateView):
    template_name = "mcq_bank/history.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(HistoryView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(HistoryView, self).get_context_data(**kwargs)
        history, c = History.objects.get_or_create(user=self.request.user)
        context["category_progress_table"] = CategoryProgressTable(history.category_progress)
        context["session_history_table"] = SessionHistoryTable(history.session_history)
        return context
