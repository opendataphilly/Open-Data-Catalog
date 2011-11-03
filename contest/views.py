from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.template.loader import render_to_string
from django.core.mail import send_mail, mail_managers, EmailMessage
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from contest.models import *
from datetime import datetime

def get_entries(request, contest_id=1):
    contest = Contest.objects.get(pk=contest_id)
    entries = Entry.objects.filter(contest=contest)
    if not request.GET.__contains__('sort'):
        entries = entries.order_by('-vote_count')
    return render_to_response('contest/entries.html', {'contest': contest, 'entries': entries}, context_instance=RequestContext(request))

def get_winners(request, contest_id=1):
    contest = Contest.objects.get(pk=contest_id)
    entries = Entry.objects.filter(contest=contest).order_by('-vote_count')
    return render_to_response('contest/winners.html', {'contest': contest, 'entries': entries}, context_instance=RequestContext(request))

def get_rules(request, contest_id=1):
    contest = Contest.objects.get(pk=contest_id)
    return render_to_response('contest/rules.html', {'contest': contest}, context_instance=RequestContext(request))

def get_entry(request, entry_id):
    entry = Entry.objects.get(pk=entry_id)
    return render_to_response('contest/entry.html', {'contest': entry.contest, 'entry': entry}, context_instance=RequestContext(request))

#@login_required
def add_entry(request, contest_id=1):
    contest = Contest.objects.get(pk=contest_id)
    if request.method == 'POST':
        form = EntryForm(request.POST)
        form.contest = contest_id

        if form.is_valid():

            data = {
                #"submitter": request.user.username,
                "submit_date": datetime.now(),
                "org_name": request.POST.get("org_name"),
                "org_url": request.POST.get("org_url"),
                "contact_person": request.POST.get("contact_person"),
                "contact_phone": request.POST.get("contact_phone"),
                "contact_email": request.POST.get("contact_email"),
                "data_set": request.POST.get("data_set"),
                "data_use": request.POST.get("data_use"),
                "data_mission": request.POST.get("data_mission")
            }

            subject = 'OpenDataPhilly - Contest Submission'
            user_email = request.POST.get("contact_email")
            text_content = render_to_string('contest/submit_email.txt', data)
            text_content_copy = render_to_string('contest/submit_email_copy.txt', data)
            mail_managers(subject, text_content)

            msg = EmailMessage(subject, text_content_copy, to=[user_email])
            msg.send()

            return render_to_response('contest/thanks.html', {'contest': contest}, context_instance=RequestContext(request))

    else: 
        form = EntryForm()

    return render_to_response('contest/submit_entry.html', {'contest': contest, 'form': form}, context_instance=RequestContext(request))

@login_required
def add_vote(request, entry_id):
    entry = Entry.objects.get(pk=entry_id)
    contest = entry.contest
    user = User.objects.get(username=request.user)

    if contest.user_can_vote(user):
        new_vote = Vote(user=user, entry=entry)
        new_vote.save()
        entry.vote_count = entry.vote_set.count()
        entry.save()
        next_vote_date = contest.get_next_vote_date(user)
        if next_vote_date > contest.end_date:
            messages.success(request, '<div style="font-weight:bold;">Your vote has been recorded.</div>Thank you for your vote! You will not be able to vote again before the end of the contest. <br><br>Please encourage others to visit <a href="/">OpenDataPhilly</a> and to join the race toward more open data!')
        else:
            messages.success(request, '<div style="font-weight:bold;">Your vote has been recorded.</div>You may vote once per week, so come back and visit us again on ' + next_vote_date.strftime('%A, %b %d %Y, %I:%M%p') + '. <br><br>Until then, encourage others to visit <a href="/">OpenDataPhilly</a> and to join the race toward more open data!')
    else:
        next_vote_date = contest.get_next_vote_date(user)
        if next_vote_date > contest.end_date:
            messages.error(request, '<div style="font-weight:bold;">You have already voted.</div>You will not be able to vote again before the end of the contest. <br><br>Please encourage others to visit <a href="/">OpenDataPhilly</a> and to join the race toward more open data!')
        else:
            messages.error(request, '<div style="font-weight:bold;">You have already voted.</div>You may vote once per week, so come back and visit us again on ' + next_vote_date.strftime('%A, %b %d %Y, %I:%M%p') + '. <br><br>Until then, encourage others to visit <a href="/">OpenDataPhilly</a> and to join the race toward more open data!')    
    
    return redirect('/contest/?sort=vote_count')
    
