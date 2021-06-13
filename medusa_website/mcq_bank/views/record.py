from django.utils import timezone
from rest_framework import generics
from rest_framework.request import Request

from medusa_website.mcq_bank.models import Record

from ...users.admin import User
from ..exceptions import AnswerRecordNotValid, UserNotValid
from ..serializers import RecordSerializer


class RecordHistoryView(generics.ListAPIView):
    serializer_class = RecordSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Record.objects.filter(user=user)
        question_id = self.request.query_params.get("question_id", None)
        if question_id is not None:
            queryset = queryset.filter(question__id=question_id)
        return queryset


class RecordCreateView(generics.CreateAPIView):
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
