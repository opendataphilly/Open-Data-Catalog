# Create your views here
from django.http import HttpResponse, Http404
from opendata.models import Resource, DataType, Tag, CoordSystem, Url, UrlImage, Idea
from suggestions.models import Suggestion
from datetime import datetime
from encoder import *
from rest import login_required
from django.views.decorators.csrf import csrf_exempt

def http_badreq():
    res = HttpResponse("Bad Request")
    res.status_code = 400
    return res

@login_required
def vote(request, suggestion_id):
    suggestion = Suggestion.objects.get(pk=suggestion_id)
    if request.method == 'PUT' and suggestion != None:
        remote_addr = request.META['REMOTE_ADDR']
        did_vote = suggestion.rating.get_rating_for_user(request.user, remote_addr)
        
        if did_vote == None:
            suggestion.rating.add(score=1, user=request.user, ip_address=remote_addr)

        return HttpResponse(json_encode(suggestion))

    elif request.method == "DELETE" and suggestion != None:
        suggestion.rating.delete(user, request.META['REMOTE_ADDR'])
                
        return HttpResponse(json_encode(suggestion))

    raise Http404

def add_suggestion(user, text, remote_addr):
    sug = Suggestion()
    sug.suggested_by = user
    sug.text = text
            
    sug.save()            
    sug.rating.add(score=1, user=user, ip_address=remote_addr)
            
    return sug

@login_required
def add_suggestion_view(request):
    json_string = request.raw_post_data
    json_dict = json_load(json_string)

    if (json_dict.has_key("text") == False):
        return http_badreq()

    text = json_dict["text"]

    return HttpResponse(json_encode(add_suggestion(request.user, text, request.META['REMOTE_ADDR'])))

def suggestion(request, suggestion_id):
    return HttpResponse(json_encode(Suggestion.objects.filter(id = suggestion_id)[0]))

@csrf_exempt
def suggestions(request):
    if (request.method == 'POST'):
        return add_suggestion_view(request)
    elif (request.method == 'GET'):
        return HttpResponse(json_encode(list(Suggestion.objects.all())))
    else:
        raise Http404

def ideas(request):
    return HttpResponse(json_encode(list(Idea.objects.all()), tiny_resource_encoder))

def idea(request, idea_id):
    return HttpResponse(json_encode(Idea.objects.filter(id = idea_id)[0]))

def tags(request):
    return HttpResponse(json_encode(list(Tag.objects.all())))

def by_tag(request, tag_name):
    return HttpResponse(json_encode(list(Resource.objects.filter(tags__tag_name = tag_name))))

def resource(request, resource_id):
    return HttpResponse(json_encode(Resource.objects.filter(id=resource_id)[0], full_resource_encoder))

def resources(request):
    return HttpResponse(json_encode(list(Resource.objects.all()), short_resource_encoder))
