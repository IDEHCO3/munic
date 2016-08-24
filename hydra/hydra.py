from rest_framework.reverse import reverse

def getHydraVocab():
    context = {
            "hydra": "http://www.w3.org/ns/hydra/core#",
            "ApiDocumentation": "hydra:ApiDocumentation",
            "property": {
                "@id": "hydra:property",
                "@type": "@id"
            },
            "readonly": "hydra:readonly",
            "writeonly": "hydra:writeonly",
            "supportedClass": "hydra:supportedClass",
            "supportedProperty": "hydra:supportedProperty",
            "supportedOperation": "hydra:supportedOperation",
            "method": "hydra:method",
            "expects": {
                "@id": "hydra:expects",
                "@type": "@id"
            },
            "returns": {
                "@id": "hydra:returns",
                "@type": "@id"
            },
            "statusCodes": "hydra:statusCodes",
            "code": "hydra:statusCode",
            "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
            "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
            "label": "rdfs:label",
            "Class": "hydra:Class",
            "description": "rdfs:comment",
            "domain": {
                "@id": "rdfs:domain",
                "@type": "@id"
            },
            "range": {
                "@id": "rdfs:range",
                "@type": "@id"
            },
            "subClassOf": {
                "@id": "rdfs:subClassOf",
                "@type": "@id"
            }
        }
    return context

DEFAULT_HYDRA_PREFIX = "hydra"

class HydraReservedWords():

    def __init__(self, prefix=DEFAULT_HYDRA_PREFIX, connector=":"):
        self.HYDRA_PREFIX = prefix
        self.CONNECTOR = connector

        self.ApiDocumentation = self.HYDRA_PREFIX + self.CONNECTOR + "ApiDocumentation"
        self.supportedClass = self.HYDRA_PREFIX + self.CONNECTOR + "supportedClass"

        self.property = self.HYDRA_PREFIX + self.CONNECTOR + "property"
        self.required = self.HYDRA_PREFIX + self.CONNECTOR + "required"
        self.readable = self.HYDRA_PREFIX + self.CONNECTOR + "readable"
        self.writeable = self.HYDRA_PREFIX + self.CONNECTOR + "writeable"

        self.title = self.HYDRA_PREFIX + self.CONNECTOR + "title"
        self.method = self.HYDRA_PREFIX + self.CONNECTOR + "method"
        self.expects = self.HYDRA_PREFIX + self.CONNECTOR + "expects"
        self.returns = self.HYDRA_PREFIX + self.CONNECTOR + "returns"
        self.possibleStatus = self.HYDRA_PREFIX + self.CONNECTOR + "possibleStatus"

        self.createResourceOperation = self.HYDRA_PREFIX + self.CONNECTOR + "CreateResourceOperation"
        self.replaceResourceOperation = self.HYDRA_PREFIX + self.CONNECTOR + "ReplaceResourceOperation"
        self.deleteResourceOperation = self.HYDRA_PREFIX + self.CONNECTOR + "DeleteResourceOperation"

        self.Class = self.HYDRA_PREFIX + self.CONNECTOR + "Class"
        self.description = self.HYDRA_PREFIX + self.CONNECTOR + "description"

        self.suportedProperty = self.HYDRA_PREFIX + self.CONNECTOR + "suportedProperty"
        self.suportedOperation = self.HYDRA_PREFIX + self.CONNECTOR + "suportedOperation"


class HydraPropertySerializer:

    h = HydraReservedWords()

    def __init__(self):
        self._data = []

    def createProperties(self):
        pass

    def getTypeID(self):
        return "@id"

    def getTypeBoolean(self):
        return "http://schema.org/Boolean"

    def getTypeFloat(self):
        return "http://schema.org/Float"

    def getTypeInteger(self):
        return "http://schema.org/Integer"

    def getTypeString(self):
        return "http://schema.org/Text"

    def getTypeDate(self):
        return "http://schema.org/Date"

    def getTypeDateTime(self):
        return "http://schema.org/DateTime"

    def getTypeTime(self):
        return "http://schema.org/Time"

    def addProperty(self, name="", type="", required=False, readable=False, writeable=False):
        property = {
            #"@type": type,
            self.h.property: name,
            self.h.required: required,
            self.h.readable: readable,
            self.h.writeable: writeable,
        }
        self._data.append(property)

    @property
    def data(self):
        self.createProperties()
        return self._data


