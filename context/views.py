from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from hydra.serializers import HydraSerializer
from rest_framework import status

from .utilities import *
from .models import *
from .serializers import *
# Create your views here.

class ContextView(APIView):


    def get(self, request, *args, **kwargs):
        classname = kwargs.get('classname')
        try:
            classobject = Class.objects.get(name=classname)
        except:
            return Response(data={})

        contextdata = ContextSerializer(classobject).data
        hydradata = HydraSerializer(classobject, request).data
        if "@context" in hydradata:
            hydradata["@context"].update(contextdata["@context"])
        contextdata.update(hydradata)
        response = Response(data=contextdata)
        if request.accepted_media_type != "text/html":
            response.content_type = "application/ld+json"
        return response

class CreatorContext(generics.ListCreateAPIView):

    def options(self, request, *args, **kwargs):
        classname = getClassnameByURL(request._request.path)
        response = Response(getContextData(classname, request), status=status.HTTP_200_OK, content_type="application/ld+json")
        response = createLinkOfContext(classname, request, response)
        return response

    def get(self, request, *args, **kwargs):
        response = super(CreatorContext, self).get(request, *args, **kwargs)
        classname = getClassnameByURL(request._request.path)
        response = createLinkOfContext(classname, request, response)
        return response

class CreatorContextToRetrieve(generics.RetrieveAPIView):

    def options(self, request, *args, **kwargs):
        classname = getClassnameByURL(request._request.path)
        response = Response(getContextData(classname, request), status=status.HTTP_200_OK, content_type="application/ld+json")
        response = createLinkOfContext(classname, request, response)
        return response

    def get(self, request, *args, **kwargs):
        response = super(CreatorContextToRetrieve, self).get(request, *args, **kwargs)
        classname = getClassnameByURL(request._request.path)
        response = createLinkOfContext(classname, request, response)
        return response