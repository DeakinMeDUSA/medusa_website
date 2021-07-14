from django.urls import path
from vanilla import TemplateView

app_name = "site"
urlpatterns = [
    path("index/", view=TemplateView.as_view(template_name="site/index.html"), name="index"),
    path("elements/", view=TemplateView.as_view(template_name="site/elements.html"), name="elements"),
    path("generic/", view=TemplateView.as_view(template_name="site/generic.html"), name="generic"),

]

# TODO link detail view to use a modified UPdateView to keep things DRY
