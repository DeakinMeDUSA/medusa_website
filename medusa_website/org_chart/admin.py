# Register your models here.

from django.contrib import admin

from .models import CommitteeMemberRecord, CommitteeRole, SubCommittee


class CommitteeRoleInline(admin.TabularInline):
    model = CommitteeRole


@admin.register(SubCommittee)
class SubCommitteeAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "title",
    ]
    search_fields = ("title",)
    inlines = [CommitteeRoleInline]


@admin.register(CommitteeRole)
class CommitteeRoleAdmin(admin.ModelAdmin):
    list_display = ["email", "position", "sub_committee"]
    search_fields = (
        "position",
        "email",
    )


@admin.register(CommitteeMemberRecord)
class CommitteeMemberRecordAdmin(admin.ModelAdmin):
    list_display = ["role", "user", "year"]
    search_fields = (
        "role",
        "user",
    )
