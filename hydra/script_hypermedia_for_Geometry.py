#Objetiva criar uma classe do tipo hydra com suas propiedades e metodos para point, line e polygon
#Este script adianta algumas coisas, mas muita coisa é preciso fazer na mão.

from django.contrib.gis.geos import GEOSGeometry, Point, LineString, Polygon
from hydra.models import Class, SupportedProperty, SupportedOperation, ExpectedParameter
pt = Point(5, 23)
line = LineString((0, 0), (0, 50), (50, 50), (50, 0), (0, 0))
poly = Polygon( ((0.0, 0.0), (0.0, 50.0), (50.0, 50.0), (50.0, 0.0), (0.0, 0.0)))

arr_pt = [ method_attribute for method_attribute in dir(pt) if not method_attribute.startswith('_')]
arr_line = [ method_attribute for method_attribute in dir(line) if not method_attribute.startswith('_')]
arr_polygon = [ method_attribute for method_attribute in dir(poly) if not method_attribute.startswith('_')]


def is_method(object, method_name):
    return hasattr(object, method_name) and callable(getattr(object, method_name))

#Select only properties
arr_pt_attribute = [ method_attribute for method_attribute in arr_pt if not is_method(pt, method_attribute)]
arr_line_attribute = [ method_attribute for method_attribute in arr_line if not is_method(line, method_attribute)]
arr_poly_attribute = [ method_attribute for method_attribute in arr_polygon if not is_method(poly, method_attribute)]
#Select only methods
arr_pt_method = [ method_attribute for method_attribute in arr_pt if not is_method(pt, method_attribute)]
arr_line_method = [ method_attribute for method_attribute in arr_line if not is_method(line, method_attribute)]
arr_poly_method = [ method_attribute for method_attribute in arr_polygon if is_method(poly, method_attribute)]


#Save properties for point class

def save_hydra_class(name_class, arr_property, arr_method):
    #Save properties for point class
    a_class = Class()
    a_class.name = name_class
    a_class.save()
    #Save properties for  class
    for attribute_name in arr_property:
        supported_property = SupportedProperty()
        supported_property.property = attribute_name
        supported_property.hydra_class = a_class
        supported_property.save()

    #Save methods for  class
    for method_name in arr_method:
      supported_property = SupportedProperty()
      supported_property.property = method_name
      supported_property.hydra_class = a_class
      supported_property.save()

#save hydra classes point, line and polygon
save_hydra_class('https://schema.org/geo', arr_pt_attribute, arr_pt_method)
save_hydra_class('https://schema.org/line', arr_line_attribute, arr_line_method)
save_hydra_class('https://schema.org/polygon', arr_poly_attribute, arr_poly_method)
