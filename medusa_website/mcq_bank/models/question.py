from typing import Optional

from django.db import models

from medusa_website.users.models import User

# TODO single source of truth for this, see frontend/src/MedusaMCQ.tsx

QUESTION_CATEGORIES = ["UNCATEGORISED", "CARDIOLOGY", "NEUROLOGY", "PAEDIATRICS"]
QuestionCategory = models.TextChoices("QuestionCategory", QUESTION_CATEGORIES)


class Question(models.Model):

    question_text = models.TextField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    image = models.ImageField(null=True, blank=True)
    category = models.CharField(
        max_length=128,
        choices=QuestionCategory.choices,
        default=QuestionCategory.UNCATEGORISED,
        blank=None,
        null=True,
    )

    def add_new_answer(self, answer_text: str, is_correct=False):
        from medusa_website.mcq_bank.models import Answer

        Answer.objects.create(
            question=self, answer_text=answer_text, is_correct=is_correct
        )

    def add_existing_answer(self, answer_id, is_correct=None):
        from medusa_website.mcq_bank.models import Answer

        a: Answer = Answer.objects.get(id=answer_id)
        assert a.question is None
        if is_correct is not None:
            a.is_correct = is_correct
        self.save()

    def set_correct_answer(self, answer_id):
        from medusa_website.mcq_bank.models import Answer

        a = Answer.objects.get(id=answer_id)
        a.is_correct = True

        self.save()

    @property
    def num_correct_ans(self):
        return len([a for a in self.answers.all() if a.is_correct])

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
