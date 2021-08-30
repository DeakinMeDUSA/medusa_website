from django.urls import path
from vanilla import TemplateView

from medusa_website.frontend.views import AboutView, ContactView, PublicationsView, ResourcesView, TCSSView

app_name = "frontend"
urlpatterns = [
    path("", view=TemplateView.as_view(template_name="frontend/index.html"), name="index"),
    path("index/", view=TemplateView.as_view(template_name="frontend/index.html"), name="index"),
    path("elements/", view=TemplateView.as_view(template_name="frontend/elements.html"), name="elements"),
    path("generic/", view=TemplateView.as_view(template_name="frontend/generic.html"), name="generic"),
    path("events/", view=TemplateView.as_view(template_name="frontend/events.html"), name="events"),
    path("about/", view=AboutView.as_view(), name="about"),
    path("contact/", view=ContactView.as_view(), name="contact"),
    path("publications/", view=PublicationsView.as_view(), name="publications"),
    path("resources/", view=ResourcesView.as_view(), name="resources"),
    path("tcss/", view=TCSSView.as_view(), name="tcss"),
    path("feedback/", view=TemplateView.as_view(template_name="frontend/feedback.html"), name="feedback"),

]

# TODO link detail view to use a modified UPdateView to keep things DRY
