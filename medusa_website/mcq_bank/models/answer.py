from django.db import models


# Create your models here.


class Answer(models.Model):
    from medusa_website.mcq_bank.models.question import Question

    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="answers"
    )
    answer_text = models.CharField(max_length=200)
    explanation_text = models.CharField(max_length=500, null=True, blank=True)
    is_correct = models.BooleanField(default=False)

    # @property
    # def question_id(self):
    #     return self.question.id
