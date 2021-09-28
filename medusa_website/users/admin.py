from cuser.admin import UserAdmin as cuUserAdmin
from django.contrib import admin
from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _
from nameparser import HumanName

from medusa_website.users.forms import UserChangeForm, UserCreationForm
from .models import MemberRecord, MemberRecordsImport, User


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


@admin.register(User)
class UserAdmin(cuUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("name", "all_emails")}),
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
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_display = ["email", "name", "last_login", "date_joined", "is_superuser", "is_staff", "is_medusa"]
    search_fields = ["email", "name"]
    readonly_fields = ["all_emails"]
    actions = [set_staff_status, set_medusa_status, set_name_from_memberlist]


@admin.register(MemberRecordsImport)
class MemberRecordsImportAdmin(admin.ModelAdmin):
    list_display = ["id", "import_dt", "report_date", "file"]
    readonly_fields = ("id", "report_date")
    fields = ["members", "file"]
    actions = [import_users]


@admin.register(MemberRecord)
class MemberRecordAdmin(admin.ModelAdmin):
    list_display = ["email", "name", "end_date"]
    list_display_links = ["email", "name"]
    fields = ["email", "name", "end_date"]
    search_fields = ["email", "name"]