class HydraMethodSerializer:

    h = HydraReservedWords()

    def __init__(self):
        self._data = []

    def createMethods(self):
        pass

    def getCreateName(self):
        return "POST"

    def getUpdateName(self):
        return "PUT"

    def getDeleteName(self):
        return "DELETE"

    def getRetrieveName(self):
        return "GET"

    def addDefaultCreateOperation(self, id="", expects="", returns="", possible_status=[]):
        method = {
            #"@id": id,
            "@type": self.h.createResourceOperation,
            self.h.title: "Create",
            self.h.method: "POST",
            self.h.expects: expects,
            self.h.returns: returns,
            self.h.possibleStatus: possible_status
        }
        self._data.append(method)

    def addDefaultUpdateOperation(self, id="", expects="", returns="", possible_status=[]):
        method = {
            #"@id": id,
            "@type": self.h.replaceResourceOperation,
            self.h.title: "Update",
            self.h.method: "PUT",
            self.h.expects: expects,
            self.h.returns: returns,
            self.h.possibleStatus: possible_status
        }
        self._data.append(method)

    def addDefaultDeleteOperation(self, id="", possible_status=[]):
        method = {
            #"@id": id,
            "@type": self.h.deleteResourceOperation,
            self.h.title: "Delete",
            self.h.method: "DELETE",
            self.h.expects: "",
            self.h.returns: "",
            self.h.possibleStatus: possible_status
        }
        self._data.append(method)

    def addCustomOperation(self, id="", type="", title="Default", httpMethod="GET", expects="", returns="", possible_status=[]):
        method = {
            #"@id": id,
            "@type": type,
            self.h.title: title,
            self.h.method: httpMethod,
            self.h.expects: expects,
            self.h.returns: returns,
            self.h.possibleStatus: possible_status
        }
        self._data.append(method)

    @property
    def data(self):
        self.createMethods()
        return self._data

# remember of case using authentication
class HydraClassSerializer():

    h = HydraReservedWords()

    def __init__(self, request=None):
        self.request = request

        self._data = {}

        self.class_name = None
        self.is_collection = False
        self.context = ""
        self.description = ""

    def createProperties(self, property_serializer):
        pass

    def createMethods(self, method_serializer):
        pass

    # use this to create the entire hydra class. Overwrite this method in child class
    def createMetadata(self):
        self.baseStructure()

        property_serializer = HydraPropertySerializer()
        self.createProperties(property_serializer)
        self._data[self.h.suportedProperty] = property_serializer.data

        method_serializer = HydraMethodSerializer()
        self.createMethods(method_serializer)
        self._data[self.h.suportedOperation] = method_serializer.data

    def baseStructure(self):
        class_name = self.getTitle()
        if self.class_name is None:
            id = ""
        else:
            id = reverse('context:detail', args=[self.class_name], request=self.request)
        base = {
            "@context": self.getContext(),
            "@id": id,
            "@type": self.h.Class,
            self.h.title: class_name,
            self.h.description: self.description,
            self.h.suportedProperty: [],
            self.h.suportedOperation: []
        }
        self._data = base

    def getClassTitle(self):
        if self.class_name is not None:
            return self.class_name
        else:
            return ""

    def getTitle(self):
        if self.is_collection:
            return self.getClassTitle()+"Collection"
        else:
            return self.getClassTitle()

    @property
    def data(self):
        self.createMetadata()
        return self._data

    def getContext(self):
        hydraVocab = {
            self.h.HYDRA_PREFIX: reverse('hydra:hydravocab', request=self.request)
        }
        return hydraVocab


class HydraAPISerializer():

    _data = {}
    h = HydraReservedWords()

    vocab = ""
    classes_serializers = ()

    def createBase(self):
        id = reverse('documentation:listHydra')

        data = {
            "@context": "",
            "@id": id,
            "@type": self.h.ApiDocumentation,
            self.h.supportedClass: ""
        }

        self._data = data

    def createMetadata(self):
        self.createBase()
        self._data[self.h.supportedClass] = self.getClassesData()
        self._data["@context"] = self.getContext()

    def getContext(self):
        return getHydraVocab()

    def getClassesData(self):
        classesData = []
        for aClass in self.classes_serializers:
            aInstance = aClass()
            classesData.append(aInstance.data)
        return classesData

    def getClassData(self, class_name):
        aClass = None
        for oneClass in self.classes_serializers:
            temp = oneClass()
            temp = temp.data
            if temp[self.h.title] == class_name:
                aClass = temp
                break
        return aClass

    @property
    def data(self):
        self.createMetadata()
        return self._data