from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

import os
import datetime
from datetime import datetime as dt

# Create your models here.

class Contest(models.Model):
    title = models.CharField(max_length=255)    
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    vote_frequency = models.IntegerField()
    rules = models.TextField()
    
    def get_days_left(self):
        today = dt.today()
        left = self.end_date - today 
        if left.days < 0:
            return 0
        return left.days
    
    def get_days_till_start(self):
        till = self.start_date - dt.today()
        return till.days +1

    def has_ended(self):
        return dt.today() >= self.end_date

    def has_started(self):
        return dt.today() >= self.start_date


    def get_next_vote_date(self, user):
        votes = user.vote_set.order_by('-timestamp')
        increment = datetime.timedelta(days=self.vote_frequency)
        last_vote_date = votes[0].timestamp
        next_vote_date = last_vote_date + increment 
        return next_vote_date

    def user_can_vote(self, user):
        votes = user.vote_set.order_by('-timestamp')
        if votes.count > 0:           
            next_date = self.get_next_vote_date(user)
            if dt.today() < next_date and dt.today() < self.end_date:
                return False
        return True

    def __str__(self):
        return self.title

class Entry(models.Model):
    def get_image_path(instance, filename):
        fsplit = filename.split('.')
        extra = 1
        test_path = os.path.join(settings.MEDIA_ROOT, 'contest_images', str(instance.id), fsplit[0] + '_' + str(extra) + '.' + fsplit[1])
        while os.path.exists(test_path):
           extra += 1
           test_path = os.path.join(settings.MEDIA_ROOT, 'contest_images', str(instance.id), fsplit[0] + '_' + str(extra) + '.' +  fsplit[1])
        path = os.path.join('contest_images', str(instance.id), fsplit[0] + '_' + str(extra) + '.' + fsplit[1])
        return path

    title = models.CharField(max_length=255)
    description = models.TextField()
    short_description = models.CharField(max_length=120)
    nominator = models.CharField(max_length=255)
    nominator_link = models.CharField(max_length=255)
    nominator_image = models.ImageField(upload_to=get_image_path, null=True, blank=True, help_text="Save the entries before adding images.")        

    contest = models.ForeignKey(Contest)
    vote_count = models.IntegerField(default=0)


    def __str__(self):
        return self.title

    def get_place(self):
        entries = Entry.objects.filter(contest=self.contest).order_by('-vote_count')
        for i, entry in enumerate(entries):
            if entry == self: return i+1

class Vote(models.Model):
    user = models.ForeignKey(User)
    timestamp = models.DateTimeField(auto_now=True)

    entry = models.ForeignKey(Entry)


from django import forms

class EntryForm(forms.Form):
    org_name = forms.CharField(max_length=255, label="Organization Name")
    org_url = forms.CharField(max_length=255, label="Organization Url")
    contact_person = forms.CharField(max_length=150, label="Contact Person")
    contact_phone = forms.CharField(max_length=15, label="Contact Phone Number")
    contact_email = forms.EmailField(max_length=150, label="Contact Email")
    data_set = forms.CharField(max_length=255, label="Data Set to Nominate")
    data_use = forms.CharField(max_length=1000, widget=forms.Textarea, label="If this data set were available, how would your organization use it?")
    data_mission = forms.CharField(max_length=1000, widget=forms.Textarea, label="How would this data set contribute to your organization's mission")
    

