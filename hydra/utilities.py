from context.models import *
from .models import *
from .serializers import *

def getHydraData(classname, request):
    classobject = Class.objects.get(name=classname)
    serializerHydra = HydraSerializer(classobject, request)
    return serializerHydra.data
