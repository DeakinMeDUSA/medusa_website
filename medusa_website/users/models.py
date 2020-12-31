from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, EmailField, IntegerField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Default user for MeDUSA Website."""

    #: First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    email = EmailField(unique=True)
    graduation_year = IntegerField(
        verbose_name="Year of Graduation", null=True, blank=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})

    @property
    def answered_questions(self):
        from medusa_website.mcq_bank.models import Record
        return Record.objects.filter(user=self)

    @property
    def correct_questions(self):
        return self.answered_questions.filter(answer__is_correct=True)

    @property
    def incorrect_qustions(self):
        return self.answered_questions.filter(answer__is_correct=False)
