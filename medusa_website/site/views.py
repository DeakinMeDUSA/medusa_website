from vanilla import TemplateView

from medusa_website.org_chart.models import SubCommittee


class AboutView(TemplateView):
    template_name = "site/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # subcommittees =
        # history, c = History.objects.get_or_create(user=self.request.user)
        context["subcommittees"] = {subcomm.title: subcomm for subcomm in SubCommittee.objects.all().order_by("id")}
        # context["session_history_table"] = SessionHistoryTable(history.session_history)
        return context
