from django.urls import path
from vanilla import TemplateView

from medusa_website.frontend.views import AboutView, ContactView

app_name = "frontend"
urlpatterns = [
    path("", view=TemplateView.as_view(template_name="frontend/index.html"), name="index"),
    path("index/", view=TemplateView.as_view(template_name="frontend/index.html"), name="index"),
    path("elements/", view=TemplateView.as_view(template_name="frontend/elements.html"), name="elements"),
    path("generic/", view=TemplateView.as_view(template_name="frontend/generic.html"), name="generic"),
    path("events/", view=TemplateView.as_view(template_name="frontend/events.html"), name="events"),
    path("about/", view=AboutView.as_view(), name="about"),
    path("contact/", view=ContactView.as_view(), name="contact"),

]

# TODO link detail view to use a modified UPdateView to keep things DRY
