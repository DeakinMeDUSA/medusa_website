import django_tables2 as tables
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.html import format_html
from django.views.generic import TemplateView

from medusa_website.mcq_bank.models import History


class CategoryProgressTable(tables.Table):
    class Meta:
        attrs = {
            "class": "table tablesorter-metro-dark",  # Sorting is handled by js to avoid refresh
            "id": "category-progress-table",
        }
        exclude = ("id",)

    name = tables.Column(verbose_name="Category", orderable=False)
    cat_qs_num = tables.Column(verbose_name="Nº questions total", empty_values=(), orderable=False)
    attempted_num = tables.Column(verbose_name="Nº questions attempted", empty_values=(), orderable=False)
    cat_average_score = tables.Column(verbose_name="Attempts correct avg (%)", empty_values=(), orderable=False)

    def render_name(self, value, record):
        if value != "OVERALL":
            cat_url = f'{reverse("mcq_bank:question_list")}?category={record["id"]}'
            return format_html(f'<a href="{cat_url}">{value}</a>')
        else:
            return format_html(f"<b>{value}</b>")

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

    def render_id(self, value, record):
        session_url = reverse("mcq_bank:quiz_session_detail", kwargs={"id": record["id"]})
        return format_html(f'<a href="{session_url}">{value}</a>')


class HistoryView(TemplateView, LoginRequiredMixin):
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
