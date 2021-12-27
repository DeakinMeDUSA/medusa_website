from django.urls import path, re_path

from .views import (
    OSCEHistoryView,
    OSCEIndexRedirectView,
    OSCEIndexView,
    OSCERunView,
    OSCEStationCreateView,
    OSCEStationDetailView,
    OSCEStationListEditView,
    OSCEStationListView,
    OSCEStationMarkFlaggedView,
    OSCEStationMarkReviewedView,
    OSCEStationUpdateView,
)

app_name = "osce_bank"

urlpatterns = [
    path("history/", view=OSCEHistoryView.as_view(), name="history"),
    # path("session/create/", view=OSCESessionCreateView.as_view(), name="osce_session_create"),
    # path("session/", view=OSCERunView.as_view(), name="run_session"),
    path("session/check", view=OSCEIndexRedirectView.as_view(), name="check_session"),  # TODO implement
    # path(
    #     "history/<int:id>",
    #     view=OSCESessionDetailView.as_view(),
    #     name="quiz_session_detail",
    # ),
    path("station/run/<int:id>", view=OSCERunView.as_view(), name="osce_station_run"),
    path("station/detail/<int:id>", view=OSCEStationDetailView.as_view(), name="osce_station_detail"),
    path("station/update/<int:id>", view=OSCEStationUpdateView.as_view(), name="osce_station_update"),
    path("station/create", view=OSCEStationCreateView.as_view(), name="osce_station_create"),
    path("station/list", view=OSCEStationListView.as_view(), name="osce_station_list"),
    path("station/list-edit", view=OSCEStationListEditView.as_view(), name="osce_station_list_edit"),
    path("station/mark-flagged/<int:id>", view=OSCEStationMarkFlaggedView.as_view(), name="osce_station_mark_flagged"),
    path("station/mark-review/<int:id>", view=OSCEStationMarkReviewedView.as_view(), name="osce_station_mark_reviewed"),
    # redirect all others to index
    re_path("^$", view=OSCEIndexView.as_view(), name="osce_index"),
    re_path("^.*$", view=OSCEIndexRedirectView.as_view(), name="index_redirect"),  # redirect all others to index
]
