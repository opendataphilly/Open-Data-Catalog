import os.path

from django.conf import settings
from django.http import HttpResponse
from pycsw import server

def global_dispatch(request):
    # config = 'default.cfg'

    # # if env['QUERY_STRING'].lower().find('config') != -1:
    # #     for kvp in env['QUERY_STRING'].split('&'):
    # #         if kvp.lower().find('config') != -1:
    # #             config = kvp.split('=')[1]
    app_root = os.path.dirname(__file__)    


    # if os.path.isabs(config) is False:
    #     config = os.path.join(app_root, config)

    config = settings.CSW_CONFIG
    
    # if 'HTTP_HOST' in env and ':' in env['HTTP_HOST']:
    #     env['HTTP_HOST'] = env['HTTP_HOST'].split(':')[0]

    scheme = "http"
    if request.is_secure():
        scheme = "https"

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

    # gzip = False
    # if (env.has_key('HTTP_ACCEPT_ENCODING') and
    #     env['HTTP_ACCEPT_ENCODING'].find('gzip') != -1):
    #     # set for gzip compressed response 
    #     gzip = True

    # # set compression level
    # if csw.config.has_option('server', 'gzip_compresslevel'):
    #     gzip_compresslevel = \
    #         int(csw.config.get('server', 'gzip_compresslevel'))
    # else:
    #     gzip_compresslevel = 0

    content = csw.dispatch_wsgi()

    return HttpResponse(content, content_type=csw.contenttype)

    # headers = {}

    # if gzip and gzip_compresslevel > 0:
    #     import gzip

    #     buf = StringIO()
    #     gzipfile = gzip.GzipFile(mode='wb', fileobj=buf,
    #                              compresslevel=gzip_compresslevel)
    #     gzipfile.write(contents)
    #     gzipfile.close()
        
    #     contents = buf.getvalue()

    #     headers['Content-Encoding'] = 'gzip'

    # headers['Content-Length'] = str(len(contents))
    # headers['Content-Type'] = csw.contenttype

    # status = '200 OK'
    # start_response(status, headers.items())


