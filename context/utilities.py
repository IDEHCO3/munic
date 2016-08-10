from rest_framework.reverse import reverse
from context.models import *
from context.serializers import *
from hydra.utilities import getHydraData

def createLinkOfContext(classname, request, response, properties=None):
    if properties is None:
        url = reverse('context:detail', args=[classname], request=request)
    else:
        url = reverse('context:detail-property', args=[classname, ",".join(properties)], request=request)

    response['Link'] = '<'+url+'>; rel=\"http://www.w3.org/ns/json-ld#context\"; type=\"application/ld+json\";'
    return response

def getContextData(classname, request):
    try:
        classobject = Class.objects.get(name=classname)
    except:
        return ""
    serializer = ContextSerializer(classobject)
    contextdata = serializer.data
    hydradata = getHydraData(classname, request)
    if "@context" in hydradata:
        hydradata["@context"].update(contextdata["@context"])
    contextdata.update(hydradata)
    return contextdata

def getClassnameByURL(path):
    if path[-1] != '/':
            path += '/'
    list_path = path.split('/')
    classname = list_path[-2]
    return classname