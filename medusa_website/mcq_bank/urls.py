from django.urls import path

from . import views
from .views import (
    CategoriesListView,
    QuizDetailView,
    QuizListView,
    QuizMarkingDetail,
    QuizMarkingList,
    QuizTake,
    QuizUserProgressView,
    ViewQuizListByCategory,
)

app_name = "mcq_bank"

urlpatterns = [
    path("api/questions", views.QuestionListCreate.as_view()),
    path("api/question/<int:id>", views.QuestionRetrieveUpdateDestroy.as_view()),
    path("api/answers", views.AnswersList.as_view()),
    path("api/answer/<int:id>", views.AnswerRetrieveUpdateDestroy.as_view()),
    path("api/answer/create", views.AnswerCreate.as_view()),
    path("api/record/list", views.RecordHistory.as_view()),
    path("api/record/create", views.RecordCreate.as_view()),
    path("index/", view=QuizListView.as_view(), name="quiz_list"),
    path("category/", view=CategoriesListView.as_view(), name="quiz_category_list_all"),
    path(
        "category/<str:category_name>",
        view=ViewQuizListByCategory.as_view(),
        name="quiz_category_list_matching",
    ),
    path("progress/", view=QuizUserProgressView.as_view(), name="quiz_progress"),
    path("marking/", view=QuizMarkingList.as_view(), name="quiz_marking"),
    path(
        "marking/<int:id>", view=QuizMarkingDetail.as_view(), name="quiz_marking_detail"
    ),
    #  passes variable 'quiz_name' to quiz_take view
    path(
        "quiz/<slug:quiz_name>/", view=QuizDetailView.as_view(), name="quiz_start_page"
    ),
    path("quiz/<slug:quiz_name>/take/", view=QuizTake.as_view(), name="quiz_question"),
]
