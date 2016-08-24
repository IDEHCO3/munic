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
            #"description": "rdfs:comment",
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

class HydraPropertySerializer:


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
            "property": name,
            "required": required,
            "readable": readable,
            "writeable": writeable,
        }
        self._data.append(property)

    @property
    def data(self):
        self.createProperties()
        return self._data


class HydraMethodSerializer:

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
            "@type": "CreateResourceOperation",
            "title": "Create",
            "method": "POST",
            "expects": expects,
            "returns": returns,
            "possibleStatus": possible_status
        }
        self._data.append(method)

    def addDefaultUpdateOperation(self, id="", expects="", returns="", possible_status=[]):
        method = {
            #"@id": id,
            "@type": "ReplaceResourceOperation",
            "title": "Update",
            "method": "PUT",
            "expects": expects,
            "returns": returns,
            "possibleStatus": possible_status
        }
        self._data.append(method)

    def addDefaultDeleteOperation(self, id="", possible_status=[]):
        method = {
            #"@id": id,
            "@type": "DeleteResourceOperation",
            "title": "Delete",
            "method": "DELETE",
            "expects": "",
            "returns": "",
            "possibleStatus": possible_status
        }
        self._data.append(method)

    def addCustomOperation(self, id="", type="", title="Default", httpMethod="GET", expects="", returns="", possible_status=[]):
        method = {
            #"@id": id,
            "@type": type,
            "title": title,
            "method": httpMethod,
            "expects": expects,
            "returns": returns,
            "possibleStatus": possible_status
        }
        self._data.append(method)

    @property
    def data(self):
        self.createMethods()
        return self._data

# remember of case using authentication
class HydraClassSerializer():

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
        self._data["suportedProperty"] = property_serializer.data

        method_serializer = HydraMethodSerializer()
        self.createMethods(method_serializer)
        self._data["suportedOperation"] = method_serializer.data

    def baseStructure(self):
        class_name = self.getTitle()
        if self.class_name is None:
            id = ""
        else:
            id = reverse('context:detail', args=[self.class_name], request=self.request)
        base = {
            "@context": self.getContext(),
            "@id": id,
            "@type": "hydra:Class",
            "title": class_name,
            "description": self.description,
            "suportedProperty": [],
            "suportedOperation": []
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
            "@vocab": reverse('hydra:hydravocab', request=self.request)
        }
        return hydraVocab


class HydraAPISerializer():

    _data = {}

    vocab = ""
    classes_serializers = ()

    def createBase(self):
        id = reverse('documentation:listHydra')

        data = {
            "@context": "",
            "@id": id,
            "@type": "ApiDocumentation",
            "supportedClass": ""
        }

        self._data = data

    def createMetadata(self):
        self.createBase()
        self._data["supportedClass"] = self.getClassesData()
        self._data["@context"] = self.getContext()

    def getContext(self):
        context = {
            #"vocab": "self.vocab",
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
            #"description": "rdfs:comment",
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
            if temp["title"] == class_name:
                aClass = temp
                break
        return aClass

    @property
    def data(self):
        self.createMetadata()
        return self._data