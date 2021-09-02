# Register your models here.

from django.contrib import admin

from .models import CommitteeMember, SubCommittee


class CommitteeMemberInline(admin.TabularInline):
    model = CommitteeMember


@admin.register(SubCommittee)
class SubCommitteeAdmin(admin.ModelAdmin):
    list_display = [
        "id", "title",
    ]
    search_fields = ("title",)
    inlines = [CommitteeMemberInline]


@admin.register(CommitteeMember)
class CommitteeMemberAdmin(admin.ModelAdmin):
    list_display = [
        "email",
        "position",
        "name",
    ]
    search_fields = ("title", "position", "email", "name")
