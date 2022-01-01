# Register your models here.

from django.contrib import admin

from .models import CommitteeRole, SubCommittee


class CommitteeMemberInline(admin.TabularInline):
    model = CommitteeRole


@admin.register(SubCommittee)
class SubCommitteeAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "title",
    ]
    search_fields = ("title",)
    inlines = [CommitteeMemberInline]


@admin.register(CommitteeRole)
class CommitteeRoleAdmin(admin.ModelAdmin):
    list_display = ["email", "position", "sub_committee"]
    search_fields = (
        "position",
        "email",
    )
