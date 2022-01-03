from datetime import datetime
from typing import List

from django.db import models
from martor.models import MartorField

from medusa_website.users.models import User
from medusa_website.utils.general import get_pretty_logger

logger = get_pretty_logger(__name__)


class ContributionType(models.Model):
    """
    A type of contribution, e.g MCQ Night
    """

    machine_name = models.CharField(
        max_length=64,
        help_text="Machine readable type of contribution, e.g. MCQ_NIGHT_ORGANISE. Must be unique",
        unique=True,
    )
    name = models.CharField(
        max_length=128,
        help_text="Human readable type of contribution, e.g. 'Organised MCQ Night'. Must be unique.",
        unique=True,
    )
    requires_signoff = models.BooleanField(
        default=True, help_text="True if this contribution requires signoff by a executive member"
    )
    signoff_requirements = models.TextField(
        help_text="Any sign off requirements for the contribution, e.g. uploading MCQ slides to MeDUSA drive",
        null=True,
        blank=True,
    )

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.machine_name}>"

    def __str__(self):
        return self.__repr__()


class Contribution(models.Model):
    """
    A contribution by a MeDUSA member to the society, e.g. a
    """

    user = models.ForeignKey(
        User,
        help_text="User the this contribution corresponds to",
        on_delete=models.PROTECT,
        related_name="contributions",
    )
    date = models.DateField(help_text="Date the contribution occurred")
    type = models.ForeignKey(ContributionType, on_delete=models.PROTECT, related_name="contributions")
    description = models.CharField(
        max_length=128,
        help_text="Description of the contribution. E.g. DSIG MCQ Night. \n"
        "For auto-generated like Question and OSCE Bank creation, "
        "this field will be filled the unique ID of the question or OSCE station",
        unique=True,
    )
    is_signed_off = models.BooleanField(
        default=False, help_text="This will change status after signing off, do not edit this field manually."
    )
    signed_off_by = models.ForeignKey(
        User,
        help_text="User who signed off contribution, if required",
        on_delete=models.PROTECT,
        related_name="signed_contributions",
        null=True,
        blank=True,
    )
    signed_off_date = models.DateField(
        help_text="Date the contribution was signed off. "
        "This will be auto filled upon signing, do not edit manually",
        null=True,
        blank=True,
    )
    requires_signing = models.BooleanField(
        default=True,
        help_text="If true, it needs signing off by a sign off approver. "
        "This will change status after signing off, do not edit this field manually.",
    )

    class Meta:
        unique_together = ["user", "date", "type", "description"]

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.user} - {self.type.machine_name}>"

    def __str__(self):
        return self.__repr__()

    def save(self, *args, **kwargs):
        # Set flags if sign off, or if its not required
        if self.signed_off_by:
            self.is_signed_off = True
            self.requires_signing = False
            self.signed_off_date = datetime.today()
        elif self.type.requires_signoff is False:
            self.requires_signing = False
        else:
            self.requires_signing = True
        super().save(*args, **kwargs)

    @classmethod
    def gen_mcq_bank_contributions_for_user(cls, user: User):
        from medusa_website.mcq_bank.models import Question

        logger.info(f"Generating mcq_bnk contributions for user {user}")
        # TODO implement rate limiter?

        authored_questions = Question.objects.filter(author=user)
        reviewed_questions = Question.objects.filter(reviewed_by=user)

        question_create_contrib_type = ContributionType.objects.get(machine_name="MCQ_BANK_QUESTION_CREATE")
        question_review_contrib_type = ContributionType.objects.get(machine_name="MCQ_BANK_QUESTION_REVIEW")

        for q in authored_questions:
            contrib, created = cls.objects.get_or_create(
                user=user,
                date=q.creation_date,
                type=question_create_contrib_type,
                description=f"Authored MCQ Bank Question id {q.id}",
            )
            if created:
                logger.info(f"Created contribution : {contrib}")

        for q in reviewed_questions:
            if not q.review_date:
                q.review_date = datetime.today().date()
                q.save()

            contrib, created = cls.objects.get_or_create(
                user=user,
                date=q.review_date,
                type=question_review_contrib_type,
                description=f"Reviewed MCQ Bank Question id {q.id}",
            )
            if created:
                logger.info(f"Created contribution : {contrib}")

    @classmethod
    def gen_osce_bank_contributions_for_user(cls, user: User):
        logger.info(f"Generating OSCE bank contributions for user {user}")
        # TODO implement rate limiter?

        from medusa_website.osce_bank.models import OSCEStation

        authored_stations = OSCEStation.objects.filter(author=user)
        reviewed_stations = OSCEStation.objects.filter(reviewed_by=user)

        station_create_contrib_type = ContributionType.objects.get(machine_name="OSCE_BANK_STATION_CREATE")
        station_review_contrib_type = ContributionType.objects.get(machine_name="OSCE_BANK_STATION_REVIEW")

        for s in authored_stations:
            contrib, created = cls.objects.get_or_create(
                user=user,
                date=s.creation_date,
                type=station_create_contrib_type,
                description=f"Authored OSCE Bank Station id {s.id}",
            )
            if created:
                logger.info(f"Created contribution : {contrib}")

        for s in reviewed_stations:
            if not s.review_date:
                s.review_date = datetime.today().date()
                s.save()

            contrib, created = cls.objects.get_or_create(
                user=user,
                date=s.review_date,
                type=station_review_contrib_type,
                description=f"Reviewed OSCE Bank Station id {s.id}",
            )
            if created:
                logger.info(f"Created contribution : {contrib}")

    def sign(self, signer: User):
        self.signed_off_by = signer
        self.save()


