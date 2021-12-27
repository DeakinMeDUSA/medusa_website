from allauth.account.models import EmailAddress
from cuser.models import CUserManager
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import Group, PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.db.models import CharField
from django.urls import reverse
from django.utils import timezone


class User(AbstractBaseUser, PermissionsMixin):
    """Default user for MeDUSA Website."""

    email = models.EmailField(
        "Email address",
        unique=True,
        error_messages={
            "unique": "A user with that email address already exists.",
        },
    )
    # First and last name do not cover name patterns around the globe
    name = CharField("Name of User", blank=True, max_length=255)

    is_staff = models.BooleanField(
        "Staff status",
        default=False,
        help_text="Designates whether the user can log into this admin site.",
    )
    is_active = models.BooleanField(
        "Active",
        default=True,
        help_text="Designates whether this user should be treated as active. "
        "Unselect this instead of deleting accounts.",
    )
    is_medusa = models.BooleanField(
        "Is a medusa.org.au user",
        default=False,
        help_text="Designates whether this user is associated with a medusa.org.au email address.",
    )

    date_joined = models.DateTimeField("Date joined", default=timezone.now)

    objects = CUserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def get_absolute_url(self):
        """Get url for user's detail view.
        Returns:
            str: URL for user detail.
        """
        return reverse("users:detail", kwargs={"email": self.email})

    @property
    def answered_questions(self):
        from medusa_website.mcq_bank.models import Record

        return Record.objects.filter(user=self)

    @property
    def correct_questions(self):
        return self.answered_questions.filter(answer__is_correct=True)

    @property
    def incorrect_questions(self):
        return self.answered_questions.filter(answer__is_correct=False)

    @property
    def all_emails(self):
        return EmailAddress.objects.filter(user=self).all()

    def is_reviewer(self) -> bool:
        reviewer_group = Group.objects.get(name="ContentReviewers")
        return self in reviewer_group.user_set.all()
