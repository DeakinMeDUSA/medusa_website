from cuser.admin import UserAdmin as cuUserAdmin
from django.contrib import admin
from django.contrib.auth.models import Group
from django.db.models import QuerySet
from nameparser import HumanName

from medusa_website.users.forms import UserChangeForm, UserCreationForm
from medusa_website.users.models import (
    Contribution,
    ContributionCertificate,
    MemberRecord,
    User,
)


@admin.action(description="Set selected users is_staff = True")
def set_staff_status_true(modeladmin, request, queryset: QuerySet[User]):
    for user in queryset:
        user.is_staff = True
        user.save()


@admin.action(description="Set selected users is_staff = False")
def set_staff_status_false(modeladmin, request, queryset: QuerySet[User]):
    for user in queryset:
        user.is_staff = False
        user.save()


@admin.action(description="Set selected users is_medusa = True")
def set_medusa_status_true(modeladmin, request, queryset: QuerySet[User]):
    for user in queryset:
        user.is_medusa = True
        user.save()


@admin.action(description="Set selected users is_medusa = False")
def set_medusa_status_false(modeladmin, request, queryset: QuerySet[User]):
    for user in queryset:
        user.is_medusa = False
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


class ContributionCertificateInline(admin.TabularInline):
    model = ContributionCertificate
    extra = 0
    fk_name = "user"
    show_change_link = True
    readonly_fields = ["signed_off_by", "signed_off_date"]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "signed_off_by":
            kwargs["queryset"] = Group.objects.get(name="Contributions Sign Off").user_set.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class ContributionInline(admin.TabularInline):
    model = Contribution
    extra = 0
    fk_name = "user"
    show_change_link = True
    readonly_fields = ["is_signed_off", "signed_off_by", "signed_off_date"]
    max_num = 20

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "signed_off_by":
            kwargs["queryset"] = Group.objects.get(name="Contributions Sign Off").user_set.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(User)
class UserAdmin(cuUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (
        ("Personal info", {"fields": ("name", "email", "password", "member_id", "signature_image")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "is_member",
                    "is_medusa",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined", "membership_expiry")}),
    )
    inlines = [ContributionInline, ContributionCertificateInline]
    list_display = [
        "email",
        "name",
        "member_id",
        "last_login",
        "is_staff",
        "is_medusa",
        "is_member",
    ]
    search_fields = ["email", "name"]
    readonly_fields = ["all_emails", "member_id", "date_joined", "last_login"]
    list_filter = ["is_active", "is_staff", "is_medusa", "is_member", "groups", "membership_expiry"]
    actions = [
        create_member_ids,
        assign_is_member,
        set_staff_status_true,
        set_staff_status_false,
        set_medusa_status_true,
        set_medusa_status_false,
        set_name_from_memberlist,
        set_reviewer_status,
        gen_contribution_certificates,
    ]
