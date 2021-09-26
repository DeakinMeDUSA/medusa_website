# from typing import Optional
#
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.http import JsonResponse
# from django.shortcuts import redirect, render
# from django.template import loader
# from django.views.generic import FormView
# from vanilla import DetailView
#
# from medusa_website.osce_bank.models import OSCEHistory, OSCEStation
# from ..forms import OSCEStationForm
# from ...users.models import User
#
#
from typing import Optional

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from vanilla import DetailView, FormView

from medusa_website.osce_bank.forms import OSCEStationCompleteForm
from medusa_website.osce_bank.models import OSCEStation
from medusa_website.users.models import User


class OSCERunView(DetailView, FormView, LoginRequiredMixin, ):
    template_name = "osce_bank/osce_station_run.html"
    model = OSCEStation
    context_object_name = "osce_station"
    lookup_field = "id"
    form_class = OSCEStationCompleteForm

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user: Optional[User] = None
        self.osce_station: Optional[OSCEStation] = None
        self.object: Optional[OSCEStation] = None

    def get(self, request, *args, **kwargs):
        form = self.get_form()
        self.object = self.get_object()
        context = self.get_context_data(form=form)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(OSCERunView, self).get_context_data(**kwargs)

        return context

    def post(self, request, *args, **kwargs):
        osce_station = OSCEStation.objects.get(id=request.POST.get("osce_station"))
        user: User = request.user
        user.osce_history.completed_stations.add(osce_station)
        user.osce_history.save()

        return HttpResponseRedirect(reverse("osce_bank:osce_index"))
