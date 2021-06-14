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
        cat_progress = {}

        for cat in Category.objects.all():
            total_qs = cat.questions.count()
            user_answers = cat.questions.filter(user=self.user)

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
