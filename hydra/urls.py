
from django.conf.urls import patterns, url
from hydra.views import HydraVocab

urlpatterns = patterns('',
    url(r'^vocab/$', HydraVocab.as_view(), name="hydravocab"),
)