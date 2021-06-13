from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView, TemplateView

from medusa_website.mcq_bank.models import Quiz


class QuizIndexView(TemplateView):
    template_name = "mcq_bank/index.html"


class QuizListView(ListView):
    template_name = "mcq_bank/quiz_list.html"

    queryset = Quiz.objects.filter(draft=False)
    # def get_queryset(self):
    #     queryset = super(QuizListView, self).get_queryset()
    #     return queryset.filter(draft=False)


class QuizDetailView(DetailView):
    model = Quiz

    template_name = "mcq_bank/quiz_detail.html"

    def get(self, request, *args, **kwargs):
        self.quiz = get_object_or_404(Quiz, url=self.kwargs["quiz_name"])

        self.object = self.quiz
        if self.object.draft and not request.user.has_perm("quiz.change_quiz"):
            raise PermissionDenied

        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)
