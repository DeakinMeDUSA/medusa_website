import requests
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponseRedirect
from vanilla import TemplateView, FormView

from medusa_website.frontend.forms import ContactForm
from medusa_website.frontend.models import Sponsor, Supporter, OfficialDocumentation, Publication, group_docs_by_year, \
    ElectiveReport, ConferenceReport, PublicationType
from medusa_website.org_chart.models import SubCommittee
from medusa_website.utils.general import get_pretty_logger

logger = get_pretty_logger(__name__)


class AboutView(TemplateView):
    template_name = "frontend/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # subcommittees =
        # history, c = History.objects.get_or_create(user=self.request.user)
        context["subcommittees"] = {subcomm.title: subcomm for subcomm in SubCommittee.objects.all().order_by("id")}
        context["sponsors"] = {sponsor.name: sponsor for sponsor in Sponsor.objects.all().order_by("id")}
        context["supporters"] = {supporter.name: supporter for supporter in Supporter.objects.all().order_by("id")}
        # Ensure Rules of Association are always first
        context["rules_of_association"] = OfficialDocumentation.objects.get(name="MeDUSA Rules of Association")
        offical_docs = OfficialDocumentation.objects.all().exclude(name="MeDUSA Rules of Association").order_by(
            "-publish_year")
        context["official_documentation"] = {document.name: document for document in offical_docs}

        # context["session_history_table"] = SessionHistoryTable(history.session_history)
        return context


class ContactView(FormView, TemplateView):
    template_name = "frontend/contact.html"
    form_class = ContactForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        name = form.cleaned_data['name']
        sender = form.cleaned_data['email']
        subject = f"[INTERNAL] Website contact request from '{name}' - {sender}"
        message = f"Message from {name} <{sender}>\n{'-' * 30}\n{form.cleaned_data['message']}"
        recipients = ["contact@medusa.org.au"]
        msg = EmailMultiAlternatives(subject=subject, body=message, from_email="website@medusa.org.au", to=recipients,
                                     bcc=None, reply_to=[sender])
        msg.send()

        messages.success(self.request, 'Form submitted successfully, we will get in touch shortly!')

        return HttpResponseRedirect(self.request.path_info)

    def post(self, request, *args, **kwargs):
        form = self.get_form(data=request.POST, files=request.FILES)
        if form.is_valid():

            # Google ReCAPTCHA
            recaptcha_response = request.POST.get('g-recaptcha-response')
            data = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            result = r.json()
            logger.info(f"ReCAPTCHA result: {result}")
            if result['success']:
                return self.form_valid(form)
            else:
                messages.error(request, 'Invalid reCAPTCHA. Please try again.')
                return self.form_invalid(form)
        return self.form_invalid(form)


class PublicationsView(TemplateView):
    template_name = "frontend/publications.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["publication_types"] = PublicationType.objects.all()
        context["publications_grouped"] = []
        for publication_type in PublicationType.objects.all():
            context["publications_grouped"].append(
                (publication_type, [pub for pub in Publication.objects.filter(type=publication_type).order_by("-pub_date")])
            )
        return context


class ResourcesView(LoginRequiredMixin, TemplateView):
    template_name = "frontend/resources.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class TCSSView(LoginRequiredMixin, TemplateView):
    template_name = "frontend/tcss.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tcss_policy"] = OfficialDocumentation.objects.get(name="TCSS Policy")

        context["elective_reports_by_year"] = group_docs_by_year(ElectiveReport, "elective_year")
        context["conference_reports_by_year"] = group_docs_by_year(ConferenceReport, "conference_year")

        return context
