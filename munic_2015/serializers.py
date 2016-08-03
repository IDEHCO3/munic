from rest_framework import serializers
from .models import *

class EsferaMunicipalSerializer(serializers.ModelSerializer):

    class Meta:
        model = EsferaMunicipal
        fields = ['id_esfera_municipal', 'codigo_municipio', 'url_nome_municipio', 'geocodigo', 'url_geometry']