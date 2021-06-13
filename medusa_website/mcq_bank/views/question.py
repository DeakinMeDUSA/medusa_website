from rest_framework import generics
from vanilla import DetailView

from medusa_website.mcq_bank.models import Question

from ..serializers import QuestionSerializer


class QuestionDetailView(DetailView):
    model = Question
    template_name = "mcq_bank/question_detail.html"
    context_object_name = "question"
    lookup_field = "id"
    # def get_context_data(self, **kwargs):
    #     context = super(QuestionDetail, self).get_context_data(**kwargs)
    #     context["questions"] = context["quiz_session"].questions.all()
    #     context["answers"] = context["quiz_session"].answers.all()
    #     print(context)
    #     return context


class QuestionListCreateView(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class QuestionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    lookup_url_kwarg = "id"
