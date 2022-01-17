from pprint import pformat

from django.contrib import admin
from django.contrib.auth.models import Group
from django.db.models import QuerySet
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.encoding import smart_text
from django.utils.html import format_html

from medusa_website.users.models import ContributionCertificate, User


@admin.action(description="Sign off selected certificates")
def sign_certificates(modeladmin, request, queryset: QuerySet[ContributionCertificate]):
    for cert in queryset:
        if not cert.is_signed_off:
            cert.sign_with_user(request=request, signing_user=request.user, email_user=True)


@admin.action(description="Send off selected certificates for signoff")
def send_certificates_for_signoff(modeladmin, request, queryset: QuerySet[ContributionCertificate]):
    for cert in queryset:
        if not cert.sent_for_signoff:
            cert.send_signoff_request(request)


@admin.action(description="Generate pdfs for the selected certificates, overwriting existing ones if present")
def generate_certificate_pdfs(modeladmin, request, queryset: QuerySet[ContributionCertificate]):
    for cert in queryset:
        cert.gen_pdf(request=request, signed=False)
        if cert.is_signed_off:
            cert.gen_pdf(request=request, signed=True)


@admin.action(description="Copy contribution details to a new cert with a different user")
def copy_certificate_details_to_another_user(modeladmin, request, queryset: QuerySet[ContributionCertificate]):
    # All requests here will actually be of type POST
    # so we will need to check for our special key 'apply'
    # rather than the actual request type
    if queryset.count() != 1:
        raise RuntimeError("Only one certificate can be copied at once!")
    else:
        cert = queryset.first()

    if "apply" in request.POST:
        # The user clicked submit on the intermediate form.
        # Perform our update action:
        emails = set([em.strip() for em in request.POST["email"].split(",") if em.strip() is not None])
        users = []
        for email in emails:
            new_cert_user = User.objects.get(email=email)
            users.append(new_cert_user)
            new_cert = ContributionCertificate(user=new_cert_user, details=cert.details)
            new_cert.save()

        # Redirect back to certificate changelist
        modeladmin.message_user(request, f"Created {len(users)} new certificate(s) for users: {pformat(emails)}")
        return HttpResponseRedirect(reverse("admin:users_contributioncertificate_changelist"))

    return render(request, "admin/contribution_certificate_copy_to_user.html", context={"cert": cert})


class ContributionCertificateAdminSignersFilter(admin.SimpleListFilter):
    title = "Signed off by"
    parameter_name = "signed_off_by"

    def lookups(self, request, model_admin):
        signers = Group.objects.get(name="Contributions Sign Off").user_set.all()
        for obj in signers:
            yield (str(obj.pk), smart_text(obj))

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(signed_off_by__id=self.value())


@admin.register(ContributionCertificate)
class ContributionCertificateAdmin(admin.ModelAdmin):
    autocomplete_fields = [
        "user",
    ]
    list_display = [
        "id",
        "user",
        "is_signed_off",
        "signed_off_date",
        "signed_off_by",
        "autogenerated",
        "sent_for_signoff",
        "date_sent_for_signoff",
        "view_certificate",
        "signed_pdf",
        "preview_pdf",
    ]
    list_display_links = ["user"]
    search_fields = ["user__email", "user__name"]
    list_filter = [
        "is_signed_off",
        "autogenerated",
        ContributionCertificateAdminSignersFilter,
        "sent_for_signoff",
        "date_sent_for_signoff",
    ]
    actions = [
        sign_certificates,
        generate_certificate_pdfs,
        send_certificates_for_signoff,
        copy_certificate_details_to_another_user,
    ]
    readonly_fields = [
        "preview_pdf",
        "signed_pdf",
        "is_signed_off",
        "signed_off_by",
        "signed_off_date",
        "date_sent_for_signoff",
        "sent_for_signoff",
    ]
    fieldsets = (
        ("Certificate Details", {"fields": ("user", "details", "autogenerated")}),
        ("Generated PDFs", {"fields": ("preview_pdf", "signed_pdf")}),
        (
            "Sign-off",
            {
                "fields": (
                    "sent_for_signoff",
                    "date_sent_for_signoff",
                    "is_signed_off",
                    "signed_off_by",
                    "signed_off_date",
                )
            },
        ),
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        db = kwargs.get("using")

        if db_field.name == "signed_off_by":
            kwargs["queryset"] = Group.objects.get(name="Contributions Sign Off").user_set.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = self.readonly_fields
        if obj and obj.is_signed_off:  # Don't allow it to be edited afterwards
            readonly_fields.extend(["details", "autogenerated", "preview_pdf", "signed_pdf"])
        return readonly_fields

    def view_certificate(self, obj: ContributionCertificate):
        if obj.is_signed_off:
            return format_html(
                f'<a target="_blank" '
                f'href="{reverse("users:certificate_pdf_signed", kwargs={"id": obj.id})}">'
                f"View signed certificate {obj.id}</a>"
            )
        else:
            return format_html(
                f'<a target="_blank" '
                f'href="{reverse("users:certificate_pdf", kwargs={"id": obj.id})}">'
                f"View certificate {obj.id}</a>"
            )
