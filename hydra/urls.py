
from django.conf.urls import patterns, url, include
from .views import HydraVocab

urlpatterns = patterns('',
    url(r'^vocab/$', HydraVocab.as_view(), name="hydravocab"),
)

def getHydraVocabURLPatterns(inicialURL):
    return url(inicialURL, include('hydra.urls', namespace='hydra'))