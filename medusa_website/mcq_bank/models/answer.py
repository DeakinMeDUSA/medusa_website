from django.db import models

from medusa_website.mcq_bank.models.question import Question


class Answer(models.Model):
    class Meta:
        verbose_name = "Answer"
        verbose_name_plural = "Answers"

    question = models.ForeignKey(
        Question,
        verbose_name="Question",
        on_delete=models.PROTECT,
        related_name="answers",
    )

    text = models.CharField(
        max_length=1000,
        help_text="Enter the answer text that you want displayed",
        verbose_name="Text",
    )

    correct = models.BooleanField(
        default=False,
        help_text="Is this a correct answer?",
        verbose_name="Correct",
    )
    explanation = models.CharField(
        max_length=1000,
        null=True,
        blank=True,
        help_text="Extra explanation for this answer",
    )

    def __str__(self):
        return self.text
