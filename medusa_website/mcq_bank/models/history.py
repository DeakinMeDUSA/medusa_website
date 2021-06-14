import datetime
from typing import Dict, List, Optional, Union

from django.core.validators import validate_comma_separated_integer_list
from django.db import models
from django.db.models import QuerySet

from medusa_website.mcq_bank.models.category import Category
from medusa_website.mcq_bank.utils import percent
from medusa_website.users.models import User


class History(models.Model):
    """
    History is used to track an individual signed in users score on different
    quiz's and categories

    """

    user = models.OneToOneField(User, verbose_name="User", on_delete=models.CASCADE)

    score = models.CharField(
        max_length=1024,
        verbose_name="Score",
        validators=[validate_comma_separated_integer_list],
    )

    class Meta:
        verbose_name = "User History"
        verbose_name_plural = "User progress records"

    @property
    def category_progress(self) -> List[Dict[str, Optional[float]]]:
        """
        Returns a dict in which the key is the category name and the item is a dict of results

        """
        from medusa_website.mcq_bank.models import Record

        cat_progress = []

        for cat in Category.objects.all():
            all_cat_qs = cat.questions.all()
            answered = Record.objects.filter(question__category=cat, user=self.user)
            distinct_answers = answered.distinct("question")
            cat_attempted_percent = percent(distinct_answers.count(), all_cat_qs.count())
            correct_q = [r for r in answered if r.is_correct]
            cat_average_score = percent(len(correct_q), answered.count())
            cat_progress.append(
                {
                    "category_name": cat.name,
                    "cat_qs_num": all_cat_qs.count(),
                    "attempted_num": distinct_answers.count(),
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

    @classmethod
    def get_create_for_user(cls, user: User) -> "History":
        new_progress = cls(user=user)
        new_progress.save()
        return new_progress