class ContributionCertificate(models.Model):
    """
    Represents a certificate of contributions for a particular user.
    """

    user = models.OneToOneField(
        User,
        help_text="User the this contribution certificate corresponds to. Note there will only be one certificate at any one time",
        on_delete=models.CASCADE,
        related_name="contribution_certificate",
        primary_key=True,
    )
    date_modified = models.DateField(help_text="Date the certificate was generated", auto_now=True)
    signed_off_by = models.ForeignKey(
        User,
        help_text="User who signed off contribution, if required",
        on_delete=models.PROTECT,
        related_name="signed_contribution_certificates",
        null=True,
        blank=True,
    )
    signed_off_date = models.DateField(help_text="Date the contribution was signed off", null=True, blank=True)
    details = MartorField(
        help_text="Markdown formatted details. This will be generated automatically by "
        "user.generate_contribution_certificate, but can be modified afterwards as well.",
        blank=True,
        null=True,
    )

    @property
    def contributions(self):
        return self.user.contributions.all()

    @classmethod
    def generate_for_user(cls, user: User):
        if hasattr(user, "contribution_certificate"):
            logger.info(f"Clearing existing contribution certificate for {user}")
            user.contribution_certificate = None
            user.save()

        logger.info(f"Generating contributions for user {user}")
        Contribution.gen_mcq_bank_contributions_for_user(user)
        Contribution.gen_osce_bank_contributions_for_user(user)

        cert = cls(user=user)
        cert.save()

        return Contribution.objects.filter(user=user)

    def to_pdf(self):
        if not self.signed_off_by or not self.signed_off_date:
            raise Exception(
                "Contribution Certificate is not yet signed off!\n" "Please get it signed before attempting export"
            )
        raise NotImplementedError()

    def email_to_user(self):
        raise NotImplementedError()

    @staticmethod
    def cert_signers() -> List[User]:
        from medusa_website.org_chart.models import CommitteeMemberRecord

        current_year = datetime.today().year
        committee_members = [
            CommitteeMemberRecord.objects.get(role__email="president@medusa.org.au", year=current_year),
            CommitteeMemberRecord.objects.get(role__email="vp@medusa.org.au", year=current_year),
        ]
        signers = [mem.user for mem in committee_members]
        return signers
