import markdown
from django import forms
from django.db.models.fields.files import ImageFieldFile
from django.utils.safestring import mark_safe

from medusa_website.users.models import User


class AuthorNameWidget(forms.Widget):
    def render(self, name, value, attrs=None, renderer=None):
        if value:
            author = User.objects.get(id=value)
            return mark_safe(f"<b>{author.name}</b>") if value is not None else "-"
        else:
            return mark_safe("-")


class RenderMarkdownWidget(forms.Widget):
    def __init__(self, css_class: str = None, *args, **kwargs):
        self.css_class = css_class
        super(RenderMarkdownWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, renderer=None):
        if value:
            html = f'<div class="{self.css_class}">{markdown.markdown(value)}</div>'
            return mark_safe(html)
        else:
            return mark_safe("None")


class ImageDisplayWidget(forms.Widget):
    def __init__(self, max_width="50vw", max_height="50vh", *args, **kwargs):
        self.max_width = max_width
        self.max_height = max_height
        super(ImageDisplayWidget, self).__init__(*args, **kwargs)

    def render(self, name, value: ImageFieldFile, attrs=None, renderer=None):
        if value:
            style = f"max-width: {self.max_width}; max-height: {self.max_height};"
            html = f'<a href="{value.url}"><img src="{value.url}" style="{style}"/></a>'
            # html = f'<img src="{value.url}" style="{style}" onclick="enlargeImg(this)"/>'

            return mark_safe(html)
        else:
            return mark_safe("None")
