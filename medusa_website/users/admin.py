from cuser.admin import UserAdmin as cuUserAdmin
from django.contrib import admin
from django.contrib.auth.models import Group
from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _
from nameparser import HumanName

from medusa_website.users.forms import UserChangeForm, UserCreationForm

from .models import (
    Contribution,
    ContributionType,
    MemberRecord,
    MemberRecordsImport,
    User,
)


@admin.action(description="Set selected users to staff (is_staff = True)")
def set_staff_status(modeladmin, request, queryset: QuerySet[User]):
    for user in queryset:
        user.is_staff = True
        user.save()


@admin.action(description="Set selected users to is_medusa = True")
def set_medusa_status(modeladmin, request, queryset: QuerySet[User]):
    for user in queryset:
        user.is_medusa = True
        user.save()


@admin.action(description="Set selected users to be in the Reviewers group")
def set_reviewer_status(modeladmin, request, queryset: QuerySet[User]):
    reviewers_group = Group.objects.get(name="ContentReviewers")
    for user in queryset:
        reviewers_group.user_set.add(user)
    reviewers_group.save()


@admin.action(description="Set user's name from memberlist if member record exists")
def set_name_from_memberlist(modeladmin, request, queryset: QuerySet[User]):
    for user in queryset:
        try:
            member_record = MemberRecord.objects.get(email=user.email)
            member_name = HumanName(member_record.name)
            member_name.capitalize(force=True)
            user.name = member_name
            user.save()
        except MemberRecord.DoesNotExist:
            pass


@admin.action(description="Import users from memberlist")
def import_users(modeladmin, request, queryset: QuerySet[MemberRecordsImport]):
    for obj in queryset:
        if obj.file:
            obj.import_memberlist()
        else:
            print(f"No file for memberlist record {obj}")


@admin.action(description="Generate contribution certificate for user(s)")
def gen_contribution_certificates(modeladmin, request, queryset: QuerySet[User]):
    for user in queryset:
        user.gen_contribution_certificate()


@admin.action(description="Create missing member IDs")
def create_member_ids(modeladmin, request, queryset: QuerySet[User]):
    for user in queryset:
        try:
            user.create_member_id()
        except AssertionError:  # Already exists or not a member
            pass


@admin.action(description="Assign selected users to be a MeDUSA member")
def assign_is_member(modeladmin, request, queryset: QuerySet[User]):
    for user in queryset:
        if user.is_medusa is False:
            user.is_member = True
            user.save()


@admin.register(User)
class UserAdmin(cuUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (
        ("Personal info", {"fields": ("name", "email", "password", "member_id")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "is_medusa",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined", "membership_expiry")}),
    )
    list_display = [
        "email",
        "name",
        "member_id",
        "last_login",
        "is_staff",
        "is_medusa",
        "is_member",
        "groups_list",
    ]
    search_fields = ["email", "name"]
    readonly_fields = ["all_emails", "member_id"]
    list_filter = ["is_active", "is_staff", "is_medusa", "is_member", "groups", "membership_expiry"]
    actions = [
        set_staff_status,
        set_medusa_status,
        set_name_from_memberlist,
        set_reviewer_status,
        gen_contribution_certificates,
        create_member_ids,
        assign_is_member,
    ]

    def groups_list(self, obj):
        return ", ".join([g.name for g in obj.groups.all()])


@admin.register(MemberRecordsImport)
class MemberRecordsImportAdmin(admin.ModelAdmin):
    list_display = ["id", "import_dt", "report_date", "file"]
    readonly_fields = ("id", "report_date")
    fields = ["members", "file"]
    actions = [import_users]


@admin.register(MemberRecord)
class MemberRecordAdmin(admin.ModelAdmin):
    list_display = ["email", "name", "end_date", "import_date", "is_welcome_email_sent", "date_welcome_email_sent"]
    list_display_links = ["email", "name"]
    fields = ["email", "name", "end_date", "import_date", "is_welcome_email_sent", "date_welcome_email_sent"]
    search_fields = ["email", "name"]
    readonly_fields = ["import_date", "date_welcome_email_sent"]
    list_filter = ["end_date", "is_welcome_email_sent"]


@admin.register(ContributionType)
class ContributionTypeAdmin(admin.ModelAdmin):
    list_display = ["name", "machine_name", "requires_signoff"]
    list_display_links = ["name", "machine_name"]
    fields = ["name", "machine_name", "requires_signoff", "signoff_requirements"]
    search_fields = ["name", "machine_name"]


@admin.action(description="Sign off selected contributions")
def sign_off_contributions(modeladmin, request, queryset: QuerySet[Contribution]):
    assert request.user.has_contrib_sign_off_permission()
    for contrib in queryset:
        contrib.sign(signer=request.user)


@admin.register(Contribution)
class ContributionAdmin(admin.ModelAdmin):
    list_display = ["user", "date", "type", "requires_signing", "signed_off_date", "signed_off_by"]
    list_display_links = ["type"]
    search_fields = ["user", "type"]
    list_filter = ["requires_signing", "type", "is_signed_off", "signed_off_date"]
    readonly_fields = ["requires_signing", "is_signed_off", "signed_off_date"]
    actions = [sign_off_contributions]

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields["signed_off_by"].queryset = Group.objects.get(name="Contributions Sign Off").user_set.all()
        return form
