import re

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
from django.db import models

from medusa_website.mcq_bank.models.category import Category


class Quiz(models.Model):
    title = models.CharField(verbose_name="Title", max_length=60, blank=False)

    description = models.TextField(
        verbose_name="Description", blank=True, help_text="a description of the quiz"
    )

    url = models.CharField(
        max_length=60,
        blank=False,
        help_text="a user friendly url",
        verbose_name="user friendly url",
    )

    category = models.ForeignKey(
        Category,
        null=True,
        blank=True,
        verbose_name="Category",
        on_delete=models.CASCADE,
    )

    random_order = models.BooleanField(
        blank=False,
        default=False,
        verbose_name="Random Order",
        help_text="Display the questions in a random order or as they are set?",
    )

    max_questions = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name="Max Questions",
        help_text="Number of questions to be answered on each attempt.",
    )

    answers_at_end = models.BooleanField(
        blank=False,
        default=False,
        help_text="Correct answer is NOT shown after question. Answers displayed at the end.",
        verbose_name="Answers at end",
    )

    exam_paper = models.BooleanField(
        blank=False,
        default=False,
        help_text="If yes, the result of each attempt by a user will be stored. Necessary for marking.",
        verbose_name="Exam Paper",
    )

    single_attempt = models.BooleanField(
        blank=False,
        default=False,
        help_text="If yes, only one attempt by a user will be permitted. Non users cannot sit this exam.",
        verbose_name="Single Attempt",
    )

    pass_mark = models.SmallIntegerField(
        blank=True,
        default=0,
        verbose_name="Pass Mark",
        help_text="Percentage required to pass exam.",
        validators=[MaxValueValidator(100)],
    )

    success_text = models.TextField(
        blank=True, help_text="Displayed if user passes.", verbose_name="Success Text"
    )

    fail_text = models.TextField(
        verbose_name="Fail Text", blank=True, help_text="Displayed if user fails."
    )

    draft = models.BooleanField(
        blank=True,
        default=False,
        verbose_name="Draft",
        help_text="If yes, the quiz is not displayed in the quiz list and can only be taken by users who can edit quizzes.",
    )

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        self.url = re.sub("\s+", "-", self.url).lower()

        self.url = "".join(
            letter for letter in self.url if letter.isalnum() or letter == "-"
        )

        if self.single_attempt is True:
            self.exam_paper = True

        if self.pass_mark > 100:
            raise ValidationError("%s is above 100" % self.pass_mark)

        super(Quiz, self).save(force_insert, force_update, *args, **kwargs)

    class Meta:
        verbose_name = "Quiz"
        verbose_name_plural = "Quizzes"

    def __str__(self):
        return self.title

    @property
    def get_max_score(self):
        return self.questions.all().count()

    def anon_score_id(self):
        return str(self.id) + "_score"

    def anon_q_list(self):
        return str(self.id) + "_q_list"

    def anon_q_data(self):
        return str(self.id) + "_data"
