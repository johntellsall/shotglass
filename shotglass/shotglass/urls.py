# shotglass.urls

from django.conf.urls import include, re_path
# from django.contrib import admin

urlpatterns = [
    re_path(r"^app/", include("app.urls")),
    #    url(r'^admin/', include(admin.site.urls)),
]
