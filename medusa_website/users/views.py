import logging

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView

User = get_user_model()
logger = logging.getLogger(__name__)


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    slug_field = "email"
    slug_url_kwarg = "email"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ["name", "email"]

    def get_success_url(self):
        return reverse("users:detail", kwargs={"email": self.request.user.email})

    def get_object(self, **kwargs):
        return User.objects.get(email=self.request.user.email)

    def form_valid(self, form):
        messages.add_message(self.request, messages.INFO, _("User details successfully updated"))
        return super().form_valid(form)


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        logger.info(f"UserRedirectView(): {self.request}")
        return reverse("users:detail", kwargs={"email": self.request.user.email})


user_redirect_view = UserRedirectView.as_view()
