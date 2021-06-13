import re

from django.core.validators import validate_comma_separated_integer_list
from django.db import models
from django.db.models import QuerySet

from medusa_website.mcq_bank.models.category import Category
from medusa_website.users.models import User


class History(models.Model):
    """
    History is used to track an individual signed in users score on different
    quiz's and categories

    Data stored in csv using the format:
        category, score, possible, category, score, possible, ...
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
    def list_all_cat_scores(self):
        """
        Returns a dict in which the key is the category name and the item is
        a list of three integers.

        The first is the number of questions correct,
        the second is the possible best score,
        the third is the percentage correct.

        The dict will have one key for every category that you have defined
        """
        score_before = self.score
        output = {}

        for cat in Category.objects.all():
            to_find = re.escape(cat.category) + r",(\d+),(\d+),"
            #  group 1 is score, group 2 is highest possible

            match = re.search(to_find, self.score, re.IGNORECASE)

            if match:
                score = int(match.group(1))
                possible = int(match.group(2))

                try:
                    percent = int(round((float(score) / float(possible)) * 100))
                except:
                    percent = 0

                output[cat.category] = [score, possible, percent]

            else:  # if category has not been added yet, add it.
                self.score += cat.category + ",0,0,"
                output[cat.category] = [0, 0]

        if len(self.score) > len(score_before):
            # If a new category has been added, save changes.
            self.save()

        return output

    def update_score(self, question, score_to_add=0, possible_to_add=0):
        """
        Pass in question object, amount to increase score
        and max possible.

        Does not return anything.
        """
        category_test = Category.objects.filter(category=question.category).exists()

        if any(
            [
                item is False
                for item in [
                    category_test,
                    score_to_add,
                    possible_to_add,
                    isinstance(score_to_add, int),
                    isinstance(possible_to_add, int),
                ]
            ]
        ):
            return "error", "category does not exist or invalid score"

        to_find = (
            re.escape(str(question.category)) + r",(?P<score>\d+),(?P<possible>\d+),"
        )

        match = re.search(to_find, self.score, re.IGNORECASE)

        if match:
            updated_score = int(match.group("score")) + abs(score_to_add)
            updated_possible = int(match.group("possible")) + abs(possible_to_add)

            new_score = ",".join(
                [str(question.category), str(updated_score), str(updated_possible), ""]
            )

            # swap old score for the new one
            self.score = self.score.replace(match.group(), new_score)
            self.save()

        else:
            #  if not present but existing, add with the points passed in
            self.score += ",".join(
                [str(question.category), str(score_to_add), str(possible_to_add), ""]
            )
            self.save()

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
