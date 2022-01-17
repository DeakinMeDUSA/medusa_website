from django.contrib import admin
from django.db.models import QuerySet

from medusa_website.users.forms import User
from medusa_website.users.models import MemberRecord, MemberRecordsImport


@admin.action(description="Import users from memberlist")
def import_users(modeladmin, request, queryset: QuerySet[MemberRecordsImport]):
    for obj in queryset:
        if obj.file:
            obj.import_memberlist()
        else:
            print(f"No file for memberlist record {obj}")


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


@admin.action(description="Mark selected MemberRecords as Welcome Email Sent = True")
def mark_welcome_email_sent(modeladmin, request, queryset: QuerySet[MemberRecord]):
    for member in queryset:
        if not member.is_welcome_email_sent:
            member.is_welcome_email_sent = True
            member.save()


@admin.register(MemberRecord)
class MemberRecordAdmin(admin.ModelAdmin):
    list_display = ["email", "name", "end_date", "import_date", "is_welcome_email_sent", "date_welcome_email_sent"]
    list_display_links = ["email", "name"]
    fields = ["email", "name", "end_date", "import_date", "is_welcome_email_sent", "date_welcome_email_sent"]
    search_fields = ["email", "name"]
    readonly_fields = ["import_date", "date_welcome_email_sent"]
    list_filter = ["end_date", "is_welcome_email_sent"]
    actions = [convert_member_into_user, mark_welcome_email_sent]
