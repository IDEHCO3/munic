from context.models import *
from hydra.models import *


def loadEsferaMunicipalContext():
    try:
        esferaMunicipalContextClass = Class.objects.get(name="esfera-municipal")
    except:
        esferaMunicipalContextClass = Class(name="esfera-municipal")
        esferaMunicipalContextClass.save()

    if len(esferaMunicipalContextClass.contexts.all()) == 0:
        contexts = []
        contexts.append(Context(attribute="id_esfera_municipal", means="@id", type="http://schema.org/Integer", classname=esferaMunicipalContextClass))
        contexts.append(Context(attribute="codigo_municipio", means="http://schema.org/Thing", type="http://schema.org/Text", classname=esferaMunicipalContextClass))
        contexts.append(Context(attribute="url_nome_municipio", means="http://schema.org/name", type="@id", classname=esferaMunicipalContextClass))
        contexts.append(Context(attribute="geocodigo", means="http://schema.org/Thing", type="http://schema.org/Text", classname=esferaMunicipalContextClass))
        contexts.append(Context(attribute="url_geometry", means="http://geojson.org/vocab#geometry", type="@id", classname=esferaMunicipalContextClass))
        for obj in contexts:
            obj.save()

    if len(esferaMunicipalContextClass.supported_properties.all()) == 0:
        properties = []
        properties.append(SupportedProperty(property="id_esfera_municipal", required=False, readable=True, writeable=False, hydra_class=esferaMunicipalContextClass))
        properties.append(SupportedProperty(property="codigo_municipio", required=True, readable=True, writeable=True, hydra_class=esferaMunicipalContextClass))
        properties.append(SupportedProperty(property="url_nome_municipio", required=True, readable=True, writeable=True, hydra_class=esferaMunicipalContextClass))
        properties.append(SupportedProperty(property="geocodigo", required=True, readable=True, writeable=True, hydra_class=esferaMunicipalContextClass))
        properties.append(SupportedProperty(property="url_geometry", required=True, readable=True, writeable=True, hydra_class=esferaMunicipalContextClass))
        for obj in properties:
            obj.save()

    if len(esferaMunicipalContextClass.supported_operations.all()) == 0:
        operations = []
        operations.append(SupportedOperation(identifier="", type="Operation", title="list", method="GET", expects=None, returns=esferaMunicipalContextClass, possible_status="", hydra_class=esferaMunicipalContextClass))
        for obj in operations:
            obj.save()


# context_classes = {
#     "esfera-municipal": {
#         "attributes": {
#             "id_esfera_municipal": {
#                 "context": {"means": "@id", "type": "http://schema.org/Integer"},
#                 "hydra": {"required": False, "readable": True, "writeable": False}
#             },
#             "codigo_municipio": {
#                 "context": {"means": "http://schema.org/Thing", "type": "http://schema.org/Text"},
#                 "hydra": {"required": True, "readable": True, "writeable": True}
#             },
#             "url_nome_municipio": {
#                 "context": {"means": "http://schema.org/url", "type": "http://schema.org/Text"},
#                 "hydra": {"required": True, "readable": True, "writeable": True}
#             },
#             "geocodigo": {
#                 "context": {"means": "http://schema.org/Thing", "type": "http://schema.org/Text"},
#                 "hydra": {"required": True, "readable": True, "writeable": True}
#             },
#             "url_geometry": {
#                 "context": {"means": "http://schema.org/url", "type": "http://schema.org/Text"},
#                 "hydra": {"required": True, "readable": True, "writeable": True}
#             }
#         },
#         "operations": [
#             {"identifier": "", "type": "Operation", "title": "list", "method": "GET", "expects": "none", "returns": "esfera-municipal", "possible_status": ""}
#         ]
#     }
# }
#
# def loadContext(contexts):
#     for context in contexts:
#         obj = contexts[context]
#         try:
#             obj_instance = Class.objects.get(name=context)
#         except:
#             spatial = "none"
#             if "spatial" in obj:
#                 spatial = obj['spatial']
#             obj_instance = Class(name=context, spatial=spatial)
#             obj_instance.save()
#
#         for attribute_key in obj['attributes']:
#             attribute = obj['attributes'][attribute_key]
#             context_instance = Context(**attribute['context'])
#             context_instance.attribute = attribute_key
#             context_instance.classname = obj_instance
#             context_instance.save()
#
#             property_instance = SupportedProperty(**attribute['hydra'])
#             property_instance.property = attribute_key
#             property_instance.hydra_class = obj_instance
#             property_instance.save()
#
#         for operation in obj['operations']:
#             operation['returns'] = Class.objects.get(name=operation['returns'])
#             operation['expects'] = Class.objects.get(name=operation['expects'])
#             operations_instance = SupportedOperation(**operation)
#             operations_instance.hydra_class = obj_instance
#             operations_instance.save()
