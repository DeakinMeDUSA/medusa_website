# Register your models here.

from django.contrib import admin

from .models import Sponsor, Supporter, OfficialDocumentation


@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):
    list_display = [
        "id", "name", "website"
    ]
    search_fields = ("name", "website")


@admin.register(Supporter)
class SupporterAdmin(SponsorAdmin):
    ...


@admin.register(OfficialDocumentation)
class OfficialDocumentationAdmin(admin.ModelAdmin):
    list_display = [
        "id", "name", "file"
    ]
    search_fields = ("name", "id")
