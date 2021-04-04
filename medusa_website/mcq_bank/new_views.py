from django.contrib.auth.mixins import LoginRequiredMixin
from vanilla import DetailView, ListView

from medusa_website.mcq_bank.models import Question, QuizSession


class QuizSessionListView(ListView, LoginRequiredMixin):
    model = QuizSession
    template_name = "mcq_bank/session_history.html"
    context_object_name = "quiz_sessions"


class QuizSessionDetail(DetailView):
    model = QuizSession
    template_name = "mcq_bank/quiz_session_detail.html"
    context_object_name = "quiz_session"
    lookup_field = "id"

    def get_context_data(self, **kwargs):
        context = super(QuizSessionDetail, self).get_context_data(**kwargs)
        context["questions"] = context["quiz_session"].questions.all()
        context["answers"] = context["quiz_session"].answers.all()
        print(context)
        return context


class QuestionDetail(DetailView):
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


# def post(self, request, *args, **kwargs):
#     sitting: Sitting = self.get_object()
#
#     q_to_toggle = request.POST.get("qid", None)
#     if q_to_toggle:
#         q = Question.objects.get(id=int(q_to_toggle))
#         if int(q_to_toggle) in sitting.get_incorrect_questions:
#             sitting.remove_incorrect_question(q)
#         else:
#             sitting.add_incorrect_question(q)
#
#     return self.get(request)
#
# def get_context_data(self, **kwargs):
#     context = super(QuizMarkingDetail, self).get_context_data(**kwargs)
#     context["questions"] = context["sitting"].get_questions(with_answers=True)
#     return context

#
#
# class QuizSessionView(FormView):
#     form_class = QuestionForm
#     template_name = "mcq_bank/question.html"
#     result_template_name = "mcq_bank/result.html"
#     single_complete_template_name = "mcq_bank/single_complete.html"
#
#     @method_decorator(login_required)
#     def dispatch(self, request, *args, **kwargs):
#         self.quiz_session = QuizSession.objects.get_current_session(user=User)
#         if self.quiz_session is None:
#             return render(request, self.single_complete_template_name)
#
#         return super(QuizSessionView, self).dispatch(request, *args, **kwargs)
#
#     def get_form(self, *args, **kwargs):
#
#         self.question = self.quiz_session.current_question
#         self.progress = self.quiz_session.progress
#
#         form_class = self.form_class
#
#         return form_class(**self.get_form_kwargs())
#
#     def get_form_kwargs(self):
#         kwargs = super(QuizSessionView, self).get_form_kwargs()
#
#         return dict(kwargs, question=self.question)
#
#     def form_valid(self, form):
#
#         self.form_valid_user(form)
#         if self.quiz_session.remaining_questions.count() == 0:
#             return self.final_result_user()
#
#         self.request.POST = {}
#
#         return super(QuizSessionView, self).get(self, self.request)
#
#     def get_context_data(self, **kwargs):
#         context = super(QuizSessionView, self).get_context_data(**kwargs)
#         context["question"] = self.question
#         context["quiz_session"] = self.quiz_session
#         if hasattr(self, "previous"):
#             context["previous"] = self.previous
#         if hasattr(self, "progress"):
#             context["progress"] = self.progress
#         return context
#
#     def form_valid_user(self, form):
#         # progress, c = Progress.objects.get_or_create(user=self.request.user)
#         guess = form.cleaned_data["answers"]
#         answer = Answer.objects.get(id=guess)
#
#         # if self.quiz.answers_at_end is not True:
#         self.previous = {
#             "previous_answer": answer,
#             "previous_outcome": answer.correct,
#             "previous_question": self.question,
#             "answers": self.question.get_answers(),
#         }
#         # else:
#         #     self.previous = {}
#
#         self.quiz_session.add_user_answer(answer=answer)
#
#     def final_result_user(self):
#         results = {
#             "quiz_session": self.quiz_session,
#             "score": self.quiz_session.get_current_score,
#             "max_score": self.quiz_session.get_max_score,
#             "percent": self.quiz_session.get_percent_correct,
#             "previous": self.previous,
#         }
#
#         self.sitting.mark_quiz_complete()
#
#         if self.quiz.answers_at_end:
#             results["questions"] = self.sitting.get_questions(with_answers=True)
#             results["incorrect_questions"] = self.sitting.get_incorrect_questions
#
#         if self.quiz.exam_paper is False:
#             self.sitting.delete()
#
#         return render(self.request, self.result_template_name, results)
