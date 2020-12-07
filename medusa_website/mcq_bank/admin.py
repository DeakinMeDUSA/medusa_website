# Register your models here.

from django.contrib import admin
from imagekit.admin import AdminThumbnail

from .models import Answer, Question


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    admin_thumbnail = AdminThumbnail(image_field="image")
    list_display = [
        "id",
        "question_text",
        "has_image",
        "image_url",
    ]
    readonly_fields = ("id", "admin_thumbnail")
    fields = ["question_text", "author", "image", "admin_thumbnail"]


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ["id", "answer_text", "is_correct"]
    eadonly_fields = ("id",)
    fields = ["answer_text", "question", "is_correct"]
