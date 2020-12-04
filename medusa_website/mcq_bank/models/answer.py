from django.db import models

from medusa_website.mcq_bank.models.question import Question

# Create your models here.


class Answer(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="answers"
    )
    answer_text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)
