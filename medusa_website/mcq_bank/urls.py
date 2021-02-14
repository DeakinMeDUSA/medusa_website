from django.urls import path, re_path

from . import views

app_name = "mcq_bank"

urlpatterns = [
    path(r"", views.IndexView.as_view(), name="index"),
    path("<int:question_id>/", views.detail, name="detail"),
    path("api/questions", views.QuestionListCreate.as_view()),
    path("api/question/<int:id>", views.QuestionRetrieveUpdateDestroy.as_view()),
    path("api/answers", views.AnswersList.as_view()),
    path("api/answer/<int:id>", views.AnswerRetrieveUpdateDestroy.as_view()),
    path("api/answer/create", views.AnswerCreate.as_view()),
]
