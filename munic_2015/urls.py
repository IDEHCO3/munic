
from django.conf.urls import include, patterns, url
from .views import *

urlpatterns = patterns('',
    url(r'^esfera-municipal/$', EsferaMunicipalList.as_view(), name="list"),
)