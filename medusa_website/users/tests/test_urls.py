import pytest
from django.urls import resolve, reverse

from medusa_website.users.models import User

pytestmark = pytest.mark.django_db


def test_detail(user: User):
    assert (
        reverse("users:detail", kwargs={"email": user.email}) == f"/users/{user.email}/"
    )
    assert resolve(f"/users/{user.email}/").view_name == "users:detail"


def test_update():
    assert reverse("users:update") == "/users/~update/"
    assert resolve("/users/~update/").view_name == "users:update"


def test_redirect():
    assert reverse("users:redirect") == "/users/~redirect/"
    assert resolve("/users/~redirect/").view_name == "users:redirect"
