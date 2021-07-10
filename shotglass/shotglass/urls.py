# shotglass.urls

from django.conf.urls import include, re_path

urlpatterns = [
    re_path(r"^app/", include("app.urls")),
]
