from typing import Optional, Union

from django.db import models

from medusa_website.mcq_bank.models.category import Category, SubCategory
from medusa_website.mcq_bank.models.quiz import Quiz
from medusa_website.users.models import User

ANSWER_ORDER_OPTIONS = (("text", "Text"), ("random", "Random"), ("none", "None"))


class Question(models.Model):
    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"
        ordering = ["category"]

    text = models.CharField(
        max_length=1000,
        blank=False,
        help_text="Enter the question text that you want displayed",
    )
    author = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    image = models.ImageField(null=True, blank=True, verbose_name="Image")

    category = models.ForeignKey(
        Category,
        verbose_name="Category",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="questions",
    )

    sub_category = models.ForeignKey(
        SubCategory,
        verbose_name="Sub-Category",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    explanation = models.TextField(
        max_length=2000,
        blank=True,
        help_text="Explanation to be shown after the question has been answered",
        verbose_name="Explanation",
    )

    answer_order = models.CharField(
        max_length=30,
        null=True,
        blank=True,
        choices=ANSWER_ORDER_OPTIONS,
        help_text="The order in which multichoice answer options are displayed to the user",
        verbose_name="Answer Order",
    )
    quiz = models.ManyToManyField(
        Quiz, verbose_name="Quiz", blank=True, related_name="questions"
    )

    def __str__(self):
        return self.text

    @classmethod
    def create_with_auth(
        cls, question_text: str, author: User, image: Union[bytes, str], category: str
    ):
        """ Used when user is creating questions from  the front end"""
        if len(question_text) == 0:
            raise ValueError("Cannot create Question with no question text")

        new_q = cls.objects.create(
            question_text=question_text, author=author, image=image, category=category
        )
        return new_q

    @property
    def num_correct_ans(self):
        return len([a for a in self.answers.all() if a.correct])

    @property
    def has_image(self) -> bool:
        if self.image:
            return True
        else:
            return False

    @property
    def image_url(self) -> Optional[str]:
        if self.image:
            return self.image.url
        else:
            return None

    @staticmethod
    def check_if_correct(guess: str):
        from medusa_website.mcq_bank.models.answer import Answer

        answer = Answer.objects.get(id=guess)
        return answer.correct

    def order_answers(self, queryset):
        if self.answer_order == "content":
            return queryset.order_by("content")
        if self.answer_order == "random":
            return queryset.order_by("?")
        if self.answer_order == "none":
            return queryset.order_by()
        return queryset

    def get_answers(self):
        return self.order_answers(self.answers.all())

    def get_answers_list(self):
        return [
            (answer.id, answer.text)
            for answer in self.order_answers(self.answers.all())
        ]

    @staticmethod
    def answer_choice_to_string(guess):
        from medusa_website.mcq_bank.models.answer import Answer

        return Answer.objects.get(id=guess).text

    def add_new_answer(self, answer_text: str, explanation: str = "", correct=False):
        from medusa_website.mcq_bank.models.answer import Answer

        Answer.objects.create(
            question=self,
            text=answer_text,
            correct=correct,
            explanation=explanation,
        )

    def add_existing_answer(self, answer_id, correct=None):
        from medusa_website.mcq_bank.models.answer import Answer

        a: Answer = Answer.objects.get(id=answer_id)
        assert a.question is None
        if correct is not None:
            a.correct = correct
        self.save()

    def set_correct_answer(self, answer_id):
        from medusa_website.mcq_bank.models.answer import Answer

        a = Answer.objects.get(id=answer_id)
        a.correct = True

        self.save()
