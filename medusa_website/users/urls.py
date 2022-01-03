from django.urls import path

from medusa_website.users.views import (
    contribution_certificate_pdf_view,
    contribution_certificate_view,
    member_check_view,
    user_detail_view,
    user_redirect_view,
    user_update_view,
)

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("certificate/", view=contribution_certificate_view, name="certificate"),
    path("certificate_pdf/", view=contribution_certificate_pdf_view, name="certificate_pdf"),
    path("member_check/", view=member_check_view, name="member_check"),
    path("member_check/<str:member_id>", view=member_check_view, name="member_check"),
    path("<str:email>/", view=user_detail_view, name="detail"),
]
