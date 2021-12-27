from django.contrib import admin
from imagekit.admin import AdminThumbnail

from .models import Level, OSCEHistory, OSCEStation, Speciality, StationType


@admin.register(OSCEStation)
class OSCEStationAdmin(admin.ModelAdmin):
    stem_image_thumbnail = AdminThumbnail(image_field="stem_image")
    marking_guide_image_thumbnail = AdminThumbnail(image_field="marking_guide_image")
    supporting_notes_image_thumbnail = AdminThumbnail(image_field="supporting_notes_image")

    list_display = [
        "id",
        "title",
        "level",
        "author",
        "is_flagged",
        "is_reviewed",
    ]
    readonly_fields = (
        "id",
        "stem_image_thumbnail",
        "marking_guide_image_thumbnail",
        "supporting_notes_image_thumbnail",
    )
    fields = [
        "title",
        "level",
        "types",
        "specialities",
        "author",
        "stem",
        "patient_script",
        "marking_guide",
        "supporting_notes",
        "is_flagged",
        "flagged_by",
        "is_reviewed",
        "reviewed_by",
        "stem_image_thumbnail",
        "stem_image",
        "marking_guide_image_thumbnail",
        "marking_guide_image",
        "supporting_notes_image_thumbnail",
        "supporting_notes_image",
    ]
    list_filter = ("level", "author")
    search_fields = ("title", "author")
    filter_horizontal = ("types", "specialities")  # Must be many-to-many


@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    search_fields = ("level",)


@admin.register(StationType)
class StationTypeAdmin(admin.ModelAdmin):
    search_fields = ("StationType",)


@admin.register(Speciality)
class SpecialityAdmin(admin.ModelAdmin):
    search_fields = ("Speciality",)


@admin.register(OSCEHistory)
class OSCEHistoryAdmin(admin.ModelAdmin):
    search_fields = ("user",)
