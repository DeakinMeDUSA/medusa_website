from django.urls import path

from medusa_website.users.views import (
    UserList,
    current_user,
    user_detail_view,
    user_redirect_view,
    user_update_view,
)

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<str:username>/", view=user_detail_view, name="detail"),
    path("current_user/", current_user),
    path("users/", UserList.as_view()),
]
