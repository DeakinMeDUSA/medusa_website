from django.db import models

from medusa_website.osce_bank.models.osce_station import OSCEStation
from medusa_website.users.models import User


class OSCEHistory(models.Model):
    """
    History of completed OSCE station

    """

    user = models.OneToOneField(User, verbose_name="User", on_delete=models.PROTECT, related_name="osce_history")

    completed_stations = models.ManyToManyField(OSCEStation, related_name="osce_user_histories")

    class Meta:
        verbose_name = "OSCE User History"
        verbose_name_plural = "OSCE User Histories"
