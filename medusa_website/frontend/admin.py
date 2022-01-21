# Register your models here.

from django.contrib import admin
from django.db.models import QuerySet

from .models import Sponsor, Supporter, OfficialDocumentation, Publication, ConferenceReport, ElectiveReport, \
    PublicationType


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
        "id", "name", "file", "publish_year"
    ]
    search_fields = ("name", "id")


@admin.action(description='Generate thumnails for selected publications')
def generate_thumbnails(modeladmin, request, queryset: QuerySet[Publication]):
    for pub in queryset.all():
        pub.gen_pdf_thumbnail()


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = [
        "id", "name", "pdf", "pub_date", "has_thumbnail",  "type"
    ]
    list_display_links = ["name"]
    search_fields = ("name", "id")
    fields = ["name", "pdf", "pub_date", "type"]
    extra_modify_fields = ["thumbnail"]
    list_filter = ["pub_date", "type"]

    def get_fields(self, request, obj=None):
        fields = list(super().get_fields(request, obj))

        if obj:  # editing an existing object
            fields.extend(self.extra_modify_fields)

        return fields




@admin.register(PublicationType)
class PublicationTypeAdmin(admin.ModelAdmin):
    list_display = ["type", "machine_type"]
    fields = ["type", "display_description"]
    search_fields = ["type"]


@admin.register(ConferenceReport)
class ConferenceReportAdmin(admin.ModelAdmin):
    list_display = [
        "id", "conference_name", "conference_year", "conference_city", "report_author", "file"
    ]
    search_fields = list_display


@admin.register(ElectiveReport)
class ElectiveReportAdmin(admin.ModelAdmin):
    list_display = [
        "id", "elective_name", "elective_year", "elective_city", "report_author", "file"
    ]
    search_fields = list_display
