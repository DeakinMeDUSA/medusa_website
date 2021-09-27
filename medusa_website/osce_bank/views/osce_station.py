import logging

import django_tables2 as tables
from django import forms
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.html import format_html
from django_filters import FilterSet, ModelChoiceFilter, ModelMultipleChoiceFilter, BooleanFilter
from django_filters.views import FilterView
from vanilla import ListView, UpdateView, CreateView, DetailView, FormView

from medusa_website.mcq_bank.utils import CustomBooleanWidget
from medusa_website.osce_bank.forms import OSCEStationDetailForm, OSCEStationUpdateForm, OSCEStationCreateForm, \
    OSCEStationMarkFlaggedForm
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
        if author_change_permission is False and form.fields.get("author") is not None:
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
    form_class = OSCEStationUpdateForm
    context_object_name = "osce_station"
    lookup_field = "id"
    queryset = OSCEStation.objects.all()

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form(instance=self.object)

        author_change_permission = request.user.is_staff or request.user.is_superuser
        if author_change_permission is False and form.fields.get("author") is not None:
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
            return OSCEStationUpdateForm

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
    form_class = OSCEStationCreateForm
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
    completed = BooleanFilter(field_name="completed", label="Is completed", method="filter_completed",
                              widget=CustomBooleanWidget)
    is_reviewed = BooleanFilter(field_name="is_reviewed", label="Is reviewed", widget=CustomBooleanWidget)
    is_flagged = BooleanFilter(field_name="is_flagged", label="Is flagged", widget=CustomBooleanWidget)


    # def __init__(self, *args, **kwargs):
    #     super(OSCEStationListFilter, self).__init__()
    #     if kwargs.get("request")

    def filter_completed(self, queryset, name, value):
        if self.request:
            user = self.request.user
            if value is True:
                queryset = queryset.filter(id__in=user.osce_history.completed_stations.all())
            elif value is False:
                queryset = queryset.exclude(id__in=user.osce_history.completed_stations.all())
            else:  # None
                queryset = queryset
        return queryset


class OSCEStationListTable(tables.Table):
    class Meta:
        attrs = {
            "class": "table tablesorter-metro-dark",  # Sorting is handled by js to avoid refresh
            "id": "osce-station-list-table",
        }
        model = OSCEStation
        exclude = (
            "stem", "patient_script", "marking_guide", "supporting_notes", "flagged_by", "reviewed_by", "stem_image",
            "marking_guide_image", "supporting_notes_image")
        sequence = (
            "id", "title", "level", "types", "specialities", "author", "is_flagged", "is_reviewed")

    id = tables.Column(linkify=False, accessor="id", orderable=False)
    title = tables.Column(linkify=True, orderable=False)
    level = tables.Column(linkify=True, orderable=False)
    types = tables.Column(linkify=True, orderable=False)
    specialities = tables.Column(linkify=True, orderable=False)
    author = tables.Column(linkify=True, orderable=False)
    is_flagged = tables.Column(linkify=True, orderable=False)
    is_reviewed = tables.Column(linkify=True, orderable=False)

    filterset_class = OSCEStationListFilter

    # def __init__(self, *args, **kwargs):
    #     self.user: User = kwargs.pop("user")
    #     super().__init__(*args, **kwargs)

    def render_types(self, value, record: OSCEStation):
        station_types = record.types.all().values_list("station_type", flat=True)

        return ", ".join(station_types)

    def render_specialities(self, value, record: OSCEStation):
        specialities = record.specialities.all().values_list("speciality", flat=True)

        return ", ".join(specialities)

    def render_id(self, value, record: OSCEStation):
        return format_html(
            f'<a href="{reverse("osce_bank:osce_station_detail", kwargs={"id": value})}">View/edit station {value}</a>'
        )


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
        context["filter"] = OSCEStationListFilter(data=self.request.GET, request=self.request,
                                                  queryset=all_osce_stations)
        filtered_osce_stations: QuerySet[OSCEStation] = context["filter"].qs
        annotated_osce_stations = OSCEStation.station_list_for_user(user=self.request.user,
                                                                    stations=filtered_osce_stations)
        context["filtered_osce_stations"] = annotated_osce_stations
        return context


class OSCEStationListEditView(OSCEStationListView):
    model = OSCEStation
    template_name = "osce_bank/osce_station_list_edit.html"
    context_object_name = "osce_station"
    lookup_field = "id"
    table_class = OSCEStationListTable

    def get_context_data(self, **kwargs):
        context = super(OSCEStationListEditView, self).get_context_data(**kwargs)
        context["osce_station_list_table"] = OSCEStationListTable(context["filtered_osce_stations"],
                                                                  request=self.request)
        return context


class OSCEStationMarkReviewedView(LoginRequiredMixin, UpdateView):
    model = OSCEStation
    context_object_name = "osce_station"
    lookup_field = "id"
    fields = ["id"]

    def get_context_data(self, **kwargs):
        context = super(OSCEStationMarkReviewedView, self).get_context_data(**kwargs)
        user = self.request.user
        assert (user.is_staff or user.is_superuser), "User is not staff or superuser!"

        return context

    def post(self, request, *args, **kwargs):
        self.object: OSCEStation = self.get_object()
        user: User = request.user
        self.object.reviewed_by = user
        self.object.is_reviewed = True
        self.object.save()

        messages.add_message(self.request, messages.INFO, f"OSCE Station marked as reviewed by '{user.name}'")

        return HttpResponseRedirect(self.get_success_url())


class OSCEStationMarkFlaggedView(LoginRequiredMixin, UpdateView, FormView):
    model = OSCEStation
    template_name = "osce_bank/osce_station_mark_flagged.html"
    context_object_name = "osce_station"
    lookup_field = "id"
    form_class = OSCEStationMarkFlaggedForm
    fields = ["id"]

    def get_context_data(self, **kwargs):
        context = super(OSCEStationMarkFlaggedView, self).get_context_data(**kwargs)
        user = self.request.user
        assert (user.is_staff or user.is_superuser), "User is not staff or superuser!"
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form(instance=self.object)
        context = self.get_context_data(form=form)
        return self.render_to_response(context)

    def form_valid(self, form):
        # self.object = form.save()
        self.object: OSCEStation = self.get_object()
        user: User = self.request.user
        self.object.flagged_by = user
        self.object.is_flagged = True
        self.object.flagged_message = form.cleaned_data["flagged_message"]
        self.object.save()
        messages.add_message(self.request, messages.INFO, f"OSCE Station marked as flagged by '{user.name}'")
        return HttpResponseRedirect(self.get_success_url())
