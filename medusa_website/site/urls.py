from django.urls import path
from vanilla import TemplateView

from medusa_website.site.views import AboutView

app_name = "site"
urlpatterns = [
    path("", view=TemplateView.as_view(template_name="site/index.html"), name="index"),
    path("index/", view=TemplateView.as_view(template_name="site/index.html"), name="index"),
    path("elements/", view=TemplateView.as_view(template_name="site/elements.html"), name="elements"),
    path("generic/", view=TemplateView.as_view(template_name="site/generic.html"), name="generic"),
    path("sponsors/", view=TemplateView.as_view(template_name="site/sponsors.html"), name="sponsors"),
    path("about/", view=AboutView.as_view(), name="about"),

]

# TODO link detail view to use a modified UPdateView to keep things DRY
