# Register your models here.

from django.contrib import admin
from django.db.models import QuerySet

from .models import Sponsor, Supporter, OfficialDocumentation, Publication


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
        "id", "name", "pdf", "pub_date", "has_thumbnail"
    ]
    search_fields = ("name", "id")
    actions = [generate_thumbnails]
