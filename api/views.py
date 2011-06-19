# Create your views here
from django.http import HttpResponse, Http404
from opendata.models import Resource, DataType, Tag, CoordSystem, Url, UrlImage, Idea
from suggestions.models import Suggestion
from datetime import datetime
from encoder import *
from rest import login_required

@login_required
def vote(request, suggestion_id):
    if request.method == 'PUT':
        suggestion = Suggestion.objects.get(pk=suggestion_id)
        if (suggestion != None):
            remote_addr = request.META['REMOTE_ADDR']
            did_vote = suggestion.rating.get_rating_for_user(request.user, remote_addr)

            if did_vote == None:
                suggestion.rating.add(score=1, user=request.user, ip_address=remote_addr)

            return HttpResponse(json_encode(suggestion))
                
    else:
        raise Http404

def unvote(reuqest, suggestion_id):
    if request.method == 'PUT':
        suggestion = Suggestion.objects.get(pk=suggestion_id)
        if (suggestion != None):
            suggestion.reating.delete(user, request.META['REMOTE_ADDR'])
        
            return HttpResponse(json_encode(suggestion))

    raise Http404

def suggestion(request, suggestion_id):
    return HttpResponse(json_encode(Suggestion.objects.filter(id = suggestion_id)[0]))

def suggestions(request):
    return HttpResponse(json_encode(list(Suggestion.objects.all())))

@login_required
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
