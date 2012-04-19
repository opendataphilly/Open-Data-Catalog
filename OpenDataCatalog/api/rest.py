from django.http import HttpResponse
from django.contrib.auth import authenticate
import re
import base64

def http_unauth():
    res = HttpResponse("Unauthorized")
    res.status_code = 401
    res['WWW-Authenticate'] = 'Basic realm="Secure Area"'
    return res

def match_first(regx, strg):
    m = re.match(regx, strg)
    if (m == None):
        return None
    else:
        return m.group(1)

def decode_auth(strg):
    if (strg == None):
        return None
    else:
        m = re.match(r'([^:]*)\:(.*)', base64.decodestring(strg))
        if (m != None):
            return (m.group(1), m.group(2))
        else:
            return None

def parse_auth_string(authstr):
    auth = decode_auth(match_first('Basic (.*)', authstr))
    if (auth == None):
        return None
    else:
        return authenticate(username = auth[0], password = auth[1])
        
def login_required(view_f):
    def wrapperf(request, *args, **kwargs):
        if (request.META.has_key('HTTP_AUTHORIZATION')):
            auth = request.META['HTTP_AUTHORIZATION']
            user = parse_auth_string(auth)
            if (user != None):
                request.user = user
                return view_f(request, *args, **kwargs)
        return http_unauth()

    return wrapperf

