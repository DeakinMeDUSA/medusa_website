from django.contrib.auth.mixins import LoginRequiredMixin
from vanilla import CreateView, ListView, UpdateView

from medusa_website.mcq_bank.models import Answer


class AnswerUpdateView(UpdateView, LoginRequiredMixin):
    queryset = Answer.objects.all()
    lookup_url_kwarg = "id"


class AnswersListView(ListView, LoginRequiredMixin):
    def get_queryset(self):
        queryset = Answer.objects.all()
        question_id = self.request.query_params.get("question_id", None)
        if question_id is not None:
            queryset = queryset.filter(question_id=question_id)
        return queryset


class AnswerCreateView(CreateView, LoginRequiredMixin):
    queryset = Answer.objects.all()
