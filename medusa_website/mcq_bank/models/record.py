from typing import Optional

from django.db import models

from medusa_website.mcq_bank.models import Answer, Question
from medusa_website.users.models import User


class Record(models.Model):
    """ Model to record the events of Question/Answers"""

    question = models.ForeignKey(
        Question, on_delete=models.SET_NULL, blank=True, null=True
    )
    answer = models.ForeignKey(Answer, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    timestamp = models.DateTimeField()

    @property
    def is_correct(self):
        return self.answer.is_correct
