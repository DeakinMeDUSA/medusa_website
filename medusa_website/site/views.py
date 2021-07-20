import logging

import requests
from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponseRedirect
from vanilla import TemplateView, FormView

from medusa_website.org_chart.models import SubCommittee
from medusa_website.site.forms import ContactForm

logger = logging.getLogger(__name__)


class AboutView(TemplateView):
    template_name = "site/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # subcommittees =
        # history, c = History.objects.get_or_create(user=self.request.user)
        context["subcommittees"] = {subcomm.title: subcomm for subcomm in SubCommittee.objects.all().order_by("id")}
        # context["session_history_table"] = SessionHistoryTable(history.session_history)
        return context


class ContactView(FormView, TemplateView):
    template_name = "site/contact.html"
    form_class = ContactForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        subject = f"[INTERNAL] Website contact request from '{form.cleaned_data['name']}'"
        message = form.cleaned_data['message']
        sender = form.cleaned_data['email']
        recipients = ["website@medusa.org.au"]
        msg = EmailMultiAlternatives(subject=subject, body=message, from_email="website@medusa.org.au", to=recipients,
                                     bcc=None, cc=[sender], reply_to=[sender])
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
