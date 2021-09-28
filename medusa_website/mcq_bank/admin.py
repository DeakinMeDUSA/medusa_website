# Register your models here.

from django.contrib import admin
from imagekit.admin import AdminThumbnail

from .models import Answer, Category, History, Question, Record, QuizSession


class AnswerInline(admin.TabularInline):
    model = Answer


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    question_image_thumbnail = AdminThumbnail(image_field="question_image")
    answer_image_thumbnail = AdminThumbnail(image_field="answer_image")

    list_display = [
        "id",
        "text",
        "has_question_image",
        "has_answer_image",
        "question_image_url",
        "answer_image_url",
        "category",
    ]
    readonly_fields = ("id", "question_image_thumbnail", "answer_image_thumbnail")
    fields = [
        "text",
        "category",
        "author",
        "question_image",
        "answer_image",
        "question_image_thumbnail",
        "answer_image_thumbnail",
        "explanation",
        "randomise_answer_order",
    ]
    list_filter = ("category",)
    search_fields = ("text", "explanation")
    # filter_horizontal = ("quiz",) # Must be many-to-many

    inlines = [AnswerInline]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ("category",)


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    search_fields = ("user",)


@admin.register(QuizSession)
class QuizSessionAdmin(admin.ModelAdmin):
    search_fields = ("user", "id")
    list_display = ["id", "user", "started", "finished", "complete"]
    list_filter = ["user", "started", "finished", "complete"]


@admin.register(History)
class ProgressAdmin(admin.ModelAdmin):
    """
    to do:
            create a user section
    """

    search_fields = ("user",)
