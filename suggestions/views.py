from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from models import *
from forms import *

def list_all(request):
    suggestions = Suggestion.objects.order_by("-rating_score")
    if 'nqs' in request.GET:
        qs = request.GET['nqs'].replace("+", " ")
        suggestions = suggestions.filter(text__icontains=qs)
    if 'filter' in request.GET:
        try:
            user = User.objects.get(username=request.user)
            for s in suggestions:
                voted = s.rating.get_rating_for_user(user=user, ip_address=request.META['REMOTE_ADDR'])
                print s.id, voted
                if not voted:
                    suggestions = suggestions.exclude(pk=s.id)
        except:
            pass    

    form = SuggestionForm()
    return render_to_response('suggestions/list.html', {'suggestions': suggestions, 'form': form}, context_instance=RequestContext(request))

@login_required
def add_suggestion(request):
    if request.method == 'POST':
        form = SuggestionForm(request.POST)
        if form.is_valid():

            sug = Suggestion()
            sug.suggested_by = request.user
            sug.text = request.POST.get('text')
            
            sug.save()            
            sug.rating.add(score=1, user=request.user, ip_address=request.META['REMOTE_ADDR'])
            
            return HttpResponseRedirect('../?sort=suggested_date&dir=desc&filter=mine')
    else: 
        form = SuggestionForm()

    suggestions = Suggestion.objects.order_by("rating_score")
    return render_to_response('suggestions/list.html', {'suggestions': suggestions, 'form': form}, context_instance=RequestContext(request))

@login_required
def add_vote(request, suggestion_id):
    suggestion = Suggestion.objects.get(pk=suggestion_id)
    did_vote = suggestion.rating.get_rating_for_user(request.user, request.META['REMOTE_ADDR'])
    if did_vote == None:
        suggestion.rating.add(score=1, user=request.user, ip_address=request.META['REMOTE_ADDR'])
    return HttpResponseRedirect('../../')

@login_required
def remove_vote(request, suggestion_id):    
    suggestion = Suggestion.objects.get(pk=suggestion_id)
    suggestion.rating.delete(request.user, request.META['REMOTE_ADDR'])
    return HttpResponseRedirect('../../')
