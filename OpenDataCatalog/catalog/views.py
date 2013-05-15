import os.path

from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from pycsw import server

CONFIGURATION = {
    'server': {
        'home': '.',
        'mimetype': 'application/xml; charset=UTF-8',
        'encoding': 'UTF-8',
        'language': 'en-US',
        'maxrecords': '10',
        # 'pretty_print': 'true',
        'profiles': 'apiso,dif,fgdc,atom,ebrim',
    },
    'repository': {
        'source': 'odc',
        'mappings': os.path.join(os.path.dirname(__file__), 'mappings.py')
    }
}

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
