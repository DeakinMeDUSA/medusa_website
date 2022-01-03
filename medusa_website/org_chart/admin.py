# Register your models here.

from django.contrib import admin

from .models import CommitteeRole, CommitteeRoleRecord, SubCommittee


class CommitteeRoleInline(admin.TabularInline):
    model = CommitteeRole
    extra = 0


class CommitteeRoleRecordInline(admin.TabularInline):
    model = CommitteeRoleRecord
    extra = 0


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
    inlines = [CommitteeRoleRecordInline]


@admin.register(CommitteeRoleRecord)
class CommitteeRoleRecordAdmin(admin.ModelAdmin):
    list_display = ["role", "user", "year"]
    search_fields = (
        "role__position",
        "user__email",
    )
