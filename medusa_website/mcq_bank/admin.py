# Register your models here.

from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from imagekit.admin import AdminThumbnail

from .models import Answer, Category, History, Question, Quiz


class AnswerInline(admin.TabularInline):
    model = Answer


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    admin_thumbnail = AdminThumbnail(image_field="image")
    list_display = [
        "id",
        "text",
        "has_image",
        "image_url",
        "category",
    ]
    readonly_fields = ("id", "admin_thumbnail")
    fields = [
        "text",
        "category",
        "sub_category",
        "author",
        "image",
        "admin_thumbnail",
        "quiz",
        "explanation",
        "answer_order",
    ]
    list_filter = ("category",)
    search_fields = ("text", "explanation")
    filter_horizontal = ("quiz",)

    inlines = [AnswerInline]


class QuizAdminForm(forms.ModelForm):
    """
    below is from
    http://stackoverflow.com/questions/11657682/django-admin-interface-using-horizontal-filter-with-inline-manytomany-field
    """

    class Meta:
        model = Quiz
        exclude = []

    questions = forms.ModelMultipleChoiceField(
        queryset=Question.objects.all(),
        required=False,
        label="Questions",
        widget=FilteredSelectMultiple(verbose_name="Questions", is_stacked=False),
    )

    def __init__(self, *args, **kwargs):
        super(QuizAdminForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields["questions"].initial = self.instance.questions.all()

    def save(self, commit=True):
        quiz = super(QuizAdminForm, self).save(commit=False)
        quiz.save()
        quiz.questions.set(self.cleaned_data["questions"])
        self.save_m2m()
        return quiz


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    form = QuizAdminForm

    list_display = (
        "title",
        "category",
    )
    list_filter = ("category",)
    search_fields = (
        "description",
        "category",
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ("category",)


@admin.register(History)
class ProgressAdmin(admin.ModelAdmin):
    """
    to do:
            create a user section
    """

    search_fields = ("user",)
