import re

from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(verbose_name="Category", max_length=250, blank=True, unique=True, null=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        # Manually add url param as its handled by the filter, reverse() with the param doesn't work
        return f'{reverse("mcq_bank:question_list")}?category={self.id}'

    @classmethod
    def new_category(cls, name):
        new_category = cls(name=re.sub("\s+", "-", name).capitalize())

        new_category.save()
        return new_category
