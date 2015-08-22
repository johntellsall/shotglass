# shotglass.urls

BLAM

from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^app/', include('app.urls')),
    # url(r'^/beer', include('app.urls')),
#     url(r'^admin/', include(admin.site.urls)),
]
