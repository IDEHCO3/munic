from .hydra import *
from context.models import Class
from .models import *

class HydraSerializer(HydraClassSerializer):

    def __init__(self, classobject, request):
        super(HydraSerializer, self).__init__()
        self.request = request
        self.classobject = classobject

    def getSpatialOperations(self):
        if self.classobject.spatial == "geometry":
            geometry = Class.objects.get(name="geometry")
            return geometry.supported_operations.all()
        return []

    def createProperties(self, property_serializer):
        for property in self.classobject.supported_properties.all():
            property_serializer.addProperty(name=property.property, required=property.required, readable=property.readable, writeable=property.writeable)

    def createMethods(self, method_serializer):
        for method in self.classobject.supported_operations.all():
            method_serializer.addCustomOperation(type=method.type, title=method.title, httpMethod=method.method, expects=self.getURLClass(method.expects), returns=self.getURLClass(method.returns))

        for method in self.getSpatialOperations():
            method_serializer.addCustomOperation(type=method.type, title=method.title, httpMethod=method.method, expects=self.getURLClass(method.expects), returns=self.getURLClass(method.returns))

    def getURLClass(self, obj):
        if obj is not None:
            return reverse('context:detail', args=[obj.name], request=self.request)
        return ""