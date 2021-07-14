from cuser.admin import UserAdmin as cuUserAdmin
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _

from medusa_website.users.forms import UserChangeForm, UserCreationForm
from .models import MemberRecord, MemberRecordsImport

User = get_user_model()


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
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_display = ["email", "name", "last_login", "date_joined", "is_superuser", "is_staff"]
    search_fields = ["email", "name"]
    readonly_fields = ["all_emails"]
    #
    # def all_emails(self, obj):
    #     return obj.all_emails()


@admin.action(description="Import users from memberlist")
def import_users(modeladmin, request, queryset: QuerySet[MemberRecordsImport]):
    for obj in queryset:
        if obj.file:
            obj.import_memberlist()
        else:
            print(f"No file for memberlist record {obj}")


@admin.register(MemberRecordsImport)
class MemberRecordsImportAdmin(admin.ModelAdmin):
    list_display = ["id", "import_dt", "file"]
    readonly_fields = ("id",)
    fields = ["members", "file"]
    actions = [import_users]


@admin.register(MemberRecord)
class MemberRecordAdmin(admin.ModelAdmin):
    list_display = ["email", "name", "end_date"]
    list_display_links = ["email", "name"]
    readonly_fields = ("email",)

    fields = ["email", "name", "end_date"]
    search_fields = ["email", "name"]
