from cuser.admin import UserAdmin as cuUserAdmin
from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.db.models import QuerySet
from django.urls import reverse
from django.utils.encoding import smart_text
from django.utils.html import format_html
from nameparser import HumanName

from medusa_website.users.forms import UserChangeForm, UserCreationForm

from .models import (
    Contribution,
    ContributionCertificate,
    ContributionType,
    MemberRecord,
    MemberRecordsImport,
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
    readonly_fields = ["all_emails", "member_id"]
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


@admin.register(MemberRecordsImport)
class MemberRecordsImportAdmin(admin.ModelAdmin):
    list_display = ["id", "import_dt", "report_date", "file"]
    readonly_fields = ("id", "report_date")
    fields = ["members", "file"]
    actions = [import_users]


@admin.action(description="Convert the selected member(s) into Users if they do not exist")
def convert_member_into_user(modeladmin, request, queryset: QuerySet[MemberRecord]):
    for member in queryset:
        try:
            user = User.objects.get(email=member.email)
        except User.DoesNotExist:
            user = User(email=member.email, name=member.name, membership_expiry=member.end_date, is_member=True)
            user.save()
            user.create_member_id()


@admin.register(MemberRecord)
class MemberRecordAdmin(admin.ModelAdmin):
    list_display = ["email", "name", "end_date", "import_date", "is_welcome_email_sent", "date_welcome_email_sent"]
    list_display_links = ["email", "name"]
    fields = ["email", "name", "end_date", "import_date", "is_welcome_email_sent", "date_welcome_email_sent"]
    search_fields = ["email", "name"]
    readonly_fields = ["import_date", "date_welcome_email_sent"]
    list_filter = ["end_date", "is_welcome_email_sent"]
    actions = [convert_member_into_user]


@admin.register(ContributionType)
class ContributionTypeAdmin(admin.ModelAdmin):
    list_display = ["name", "machine_name", "requires_signoff", "subtype"]
    list_display_links = ["name", "machine_name"]
    fields = ["name", "machine_name", "requires_signoff", "signoff_requirements", "subtype", "template"]
    search_fields = ["name", "machine_name", "subtype"]
    list_filter = ["subtype"]


@admin.action(description="Sign off selected certificates")
def sign_certificates(modeladmin, request, queryset: QuerySet[ContributionCertificate]):
    for cert in queryset:
        if not cert.is_signed_off:
            cert.sign_with_user(request=request, signing_user=request.user, email_user=True)


@admin.action(description="Generate pdfs for the selected certificates, overwriting existing ones if present")
def generate_certificate_pdfs(modeladmin, request, queryset: QuerySet[ContributionCertificate]):
    for cert in queryset:
        cert.gen_pdf(request=request)


class ContributionCertificateAdminSignersFilter(admin.SimpleListFilter):
    title = "Signed off by"
    parameter_name = "signed_off_by"

    def lookups(self, request, model_admin):
        signers = Group.objects.get(name="Contributions Sign Off").user_set.all()
        for obj in signers:
            yield (str(obj.pk), smart_text(obj))

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(signed_off_by__id=self.value())


class UserChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj: User):
        return f"{obj.name} - {obj.email}"


@admin.register(ContributionCertificate)
class ContributionCertificateAdmin(admin.ModelAdmin):
    autocomplete_fields = [
        "user",
    ]
    list_display = [
        "id",
        "user",
        "is_signed_off",
        "signed_off_date",
        "signed_off_by",
        "autogenerated",
        "sent_for_signoff",
        "date_sent_for_signoff",
        "view_certificate",
        "signed_pdf",
        "preview_pdf",
    ]
    list_display_links = ["user"]
    search_fields = ["user__email", "user__name"]
    list_filter = [
        "is_signed_off",
        "autogenerated",
        ContributionCertificateAdminSignersFilter,
        "sent_for_signoff",
        "date_sent_for_signoff",
    ]
    actions = [sign_certificates, generate_certificate_pdfs]
    readonly_fields = [
        "signed_pdf",
        "is_signed_off",
        "signed_off_by",
        "signed_off_date",
        "date_sent_for_signoff",
        "sent_for_signoff",
    ]
    fieldsets = (
        ("Certificate Details", {"fields": ("user", "details", "autogenerated")}),
        ("Generated PDFs", {"fields": ("preview_pdf", "signed_pdf")}),
        (
            "Sign-off",
            {
                "fields": (
                    "sent_for_signoff",
                    "date_sent_for_signoff",
                    "is_signed_off",
                    "signed_off_by",
                    "signed_off_date",
                )
            },
        ),
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        db = kwargs.get("using")

        if db_field.name == "signed_off_by":
            kwargs["queryset"] = Group.objects.get(name="Contributions Sign Off").user_set.all()
        # if db_field.name == 'user':
        #     kwargs['widget'] = AutocompleteSelect(db_field, self.admin_site, using=db)
        #     return UserChoiceField(queryset=User.objects.filter(is_medusa=False))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = self.readonly_fields
        if obj and obj.is_signed_off:  # Don't allow it to be edited afterwards
            readonly_fields.extend(["details", "autogenerated", "preview_pdf", "signed_pdf"])
        return readonly_fields

    def view_certificate(self, obj: ContributionCertificate):
        return format_html(
            f'<a href="{reverse("users:certificate_pdf", kwargs={"id": obj.id})}">View certificate {obj.id}</a>'
        )


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
