import django_tables2 as tables
from django.shortcuts import get_object_or_404
from django.utils.html import format_html
from django.views.generic import ListView

from medusa_website.mcq_bank.models import Category, Question


class CategoriesTable(tables.Table):
    class Meta:
        model = Category
        attrs = {"class": "table"}
        fields = ("category", "num_questions")

    # id = tables.Column(linkify=True)
    category = tables.Column(linkify=True)
    num_questions = tables.Column(verbose_name="No. of questions", accessor="questions__count")


class CategoriesTableView(tables.SingleTableView):
    model = Category
    table_class = CategoriesTable
    template_name = "mcq_bank/category_list.html"


class ViewQuestionsByCategoryView(ListView):
    model = Question
    template_name = "mcq_bank/view_quiz_category.html"

    def dispatch(self, request, *args, **kwargs):
        self.category = get_object_or_404(Category, category=self.kwargs["category_name"])

        return super(ViewQuestionsByCategoryView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ViewQuestionsByCategoryView, self).get_context_data(**kwargs)

        context["category"] = self.category
        return context

    def get_queryset(self):
        queryset = super(ViewQuestionsByCategoryView, self).get_queryset()
        return queryset.filter(category=self.category)
