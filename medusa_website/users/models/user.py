import datetime

from allauth.account.models import EmailAddress
from cuser.models import CUserManager
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import Group, PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.db.models import CharField
from django.urls import reverse
from django.utils import timezone

from medusa_website.utils.general import get_pretty_logger

logger = get_pretty_logger(__name__)


class User(AbstractBaseUser, PermissionsMixin):
    """Default user for MeDUSA Website."""

    email = models.EmailField(
        "Email address",
        unique=True,
        error_messages={
            "unique": "A user with that email address already exists.",
        },
    )

    member_id = models.CharField(
        "Member iD",
        unique=True,
        max_length=12,
        null=True,
        blank=True,
        error_messages={
            "unique": "The Member ID of a user must be unique!",
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
        help_text="Designates whether this user has medusa.org.au email address.",
    )

    is_member = models.BooleanField(
        "Is a MeDUSA member",
        default=True,
        help_text="Designates whether the user is a member of MeDUSA. "
        "Non-members include @medusa.org.au addresses, external clubs with accounts",
    )

    date_joined = models.DateTimeField("Date joined", default=timezone.now)
    membership_expiry = models.DateField(help_text="Date their membership expires", null=True, blank=True)
    signature_image = models.ImageField(
        help_text="Image of the users signature, only used for signing certificates",
        upload_to="signatures",
        null=True,
        blank=True,
    )
    phone_number = models.CharField(max_length=24, null=True, blank=True)

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

    def has_contrib_sign_off_permission(self) -> bool:
        contrib_sign_off_group = Group.objects.get(name="Contributions Sign Off")
        return self in contrib_sign_off_group.user_set.all()

    def gen_contribution_certificate(self):
        from medusa_website.users.models import ContributionCertificate

        return ContributionCertificate.generate_for_user(self)

    def create_member_id(self):
        """Create member_id of the format 2021-0088-48"""
        assert self.is_member
        assert self.member_id is None  # don't want to change these after they are created once!
        # Pad database id with 0s to 4 digits, e.g. 12 -> 0012,
        # then add numbers - the last two digits of the result of the year and the id
        check_num = str(int(self.date_joined.year) * int(self.id))[-2:]
        member_id = f"{self.date_joined.year:04}-{self.id:04}-{check_num}"
        self.member_id = member_id
        self.save()
        return member_id

    @staticmethod
    def validate_member_id(member_id: str) -> bool:
        member_id = member_id.strip()
        if "-" not in member_id and len(member_id) == 10:  # forgot to add dashes?
            member_id = f"{member_id[0:4]}-{member_id[4:8]}-{member_id[8:10]}"
        try:
            assert len(member_id) == 12
            year, user_id, check_no = member_id.split("-")
            year = int(year)
            user_id = int(user_id)
            assert year > 2000 and user_id > 0
            assert str(year * user_id)[-2:] == str(check_no)
            return True
        except Exception as errmsg:
            return False

    def current_role(self):
        current_roles = self.committee_member_records.all().filter(year=datetime.datetime.today().year)
        if len(current_roles) > 0:
            return current_roles[0].role
        else:
            return None
