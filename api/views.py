# Create your views here
from django.http import HttpResponse, Http404
from opendata.models import *
from opendata.views import send_email
from suggestions.models import Suggestion
from datetime import datetime
from encoder import *
from rest import login_required
from django.views.decorators.csrf import csrf_exempt

def http_badreq(body = ""):
    res = HttpResponse("Bad Request\n" + body)
    res.status_code = 400
    return res

@login_required
def vote(request, suggestion_id):
    suggestion = Suggestion.objects.get(pk=suggestion_id)
    remote_addr = request.META['REMOTE_ADDR']
    if request.method == 'PUT' and suggestion != None:
        did_vote = suggestion.rating.get_rating_for_user(request.user, remote_addr)
        
        if did_vote == None:
            suggestion.rating.add(score=1, user=request.user, ip_address=remote_addr)

        return HttpResponse(json_encode(suggestion))

    elif request.method == "DELETE" and suggestion != None:
        vote = suggestion.rating.get_ratings().filter(user = request.user)
        if vote:
            vote.delete()
                
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
    objs = Suggestion.objects.filter(pk = suggestion_id)

    if objs and len(objs) == 1:
        return HttpResponse(json_encode(objs[0]))
    else:
        raise Http404

@csrf_exempt
def suggestions(request):
    if (request.method == 'POST'):
        return add_suggestion_view(request)
    elif (request.method == 'GET'):
        return HttpResponse(json_encode(list(Suggestion.objects.all())))
    else:
        raise Http404

def search_suggestions(request):
    if 'qs' in request.GET:
        qs = request.GET['qs'].replace("+"," ")

        return HttpResponse(json_encode(list(Suggestion.objects.filter(text__icontains=qs))))
    else:
        return http_badreq("Missing required parameter qs")

def ideas(request):
    return HttpResponse(json_encode(list(Idea.objects.all()), tiny_resource_encoder))

def idea(request, idea_id):
    obj = Idea.objects.filter(id = idea_id)
    if obj and len(obj) == 1:
        return HttpResponse(json_encode(obj[0]))
    else:
        raise Http404

def tags(request):
    return HttpResponse(json_encode(list(Tag.objects.all())))

def by_tag(request, tag_name):
    return HttpResponse(json_encode(list(Resource.objects.filter(tags__tag_name = tag_name))))

def resource_search(request):
    if 'qs' in request.GET:
        qs = request.GET['qs'].replace("+", " ")
        search_resources = Resource.search(qs) 

        return HttpResponse(json_encode(list(search_resources), short_resource_encoder))
    else:
        return http_badreq("Must specify qs search param")

def resource(request, resource_id):
    rsrc = Resource.objects.filter(id=resource_id, is_published = True)
    if rsrc and len(rsrc) == 1:
        return HttpResponse(json_encode(rsrc[0], full_resource_encoder))
    else:
        raise Http404

def resources(request):
    return HttpResponse(json_encode(list(Resource.objects.filter(is_published = True)), short_resource_encoder))

def safe_key_getter(dic):
    def annon(key, f = lambda x: x):
        if dic.has_key(key):
            return f(dic[key])
        else:
            return None
    return annon

@csrf_exempt
def submit(request):
    if (request.method == 'POST'):
        json_dict = safe_key_getter(json_load(request.raw_post_data))
    
        coord_list = json_dict("coord_system")
        type_list = json_dict("types")
        format_list = json_dict("formats")
        update_frequency_list = json_dict("update_frequency")

        coords, types, formats, updates ="", "", "", ""

        if (coord_list == None):
            return http_badreq("coord_system should be a list")
        if (type_list == None):
            return http_badreq("types should be a list")
        if (format_list == None):
            return http_badreq("formats should be a list")
        if (update_frequency_list == None):
            return http_badreq("update_frequency should be a list")

            
        for c in coord_list:
            coords = coords + " EPSG:" + CoordSystem.objects.get(pk=c).EPSG_code.__str__()
        
        for t in type_list:
            types = types + " " + UrlType.objects.get(pk=t).url_type        
            
        for f in format_list:
            formats = formats + " " + DataType.objects.get(pk=f).data_type

        for u in update_frequency_list:
            if u:
                updates = updates + " " + UpdateFrequency.objects.get(pk=u).update_frequency
                
        data = {
            "submitter": request.user.username,
            "submit_date": datetime.now(),
            "dataset_name": json_dict("dataset_name"),
            "organization": json_dict("organization"),
            "copyright_holder": json_dict("copyright_holder"),
            "contact_email": json_dict("contact_email"),
            "contact_phone": json_dict("contact_phone"),
            "url": json_dict("url"),
            "time_period": json_dict("time_period"),
            "release_date": json_dict("release_date"),
            "area_of_interest": json_dict("area_of_interest"),
            "update_frequency": updates,
            "coord_system": coords,
            "types": types,
            "formats": formats,
            "usage_limitations": json_dict("usage_limitations"),
            "collection_process": json_dict("collection_process"),
            "data_purpose": json_dict("data_purpose"),
            "intended_audience": json_dict("intended_audience"),
            "why": json_dict("why"),
            }
        
        for key in data:
            if (data[key] == None or (hasattr(data[key], "len") and len(data[key]) == 0)):
                return http_badreq(key + " is empty or not defined")

        send_email(request.user, data)

        return HttpResponse("Created")
    else:
        raise Http404
