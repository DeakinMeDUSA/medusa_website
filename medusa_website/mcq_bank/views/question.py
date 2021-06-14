from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import generics
from vanilla import CreateView, DetailView, UpdateView

from medusa_website.mcq_bank.models import Question

from ..forms import QuestionCreateForm, QuestionDetailForm
from ..serializers import QuestionSerializer


class QuestionUpdateView(UpdateView, LoginRequiredMixin):
    model = Question
    template_name = "mcq_bank/question_detail.html"
    form_class = QuestionDetailForm
    context_object_name = "question"
    lookup_field = "id"
    # def get_context_data(self, **kwargs):
    #     context = super(QuestionDetail, self).get_context_data(**kwargs)
    #     context["questions"] = context["quiz_session"].questions.all()
    #     context["answers"] = context["quiz_session"].answers.all()
    #     print(context)
    #     return context
    # TODO add handling of staff or author to allow updating, rather than just viewing e.g:
    # def get_form(self, data=None, files=None, **kwargs):
    #     user = self.request.user
    #     if user.is_staff:
    #         return AdminAccountForm(data, files, owner=user, **kwargs)
    #     return AccountForm(data, files, owner=user, **kwargs)


class QuestionCreateView(CreateView, LoginRequiredMixin):
    model = Question
    template_name = "mcq_bank/question_create.html"
    # form_class = QuestionCreateForm
    context_object_name = "question"
    lookup_field = "id"
