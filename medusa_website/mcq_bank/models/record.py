from django.db import models


class Record(models.Model):
    from medusa_website.mcq_bank.models import Answer, Question
    from medusa_website.users.models import User

    """ Model to record the events of Question/Answers"""

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="records",
    )
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, blank=True, null=True, related_name="records")
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="records")
    timestamp = models.DateTimeField(auto_now_add=True)

    @property
    def is_correct(self):
        return self.answer.correct
