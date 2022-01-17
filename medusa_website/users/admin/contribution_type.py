from django.contrib import admin

from medusa_website.users.models import ContributionType


@admin.register(ContributionType)
class ContributionTypeAdmin(admin.ModelAdmin):
    list_display = ["name", "machine_name", "requires_signoff", "subtype"]
    list_display_links = ["name", "machine_name"]
    fields = ["name", "machine_name", "requires_signoff", "signoff_requirements", "subtype", "template"]
    search_fields = ["name", "machine_name", "subtype"]
    list_filter = ["subtype"]
