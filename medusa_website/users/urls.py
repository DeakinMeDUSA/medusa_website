from django.urls import path

from medusa_website.users.views import (
    contribution_certificate_create_view,
    contribution_certificate_delete_view,
    contribution_certificate_detail_view,
    contribution_certificate_pdf_view,
    member_check_view,
    user_detail_view,
    user_redirect_view,
    user_update_view,
)

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("certificate/create", view=contribution_certificate_create_view, name="certificate_create"),
    path("certificate/detail/<int:id>", view=contribution_certificate_detail_view, name="certificate_detail"),
    path("certificate/pdf/<int:id>", view=contribution_certificate_pdf_view, name="certificate_pdf"),
    path("certificate/delete/<int:id>", view=contribution_certificate_delete_view, name="certificate_delete"),
    path("member_check/", view=member_check_view, name="member_check"),
    path("member_check/<str:member_id>", view=member_check_view, name="member_check"),
    path("<str:email>/", view=user_detail_view, name="detail"),
]
