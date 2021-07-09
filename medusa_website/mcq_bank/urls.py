from django.urls import path, re_path

from .views import (
    HistoryView,
    IndexRedirectView,
    QuestionCreateView,
    QuestionListView,
    QuestionUpdateView,
    QuizIndexView,
    QuizSessionCreateView,
    QuizSessionDetailView,
    QuizSessionEndOrContinueView,
    QuizSessionRunView,
    QuizTakeView,
)

app_name = "mcq_bank"

urlpatterns = [
    path("history/", view=HistoryView.as_view(), name="history"),
    path("quiz/create/", view=QuizSessionCreateView.as_view(), name="quiz_session_create"),
    path(
        "quiz/check_create/",
        view=QuizSessionEndOrContinueView.as_view(),
        name="check_session",
    ),
    path(
        "quiz/session/<int:id>",
        view=QuizSessionRunView.as_view(),
        name="quiz_session_run",
    ),
    path("session/", view=QuizTakeView.as_view(), name="run_session"),
    path(
        "history/<int:id>",
        view=QuizSessionDetailView.as_view(),
        name="quiz_session_detail",
    ),
    path("question/<int:id>", view=QuestionUpdateView.as_view(), name="question_update"),
    path("question/create", view=QuestionCreateView.as_view(), name="question_create"),
    path("question/", view=QuestionListView.as_view(), name="question_list"),
    # redirect all others to index
    re_path("^$", view=QuizIndexView.as_view(), name="quiz_index"),
    re_path("^.*$", view=IndexRedirectView.as_view(), name="index_redirect"),  # redirect all others to index
]
