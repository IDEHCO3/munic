from django.shortcuts import render
from rest_framework import generics
from munic_2015.models import *
from munic_2015.serializers import *
from context.views import *
# Create your views here.

class EsferaMunicipalList(CreatorContext):

    queryset = EsferaMunicipal.objects.all()
    serializer_class = EsferaMunicipalSerializer