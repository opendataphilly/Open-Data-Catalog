# Create your views here.
from django.http import HttpResponse
from opendata.models import Resource, DataType, Tag, CoordSystem, Url, UrlImage
from datetime import datetime
from encoder import *

def tags(request):
    return HttpResponse(json_encode(list(Tag.objects.all())))

def by_tag(request, tag_name):
    return HttpResponse(json_encode(list(Resource.objects.filter(tags__tag_name = tag_name))))

def resource(request, resource_id):
    return HttpResponse(json_encode(Resource.objects.filter(id=resource_id)[0], full_resource_encoder))

def resources(request):
    return HttpResponse(json_encode(list(Resource.objects.all()), short_resource_encoder))
