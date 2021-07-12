from typing import Optional, Union

import markdown
from django.db import models
from django.db.models import QuerySet
from django.urls import reverse
from django.utils.safestring import mark_safe
from martor.models import MartorField

from medusa_website.mcq_bank.models.category import Category
from medusa_website.users.models import User


class Question(models.Model):
    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"
        ordering = ["category"]

    text = models.CharField(
        max_length=1000,
        blank=False,
        help_text="Enter the question text that you want displayed",
        verbose_name="Question text",
        unique=True,
    )
    author = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    image = models.ImageField(
        null=True, blank=True, verbose_name="Image", help_text="Upload an image supporting the question"
    )

    category = models.ForeignKey(
        Category,
        verbose_name="Category",
        on_delete=models.CASCADE,
        related_name="questions",
    )

    explanation = MartorField(
        max_length=2000,
        help_text="Explanation to be shown after the question has been answered",
        verbose_name="Explanation",
    )

    randomise_answer_order = models.BooleanField(
        default=True,
        help_text="If True (default), answers will be displayed in a random order each time",
        verbose_name="Randomise answer order?",
    )

    def __str__(self):
        return self.text

    @classmethod
    def create_with_auth(cls, question_text: str, author: User, image: Union[bytes, str], category: str):
        """Used when user is creating questions from  the front end"""
        if len(question_text) == 0:
            raise ValueError("Cannot create Question with no question text")

        new_q = cls.objects.create(question_text=question_text, author=author, image=image, category=category)
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

    def order_answers(self, queryset) -> QuerySet:
        if self.randomise_answer_order:
            return queryset.order_by("?")
        else:
            return queryset

    def get_answers(self):
        return self.order_answers(self.answers.all())

    def get_answers_list(self):
        return [(answer.id, answer.text) for answer in self.order_answers(self.answers.all())]

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

    @property
    def correct_answers(self):
        return self.answers.filter(correct=True)

    def get_absolute_url(self):
        return reverse("mcq_bank:question_detail", kwargs={"id": self.id})

    def is_answered(self, user: User) -> bool:
        return self in user.history.answered_questions()

    @classmethod
    def question_list_for_user(cls, user=User, questions: Optional[QuerySet] = None):
        """For use in the question_list view"""
        question_list = []
        from medusa_website.mcq_bank.models import History

        history, created = History.objects.get_or_create(user=user)  # force init of history

        all_questions = questions or Question.objects.all()
        for q in all_questions:
            q.answered = q.is_answered(user=user)
        return all_questions

    @property
    def explanation_as_html(self):
        if self.explanation:
            html = markdown.markdown(self.explanation)
            return mark_safe(html)
        else:
            return mark_safe("None")

    def editable(self, user: User):
        return user.is_staff or user.is_superuser or (user == self.author)
