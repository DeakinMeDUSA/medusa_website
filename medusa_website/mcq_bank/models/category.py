import re

from django.db import models


class CategoryManager(models.Manager):
    def new_category(self, category):
        new_category = self.create(category=re.sub("\s+", "-", category).lower())

        new_category.save()
        return new_category


class Category(models.Model):
    category = models.CharField(
        verbose_name="Category", max_length=250, blank=True, unique=True, null=True
    )

    objects = CategoryManager()

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.category


class SubCategory(models.Model):
    sub_category = models.CharField(
        verbose_name="Sub-Category", max_length=250, blank=True, null=True
    )

    category = models.ForeignKey(
        Category,
        null=True,
        blank=True,
        verbose_name="Category",
        on_delete=models.CASCADE,
    )

    objects = CategoryManager()

    class Meta:
        verbose_name = "Sub-Category"
        verbose_name_plural = "Sub-Categories"

    def __str__(self):
        return f"{self.sub_category} ({self.category.category})"
