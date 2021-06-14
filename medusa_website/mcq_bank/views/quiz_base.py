from django.views.generic import RedirectView, TemplateView


class IndexRedirectView(RedirectView):
    permanent = False
    query_string = False
    pattern_name = "mcq_bank:quiz_index"


class QuizIndexView(TemplateView):
    template_name = "mcq_bank/index.html"
