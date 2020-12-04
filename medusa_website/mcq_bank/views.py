from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.template import loader
from django.urls import reverse
from django.views.generic import RedirectView

from medusa_website.mcq_bank.models import Question


def index(request):
    latest_question_list = Question.objects.all()
    context = {"latest_question_list": latest_question_list}
    return render(request, "mcq_bank/index.html", context)


def detail(request, question_id):

    context = {"question_id": question_id}
    return render(request, "mcq_bank/detail.html", context)
