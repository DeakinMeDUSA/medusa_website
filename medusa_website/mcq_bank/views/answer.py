from rest_framework import generics

from medusa_website.mcq_bank.models import Answer

from ..serializers import AnswerSerializer


class AnswerRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    lookup_url_kwarg = "id"


class AnswersListView(generics.ListAPIView):
    serializer_class = AnswerSerializer

    def get_queryset(self):
        queryset = Answer.objects.all()
        question_id = self.request.query_params.get("question_id", None)
        if question_id is not None:
            queryset = queryset.filter(question_id=question_id)
        return queryset


class AnswerCreateView(generics.CreateAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
