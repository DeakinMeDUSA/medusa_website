import datetime
from typing import Dict, List, Optional, Union

from django.core.validators import validate_comma_separated_integer_list
from django.db import models
from django.db.models import QuerySet
from memoize import memoize

from medusa_website.mcq_bank.models.category import Category
from medusa_website.mcq_bank.utils import percent
from medusa_website.users.models import User


class History(models.Model):
    """
    History is used to track an individual signed in users score on different
    quiz's and categories

    """

    user = models.OneToOneField(User, verbose_name="User", on_delete=models.PROTECT)

    score = models.CharField(
        max_length=1024,
        verbose_name="Score",
        validators=[validate_comma_separated_integer_list],
    )

    class Meta:
        verbose_name = "User History"
        verbose_name_plural = "User progress records"

    @property
    @memoize(timeout=120)  # cache result for 120 seconds
    def category_progress(self) -> List[Dict[str, Optional[float]]]:
        """
        Returns a dict in which the key is the category name and the item is a dict of results, along with an aggregated "all"

        """
        from medusa_website.mcq_bank.models import Question, Record

        cat_progress = []

        all_qs = Question.objects.all()
        all_qs_count = all_qs.count()
        answered_qs = Record.objects.filter(user=self.user).prefetch_related("answer", "question__category")
        distinct_answers = answered_qs.distinct("question")
        distinct_answers_count = distinct_answers.count()
        all_attempted_percent = percent(distinct_answers_count, all_qs_count)
        all_correct_q = [r for r in answered_qs if r.is_correct]
        all_average_score = percent(len(all_correct_q), answered_qs.count())
        cat_progress.append(
            {
                "id": 0,
                "name": "OVERALL",
                "cat_qs_num": all_qs_count,
                "attempted_num": distinct_answers_count,
                "attempted_percent": all_attempted_percent,
                "cat_average_score": all_average_score,
            }
        )

        for cat in Category.objects.all().prefetch_related("questions"):
            all_cat_qs = cat.questions.all()
            all_cat_qs_count = all_cat_qs.count()
            answered = answered_qs.filter(question__category=cat)
            distinct_answers = answered.distinct("question")
            distinct_answers_count = distinct_answers.count()
            cat_attempted_percent = percent(distinct_answers_count, all_cat_qs_count)
            correct_q = [r for r in answered if r.is_correct]
            cat_average_score = percent(len(correct_q), answered.count())
            cat_progress.append(
                {
                    "id": cat.id,
                    "name": cat.name,
                    "cat_qs_num": all_cat_qs_count,
                    "attempted_num": distinct_answers_count,
                    "attempted_percent": cat_attempted_percent,
                    "cat_average_score": cat_average_score,
                }
            )

        return cat_progress


    @property
    def session_history(
        self,
    ) -> List[Dict[str, Union[None, float, bool, datetime.datetime]]]:
        """
        Returns a dict in which the key is the category name and the item is a dict of results

        """
        session_history = []

        for session in self.quiz_sessions:
            attempted = session.answers.count()

            session_history.append(
                {
                    "id": session.id,
                    "is_complete": session.complete,
                    "started": session.started,
                    "finished": session.finished,
                    "total_session_qs": session.questions.count(),
                    "attempted": session.answers.count(),
                    "correct_answers": session.correct_answers.count(),
                    "correct_answers_percent": session.percent_correct,
                }
            )
        return list(reversed(session_history))

    @property
    def current_session(self):
        from medusa_website.mcq_bank.models import QuizSession

        return QuizSession.get_current(user=self.user)

    @property
    def quiz_sessions(self) -> QuerySet["QuizSession"]:
        return self.user.quiz_sessions.all()

    def answered_questions(self, questions: Optional[QuerySet] = None):
        from medusa_website.mcq_bank.models import Question, Record

        questions = questions or Question.objects
        records = Record.objects.filter(user=self.user).distinct("question")
        return questions.filter(records__in=records)
