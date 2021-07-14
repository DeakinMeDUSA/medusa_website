from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views import defaults as default_views
from django.views.generic import TemplateView

from medusa_website.mcq_bank.views.markdown_uploader import markdown_uploader
from medusa_website.pages.views import HomeView, AboutView
from medusa_website.users import utils

urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + [
    path("", HomeView.as_view(), name="home"),
    path("about/", AboutView.as_view, name="about"),
    path(
        "empty_test/",
        TemplateView.as_view(template_name="pages/empty_test.html"),
        name="empty_test",
    ),
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    # User management
    path("users/", include("medusa_website.users.urls", namespace="users")),
    path("accounts/", include("allauth.urls")),
    # Your stuff: custom urls includes go here
    path("mcq_bank/", include("medusa_website.mcq_bank.urls", namespace="mcq_bank")),
    path("ping/", utils.ping),
    path("martor/", include("martor.urls")),
    url(r"^api/uploader/$", markdown_uploader, name="markdown_uploader_page"),
]

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
