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
    list_display = ["email", "name", "is_superuser"]
    search_fields = ["email"]
    readonly_fields = ["all_emails"]
    #
    # def all_emails(self, obj):
    #     return obj.all_emails()


def update_from_excel(modeladmin, request, queryset: QuerySet):
    queryset.first().create_from_export()


update_from_excel.short_description = "Update MemberRecordImport from excel"


@admin.register(MemberRecordsImport)
class MemberRecordsImportAdmin(admin.ModelAdmin):
    list_display = ["id", "import_dt"]
    readonly_fields = ("id",)
    fields = ["id", "import_dt", "members"]
    actions = [update_from_excel]


@admin.register(MemberRecord)
class MemberRecordAdmin(admin.ModelAdmin):
    list_display = ["email", "name"]
    list_display_links = ["email", "name"]
    readonly_fields = ("email",)

    fields = ["email", "name", "end_date", "import_records"]
