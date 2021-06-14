from .answer import AnswerCreateView, AnswersListView, AnswerUpdateView
from .categories import CategoriesTableView, ViewQuestionsByCategoryView
from .history import HistoryView
from .question import QuestionCreateView, QuestionUpdateView
from .quiz_base import IndexRedirectView, QuizIndexView
from .quiz_take import QuizTakeView
from .record import RecordCreateView, RecordHistoryView
from .session import (
    QuizSessionCreateView,
    QuizSessionDetailView,
    QuizSessionEndOrContinueView,
    QuizSessionListView,
    QuizSessionRunView,
)
