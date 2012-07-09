import os.path
from ConfigParser import SafeConfigParser

from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from pycsw import server

@csrf_exempt
def global_dispatch(request):

    app_root = os.path.dirname(__file__)    

    # serialize settings.CSW into SafeConfigParser
    # object for interaction with pycsw
    config = SafeConfigParser()
    for section, options in settings.CSW.iteritems():
        config.add_section(section)
        for k, v in options.iteritems():
            config.set(section, k, v)

    scheme = "http"
    if request.is_secure():
        scheme = "https"


    # update server.url
    server_url = '%s://%s/csw/' %(scheme, request.META['HTTP_HOST'])
    config.set('server', 'url', server_url)

    # request.meta has:
    # QUERY_STRING, REMOTE_ADDR, CONTENT_LENGTH, SERVER_NAME
    # SERVER_PORT
    env = request.META.copy()
    env.update({ 
            'local.app_root': app_root,
            'REQUEST_URI': request.build_absolute_uri(),
            'REQUEST_METHOD': request.method,
            'wsgi.url_scheme': scheme,
            'SCRIPT_NAME': '', ##### IS THIS CORRECT?!?!?!
            'PATH_INFO': request.path_info,
            'wsgi.input': request # this is being a bit sneaky but w/e
            })
            
    csw = server.Csw(config, env)

    content = csw.dispatch_wsgi()

    return HttpResponse(content, content_type=csw.contenttype)
