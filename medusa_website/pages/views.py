import logging

from vanilla import TemplateView

logger = logging.getLogger(__name__)


class HomeView(TemplateView):
    template_name = "pages/home.html"

    def get_context_data(self, **kwargs):
        user = self.request.user
        logger.info(f"user = {user} | authenticated = {user.is_authenticated}")
        return super(HomeView, self).get_context_data(**kwargs)
