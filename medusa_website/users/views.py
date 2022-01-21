from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView
from vanilla import CreateView, FormView

from medusa_website.users.forms import MemberDetailForm
from medusa_website.users.models import ContributionCertificate, User
from medusa_website.utils.general import get_pretty_logger

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
            raise PermissionDenied(self.permission_denied_message)
        form = self.get_form()
        context = self.get_context_data(form=form)
        context["member"] = self.get_object()
        return self.render_to_response(context)


member_check_view = MemberCheckView.as_view()


class ContributionCertificateCreateView(LoginRequiredMixin, CreateView):
    """This view is only for auto-generating them for users, for custom ones, create them from the admin interface."""

    template_name = "users/contribution_certificate.html"
    model = ContributionCertificate
    form_class = None

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        created_cert = context["cert"]
        # flush messages
        list(messages.get_messages(request))
        message = mark_safe(
            f"Certificate successfully created - "
            f'<a href="{reverse("users:certificate_pdf", kwargs={"id": created_cert.id})}" target="_blank">View here</a>'
        )
        messages.add_message(request, messages.SUCCESS, message)
        return redirect("users:detail", email=request.user.email)

    def dispatch(self, request, clean_existing=True, *args, **kwargs):
        # Redirect if certificate was recently created to avoid spamming the expensive endpoint
        existing_certs = ContributionCertificate.objects.filter(user=request.user, autogenerated=True)
        latest_cert = existing_certs.latest("date_modified") if existing_certs else None
        if clean_existing and latest_cert:  # Don't regenerate them if they were only generated in the last day
            time_delta = datetime.today().date() - latest_cert.date_modified
            if time_delta.days <= 1:
                return redirect("users:certificate_pdf", id=latest_cert.id)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = kwargs
        if not kwargs.get("object"):  # Create new one
            logger.info(f"Cleaning up existing un-signed auto-generated certificates")
            ContributionCertificate.objects.filter(
                user=self.request.user, autogenerated=True, is_signed_off=False
            ).delete()
            cert: ContributionCertificate = self.request.user.gen_contribution_certificate()
        else:
            cert = kwargs["object"]
        cert_user = cert.user
        cert_signers = cert.cert_signers()
        context["view"] = self
        context["cert_user"] = cert_user
        context["cert"] = cert
        context["cert_details"] = cert.details_as_html()
        if cert.is_signed_off:
            context["signer_1"] = cert_signers[0]
            context["signer_2"] = cert_signers[1]
            context["date"] = cert.signed_off_date
        else:
            context["date"] = cert.date_modified

        context["is_signed"] = cert.is_signed_off

        return context


contribution_certificate_create_view = ContributionCertificateCreateView.as_view()


class ContributionCertificateDetailView(ContributionCertificateCreateView, DetailView):
    model = ContributionCertificate
    lookup_field = "id"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def dispatch(self, request, *args, **kwargs):
        cert = self.get_object()
        context = self.get_context_data(object=cert)
        # Only allow  Contribution Sign Off to view/create them, or users to view their own (will be generated
        # without signature)"
        if not request.user.has_contrib_sign_off_permission() and request.user != cert.user:
            return self.handle_no_permission()
        return super().dispatch(request, clean_existing=False, *args, **kwargs)


contribution_certificate_detail_view = ContributionCertificateDetailView.as_view()


# class ContributionCertificateSignedDetailView(ContributionCertificateDetailView):
#     model = ContributionCertificate
#     lookup_field = "id"
#
#     def get(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         context = self.get_context_data(object=self.object)
#         return self.render_to_response(context)
#
#     def dispatch(self, request, *args, **kwargs):
#         cert = self.get_object()
#         context = self.get_context_data(object=cert)
#         # Only allow  Contribution Sign Off to view/create them, or users to view their own (will be generated
#         # without signature)"
#         if not request.user.has_contrib_sign_off_permission() and request.user != cert.user:
#             return self.handle_no_permission()
#         return super().dispatch(request, clean_existing=False, *args, **kwargs)
#
#
# contribution_certificate_detail_view = ContributionCertificateDetailView.as_view()


@login_required
def contribution_certificate_pdf_view(request, *args, **kwargs):
    user: User = request.user
    cert: ContributionCertificate = ContributionCertificate.objects.get(id=kwargs.get("id"))
    if not user.has_contrib_sign_off_permission() and request.user != cert.user:
        raise PermissionDenied("Users can only view their own certificates, or admins!")
    if "preview_pdf" in cert.pdfs_to_gen():
        cert.gen_pdf(request=request, signed=False)
    return redirect(cert.preview_pdf.url)


@login_required
def contribution_certificate_signed_pdf_view(request, *args, **kwargs):
    user: User = request.user
    cert: ContributionCertificate = ContributionCertificate.objects.get(id=kwargs.get("id"))
    if not cert.is_signed_off:
        raise PermissionDenied("Certificate is not signed off yet!")
    if not user.has_contrib_sign_off_permission() and request.user != cert.user:
        raise PermissionDenied("Users can only view their own certificates, or admins!")

    if "signed_pdf" in cert.pdfs_to_gen():
        cert.gen_pdf(request=request, signed=True)
    return redirect(cert.signed_pdf.url)


@login_required
def contribution_certificate_delete_view(request, *args, **kwargs):
    user: User = request.user
    cert = ContributionCertificate.objects.get(id=kwargs.get("id"))
    if not user.has_contrib_sign_off_permission() and request.user != cert.user:
        raise PermissionDenied("Users can only view their own certificates, or admins!")
    cert.delete()
    messages.add_message(request, messages.SUCCESS, "Certificate successfully deleted")

    return redirect("users:detail", email=request.user.email)


@login_required
def contribution_certificate_request_sign_view(request, *args, **kwargs):
    user: User = request.user
    cert = ContributionCertificate.objects.get(id=kwargs.get("id"))
    if not user.has_contrib_sign_off_permission() and request.user != cert.user:
        raise PermissionDenied("Users can only request signoff on their own certs, or admins")

    cert.send_signoff_request(request)
    messages.add_message(request, messages.SUCCESS, "Certificate request for signoff successfully sent")

    return redirect("users:detail", email=request.user.email)
