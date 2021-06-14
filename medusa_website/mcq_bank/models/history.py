import re
from typing import Dict

from django.core.validators import validate_comma_separated_integer_list
from django.db import models
from django.db.models import QuerySet

from medusa_website.mcq_bank.models.category import Category
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
    def category_progress(self) -> Dict:
        """
        Returns a dict in which the key is the category name and the item is
        a list of three integers.

        The first is the number of questions attempted in that category
        the second is number of questions remaining,
        the third is the percentage of questions attempted.
        """
        from medusa_website.mcq_bank.models import Record

        cat_progress = {}

        for cat in Category.objects.all():
            all_cat_qs = Category.objects.all()
            user_answers = Record.objects.filter(question__category=cat, user=self.user)
            distinct_answers = user_answers.distinct("question")
            cat_complete_percent = round(
                100 * distinct_answers.count() / all_cat_qs.count()
            )
            cat_progress[cat.name]

        return cat_progress

    @property
    def current_session(self):
        from medusa_website.mcq_bank.models import QuizSession

        return QuizSession.get_current(user=self.user)

    @property
    def sessions(self) -> QuerySet["QuizSession"]:
        return self.user.quiz_sessions.all()

    @classmethod
    def get_create_for_user(cls, user: User) -> "History":
        new_progress = cls(user=user)
        new_progress.save()
        return new_progress
