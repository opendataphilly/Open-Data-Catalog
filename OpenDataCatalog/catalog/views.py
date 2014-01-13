import json
import os.path

from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from OpenDataCatalog.opendata.models import Resource
from pycsw import server

CONFIGURATION = {
    'server': {
        'home': '.',
        'mimetype': 'application/xml; charset=UTF-8',
        'encoding': 'UTF-8',
        'language': 'en-US',
        'maxrecords': '10',
        # 'pretty_print': 'true',
        'profiles': 'apiso,ebrim',
    },
    'repository': {
        'source': 'odc',
        'mappings': os.path.join(os.path.dirname(__file__), 'mappings.py')
    }
}


@csrf_exempt
def data_json(request):
    """Return data.json representation of site catalog"""
    json_data = []
    for resource in Resource.objects.all():
        record = {} 
        record['title'] = resource.name
        record['description'] = resource.description
        record['keyword'] = resource.csw_keywords.split(',')
        record['modified'] = resource.last_updated
        record['publisher'] = resource.organization
        record['contactPoint'] = resource.metadata_contact
        record['mbox'] = resource.contact_email
        record['identifier'] = resource.csw_identifier
        if resource.is_published:
            record['accessLevel'] = 'public'
        else:
            record['accessLevel'] = 'non-public'

        json_data.append(record)

    return HttpResponse(json.dumps(json_data), 'application/json')

@csrf_exempt
def csw(request):
    """CSW WSGI wrapper"""
    # serialize settings.CSW into SafeConfigParser
    # object for interaction with pycsw
    mdict = dict(settings.CSW, **CONFIGURATION)

    # update server.url
    server_url = '%s://%s%s' % \
        (request.META['wsgi.url_scheme'],
         request.META['HTTP_HOST'],
         request.META['PATH_INFO'])

    mdict['server']['url'] = server_url

    env = request.META.copy()

    env.update({ 
            'local.app_root': os.path.dirname(__file__),
            'REQUEST_URI': request.build_absolute_uri(),
            })
            
    csw = server.Csw(mdict, env)

    content = csw.dispatch_wsgi()

    return HttpResponse(content, content_type=csw.contenttype)
