import logging

from vanilla import TemplateView

logger = logging.getLogger(__name__)


class HomeView(TemplateView):
    template_name = "pages/home.html"


class AboutView(TemplateView):
    template_name = "pages/home.html"
