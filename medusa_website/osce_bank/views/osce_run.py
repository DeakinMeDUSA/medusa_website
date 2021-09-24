# from typing import Optional
#
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.http import JsonResponse
# from django.shortcuts import redirect, render
# from django.template import loader
# from django.views.generic import FormView
# from vanilla import DetailView
#
# from medusa_website.osce_bank.models import OSCEHistory, OSCEStation
# from ..forms import OSCEStationForm
# from ...users.models import User
#
#
# class OSCERunView(LoginRequiredMixin, FormView, DetailView):
#     form_class = OSCEStationForm
#     template_name = "osce_bank/osce_station.html"
#     result_template_name = "osce_bank/result.html"
#     session_create_template_name = "osce_bank/osce_session_create.html"
#     single_complete_template_name = "osce_bank/single_complete.html"
#
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.user: Optional[User] = None
#         self.session: Optional[QuizSession] = None
#         self.osce_station: Optional[OSCEStation] = None
#         self.history: Optional[History] = None
#
#     def dispatch(self, request, *args, **kwargs):
#         self.user = self.request.user
#         print(f"User = {self.user}")
#         self.session = QuizSession.get_current(request.user)
#         print(f"Session = {self.session}")
#         if self.session is None:
#             return redirect("osce_bank:quiz_session_create")
#         self.history = self.user.history
#
#         # Set osce_station index to match url if specified
#         if self.request.GET.get("q"):
#             osce_station_index = int(self.request.GET["q"])
#             if osce_station_index < 0 or osce_station_index > self.session.osce_stations.count() - 1:
#                 raise ValueError("Invalid osce_station index specified!")
#             else:
#                 self.session.current_osce_station_index = osce_station_index
#
#             self.session.save()
#
#         return super(QuizTakeView, self).dispatch(request, *args, **kwargs)
#
#     def get_form(self, *args, **kwargs):
#
#         self.osce_station = self.session.current_osce_station
#         self.history = self.session.progress
#
#         form_class = self.form_class
#
#         return form_class(osce_station=self.osce_station, **self.get_form_kwargs())
#
#     # def get_form_kwargs(self):
#     #     kwargs = super(QuizTakeView, self).get_form_kwargs()
#     #
#     #     return dict(kwargs, osce_station=self.osce_station)
#
#     def form_valid(self, form):
#         submitted_answer = self.submit_answer_response(form)
#         if self.session.unanswered_osce_stations.count() == 0:
#             return self.final_result_user()
#
#         answer_response = self.render_answer_response(request=self.request, submitted_answer=submitted_answer)
#         return JsonResponse({"answer_response": answer_response})
#
#     def get_context_data(self, **kwargs):
#         context = super(QuizTakeView, self).get_context_data(**kwargs)
#         context["osce_station"] = self.osce_station
#         context["session"] = self.session
#         if self.session.current_osce_station_response is not None:
#             context["submitted_answer"] = self.session.current_osce_station_response
#
#         return context
#
#     def submit_answer_response(self, form) -> Answer:
#         submitted_answer = Answer.objects.get(id=form.cleaned_data["answers"])
#         self.session.add_user_answer(answer=submitted_answer)
#         return submitted_answer
#
#     def render_answer_response(self, request, submitted_answer) -> str:
#         context = {
#             'submitted_answer': submitted_answer,
#             'osce_station': submitted_answer.osce_station,
#         }
#         return loader.render_to_string("osce_bank/answer_response.html", context=context, request=request)
#
#     def final_result_user(self):
#         results = {
#             "session": self.session,
#             "score": self.session.correct_answers.count(),
#             "max_score": self.session.osce_stations.count(),
#             "percent": self.session.percent_correct,
#         }
#
#         self.session.mark_session_complete()
#         return render(self.request, self.result_template_name, results)
