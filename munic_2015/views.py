from django.shortcuts import render
from rest_framework import generics
from .models import *
from .serializers import *

# Create your views here.

class EsferaMunicipalList(generics.ListAPIView):

    queryset = EsferaMunicipal.objects.all()
    serializer_class = EsferaMunicipalSerializer