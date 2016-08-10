from django.db import models
from django.contrib.gis.geos import GEOSGeometry, Point, LineString, Polygon
from context.models import Class
# Create your models here.

class SupportedProperty(models.Model):
    property = models.CharField(max_length=100, blank=False, null=False)
    required = models.BooleanField(null=False)
    readable = models.BooleanField(null=False)
    writeable = models.BooleanField(null=False)
    hydra_class = models.ForeignKey(Class, blank=False, null=False, related_name='supported_properties')

class SupportedOperation(models.Model):
    identifier = models.CharField(max_length=1000, blank=True, null=True)
    type = models.CharField(max_length=100, blank=True, null=False)
    title = models.CharField(max_length=100, blank=False, null=False)
    method = models.CharField(max_length=100, blank=False, null=False)
    expects = models.ForeignKey(Class, null=True, related_name='operations_expects')
    returns = models.ForeignKey(Class, null=True, related_name='operations_returns')
    possible_status = models.CharField(max_length=100, blank=True, null=True)
    hydra_class = models.ForeignKey(Class, blank=False, null=False, related_name='supported_operations')










