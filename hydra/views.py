from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .hydra import getHydraVocab
# Create your views here.

class HydraVocab(APIView):

    def get(self, request, *args, **kwargs):
        contextdata = {
            "@context": getHydraVocab()
        }
        response = Response(data=contextdata)
        if request.accepted_media_type != "text/html":
            response.content_type = "application/ld+json"
        return response