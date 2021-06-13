from django.urls import path

from .views import (
    AnswerCreateView,
    AnswerRetrieveUpdateDestroyView,
    AnswersListView,
    CategoriesTableView,
    HistoryView,
    QuestionDetailView,
    QuestionListCreateView,
    QuestionRetrieveUpdateDestroyView,
    QuizDetailView,
    QuizIndexView,
    QuizListView,
    QuizSessionCreateView,
    QuizSessionDetailView,
    QuizSessionEndOrContinueView,
    QuizSessionRunView,
    QuizTakeView,
    RecordCreateView,
    RecordHistoryView,
    ViewQuestionsByCategoryView,
)

app_name = "mcq_bank"

urlpatterns = [
    # API Endpoints, to be depreciated
    path("api/questions/", QuestionListCreateView.as_view()),
    path("api/question/<int:id>", QuestionRetrieveUpdateDestroyView.as_view()),
    path("api/answers", AnswersListView.as_view()),
    path("api/answer/<int:id>", AnswerRetrieveUpdateDestroyView.as_view()),
    path("api/answer/create", AnswerCreateView.as_view()),
    path("api/record/list", RecordHistoryView.as_view()),
    path("api/record/create", RecordCreateView.as_view()),
    # Others
    path("index/", view=QuizIndexView.as_view(), name="quiz_index"),
    path("quiz_list/", view=QuizListView.as_view(), name="quiz_list"),
    path(
        "category/", view=CategoriesTableView.as_view(), name="quiz_category_list_all"
    ),
    path(
        "category/<str:category_name>",
        view=ViewQuestionsByCategoryView.as_view(),
        name="category_detail",
    ),
    path("question/<int:id>", view=QuestionDetailView.as_view(), name="question"),
    path("history/", view=HistoryView.as_view(), name="history"),
    path(
        "quiz/create/", view=QuizSessionCreateView.as_view(), name="quiz_session_create"
    ),
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
    #  passes variable 'quiz_name' to quiz_take view
    path(
        "quiz/<slug:quiz_name>/", view=QuizDetailView.as_view(), name="quiz_start_page"
    ),
    path("session/", view=QuizTakeView.as_view(), name="run_session"),
    path(
        "history/<int:id>",
        view=QuizSessionDetailView.as_view(),
        name="quiz_session_detail",
    ),
    path(
        "question/<int:id>", view=QuestionDetailView.as_view(), name="question_detail"
    ),
]
