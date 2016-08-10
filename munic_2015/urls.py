
from django.conf.urls import include, patterns, url
from munic_2015.views import *

urlpatterns = patterns('',
    url(r'^esfera-municipal/', EsferaMunicipalList.as_view(), name="list"),
)