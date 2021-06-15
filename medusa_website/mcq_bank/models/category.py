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
        return reverse("mcq_bank:category_detail", kwargs={"id": self.id})

    @classmethod
    def new_category(cls, name):
        new_category = cls(name=re.sub("\s+", "-", name).lower())

        new_category.save()
        return new_category
