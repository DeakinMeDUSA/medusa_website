from django.conf import settings
from django.shortcuts import render
from django.utils import timezone
from django.views.generic import TemplateView
from rest_framework import generics
from rest_framework.request import Request

from medusa_website.mcq_bank.models import Answer, Question, Record

from ..users.admin import User
from .exceptions import AnswerRecordNotValid, UserNotValid
from .serializers import AnswerSerializer, QuestionSerializer, RecordSerializer


def index(request):
    return render(request, "mcq_bank/index.html", {"debug": settings.DEBUG})


class QuestionListCreate(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class QuestionRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    lookup_url_kwarg = "id"


class AnswerRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    lookup_url_kwarg = "id"


class AnswersList(generics.ListAPIView):
    serializer_class = AnswerSerializer

    def get_queryset(self):
        queryset = Answer.objects.all()
        question_id = self.request.query_params.get("question_id", None)
        if question_id is not None:
            queryset = queryset.filter(question_id=question_id)
        return queryset


class RecordHistory(generics.ListAPIView):
    serializer_class = RecordSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Record.objects.filter(user=user)
        question_id = self.request.query_params.get("question_id", None)
        if question_id is not None:
            queryset = queryset.filter(question__id=question_id)
        return queryset


class RecordCreate(generics.CreateAPIView):
    queryset = Record.objects.all()
    serializer_class = RecordSerializer

    def create(self, request: Request, *args, **kwargs):
        print(f"request.data = {request.data}")
        user_id = request.data.get("user")
        question = request.data.get("question")
        answer = request.data.get("answer")
        if question is None or answer is None:
            raise AnswerRecordNotValid()

        try:
            User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise UserNotValid(f"Could not find user for user id = {user_id}")

        request.data["timestamp"] = timezone.now()

        return super().create(request, *args, **kwargs)


class AnswerCreate(generics.CreateAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer


class IndexView(TemplateView):
    template_name = "mcq_bank/index.html"
