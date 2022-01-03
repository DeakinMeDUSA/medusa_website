from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView
from playwright.sync_api import sync_playwright
from vanilla import FormView

from medusa_website.users.forms import MemberDetailForm
from medusa_website.users.models import ContributionCertificate
from medusa_website.utils.general import get_pretty_logger

User = get_user_model()
logger = get_pretty_logger(__name__)


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
        return reverse("users:detail", kwargs={"email": self.request.user.email})


user_redirect_view = UserRedirectView.as_view()


class MemberCheckView(LoginRequiredMixin, FormView, DetailView):
    form_class = MemberDetailForm
    template_name = "users/member_check.html"
    model = User
    context_object_name = "user"
    lookup_field = "member_id"
    queryset = User.objects.filter(is_member=True)
    permission_denied_message = (
        "You must be a MeDUSA committee or other club committee member to access this page."
        "For any queries, contact it@medusa.org.au"
    )

    def test_func(self):
        return self.request.user.is_staff

    def get_success_url(self):
        return reverse("users:member_check", kwargs={"member_id": self.request.POST["member_id"]})

    def get_object(self, queryset=None):
        """
        Returns the object the view is displaying.
        """
        if self.kwargs.get("member_id"):
            self.member = User.objects.get(member_id=self.kwargs["member_id"])
            return self.member
        else:
            self.member = None
            return None

    def get(self, request, *args, **kwargs):
        if not self.request.user.is_staff:
            raise PermissionError(self.permission_denied_message)
        form = self.get_form()
        context = self.get_context_data(form=form)
        context["member"] = self.get_object()
        return self.render_to_response(context)


member_check_view = MemberCheckView.as_view()


class ContributionCertificateView(LoginRequiredMixin, DetailView):
    template_name = "users/contribution_certificate.html"

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = kwargs
        user: User = User.objects.get(email="cfculhane@gmail.com")  # self.request.user
        user.gen_contribution_certificate()
        contribution_certificate: ContributionCertificate = user.contribution_certificate
        cert_signers = contribution_certificate.cert_signers()
        context["view"] = self
        context["user"] = user
        context["contribution_certificate"] = contribution_certificate
        context["cert_details"] = contribution_certificate.details_as_html()
        context["date_modified"] = contribution_certificate.date_modified
        context["signer_1"] = cert_signers[0]
        context["signer_2"] = cert_signers[1]

        return context


contribution_certificate_view = ContributionCertificateView.as_view()


def contribution_certificate_pdf_view(request):
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="report.pdf"'
    # find the template and render it.
    headers = dict(request.headers)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.set_extra_http_headers({"Cookie": headers["Cookie"]})
        page.goto("http://localhost:8000/users/certificate/")
        print(page.title())
        # https://playwright.dev/python/docs/api/class-page#page-pdf
        # Image size is 1754 x 1240 ––>
        pdf = page.pdf(prefer_css_page_size=True, print_background=True, width="1754px", height="1240px")
        browser.close()
    response.content = pdf
    return response
