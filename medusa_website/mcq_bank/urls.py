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
    QuizTakeView,
)
from .views.question import QuestionDetailView
from .views.session import QuizSessionCreateFromQuestionsView, complete_session

app_name = "mcq_bank"

urlpatterns = [
    path("history/", view=HistoryView.as_view(), name="history"),
    path(
        "quiz/create_from_questions/",
        view=QuizSessionCreateFromQuestionsView.as_view(),
        name="quiz_session_create_from_questions",
    ),
    path("quiz/create/", view=QuizSessionCreateView.as_view(), name="quiz_session_create"),
    path(
        "quiz/check_create/",
        view=QuizSessionEndOrContinueView.as_view(),
        name="check_session",
    ),
    path(
        "quiz/session/complete/<int:id>",
        view=complete_session,
        name="quiz_session_complete",
    ),
    path("session/", view=QuizTakeView.as_view(), name="run_session"),
    path(
        "history/<int:id>",
        view=QuizSessionDetailView.as_view(),
        name="quiz_session_detail",
    ),
    path("question/detail/<int:id>", view=QuestionDetailView.as_view(), name="question_detail"),
    path("question/update/<int:id>", view=QuestionUpdateView.as_view(), name="question_update"),
    path("question/create", view=QuestionCreateView.as_view(), name="question_create"),
    path("question/list", view=QuestionListView.as_view(), name="question_list"),
    # redirect all others to index
    re_path("^$", view=QuizIndexView.as_view(), name="quiz_index"),
    re_path("^.*$", view=IndexRedirectView.as_view(), name="index_redirect"),  # redirect all others to index
]

# TODO link detail view to use a modified UPdateView to keep things DRY
