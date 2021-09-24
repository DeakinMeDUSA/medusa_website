import logging
from typing import Optional

from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.http import HttpResponseRedirect
from django_filters import FilterSet, ModelChoiceFilter, ModelMultipleChoiceFilter
from django_filters.views import FilterView
from vanilla import ListView, UpdateView, CreateView, DetailView

from medusa_website.osce_bank.forms import OSCEStationDetailForm, OSCEStationCreateUpdateForm
from medusa_website.osce_bank.models import OSCEStation, StationType, Speciality
from medusa_website.users.models import User

logger = logging.getLogger(__name__)


class OSCEStationDetailView(LoginRequiredMixin, DetailView):
    model = OSCEStation
    template_name = "osce_bank/osce_station_detail.html"
    form_class = OSCEStationDetailForm
    context_object_name = "osce_station"
    lookup_field = "id"
    queryset = OSCEStation.objects.all()

    #
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form(instance=self.object)

        author_change_permission = request.user.is_staff or request.user.is_superuser
        if author_change_permission is False:
            form.fields["author"].disabled = True

        context = self.get_context_data(form=form)
        return self.render_to_response(context)

    def get_object(self, queryset=None) -> OSCEStation:
        """
        Returns the object the view is displaying.
        """
        osce_station = OSCEStation.objects.get(id=self.kwargs["id"])
        self.osce_station = osce_station
        return osce_station

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context["osce_station"].refresh_from_db()
        osce_station: OSCEStation = context["osce_station"]
        context["editable"] = osce_station.editable(self.request.user)
        return context


class OSCEStationUpdateView(LoginRequiredMixin, UpdateView):
    model = OSCEStation
    template_name = "osce_bank/osce_station_update.html"
    form_class = OSCEStationCreateUpdateForm
    context_object_name = "osce_station"
    lookup_field = "id"
    queryset = OSCEStation.objects.all()

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form(instance=self.object)

        author_change_permission = request.user.is_staff or request.user.is_superuser
        if author_change_permission is False:
            form.fields["author"].disabled = True

        context = self.get_context_data(form=form)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        osce_station_old = self.get_object()
        self.object = osce_station_old
        orig_author = osce_station_old.author
        form = self.get_form(
            data=request.POST,
            files=request.FILES,
            instance=osce_station_old,
        )
        if form.is_valid():
            updated_osce_station: OSCEStation = form.save(commit=False)
            updated_osce_station.author = form.instance.author or orig_author
            updated_osce_station.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.form_invalid(form)

    def get_template_names(self):
        osce_station: OSCEStation = self.get_object()
        if osce_station.editable(self.request.user):
            self.template_name = "osce_bank/osce_station_update.html"
        else:
            self.template_name = "osce_bank/osce_station_detail.html"
        return super(OSCEStationUpdateView, self).get_template_names()

    def get_form_class(self):
        if self.request.method == "GET" and self.get_object().editable(self.request.user) is False:
            return OSCEStationDetailForm
        else:
            return OSCEStationCreateUpdateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        osce_station: OSCEStation = self.get_object()
        context["editable"] = osce_station.editable(self.request.user)
        context["osce_station"] = osce_station
        return context

    def fix_missing_author(self, form):
        if isinstance(form.cleaned_data["author"], User) is False:
            print(f"Author came in as {form.cleaned_data['author']}, resetting to prior value: {form.instance.user}")
            form.cleaned_data["author"] = form.instance.author
        return super().form_valid(form)


class OSCEStationCreateView(LoginRequiredMixin, CreateView):
    model = OSCEStation

    # fields = ["text", "category", "image", "explanation", "randomise_answer_order"]
    template_name = "osce_bank/osce_station_create.html"
    form_class = OSCEStationCreateUpdateForm
    lookup_field = "id"

    def post(self, request, *args, **kwargs):
        form = self.get_form(
            data=request.POST,
            files=request.FILES,
        )
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["osce_station"] = kwargs["form"].instance

        return context

    def form_valid(self, form):
        new_osce_station: OSCEStation = form.save(commit=True)
        new_osce_station.author = self.request.user
        new_osce_station.save()
        return HttpResponseRedirect(new_osce_station.get_absolute_url())


class OSCEStationListFilter(FilterSet):
    class Meta:
        model = OSCEStation
        fields = ["author", "level", "types", "specialities", "is_flagged", "is_reviewed"]
        # form = OSCEStationListForm

    author = ModelChoiceFilter(queryset=User.objects.filter(
        id__in=OSCEStation.objects.select_related("author").order_by("author").distinct("author").values_list("author",
                                                                                                              flat=True)))
    types = ModelMultipleChoiceFilter(queryset=StationType.objects.all(), widget=forms.CheckboxSelectMultiple)
    specialities = ModelMultipleChoiceFilter(queryset=Speciality.objects.all(), widget=forms.CheckboxSelectMultiple)

    # TODO Look into using Boolean filter and its associated widget


class OSCEStationListView(LoginRequiredMixin, ListView, FilterView):
    model = OSCEStation
    template_name = "osce_bank/osce_station_list.html"
    # form_class = OSCEStationCreateUpdateForm
    context_object_name = "osce_station"
    lookup_field = "id"

    # table_class = OSCEStationListTable

    def get_context_data(self, **kwargs):
        context = super(OSCEStationListView, self).get_context_data(**kwargs)
        all_osce_stations = OSCEStation.objects.all()
        context["filter"] = OSCEStationListFilter(self.request.GET, queryset=all_osce_stations)
        filtered_osce_stations: QuerySet[OSCEStation] = context["filter"].qs
        completed_filter = self.parse_completed_filter(self.request.GET.get("completed"))
        annotated_osce_stations = OSCEStation.station_list_for_user(user=self.request.user,
                                                                    stations=filtered_osce_stations)
        if completed_filter is not None:
            annotated_osce_stations = [s for s in annotated_osce_stations if s.completed == completed_filter]

        # context["osce_station_list_table"] = OSCEStationListTable(annotated_osce_stations, request=self.request)
        context["displayed_osce_stations"] = annotated_osce_stations
        # context["quiz_create_form"] = OSCESessionCreateFromOSCEStationsForm(
        #     user=self.request.user, osce_stations=annotated_osce_stations
        # )
        return context

    @staticmethod
    def parse_completed_filter(option: Optional[str]) -> Optional[bool]:
        mapping = {"-1": None, "1": True, "0": False, None: None, "": None}
        return mapping[option]
