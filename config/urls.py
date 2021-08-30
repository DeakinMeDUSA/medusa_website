from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from django.views import defaults as default_views

from medusa_website.mcq_bank.views.markdown_uploader import markdown_uploader
from medusa_website.users import utils

urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + [
    path("", include("medusa_website.frontend.urls", namespace="frontend")),
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
    path('tinymce/', include('tinymce.urls')),
    # Catch the rest of the urls
    # re_path(r'^(?P<path>.*)/$', view=TemplateView.as_view(template_name="frontend/index.html"),
    #         name="catchall"),

]

sitemaps = {}  # Don't really need a proper sitemap

urlpatterns += [
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
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
