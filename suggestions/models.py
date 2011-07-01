import os
from operator import attrgetter
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

from sorl.thumbnail.fields import ImageWithThumbnailsField
from djangoratings.fields import RatingField


class Suggestion(models.Model):
    text = models.CharField(max_length=255)
    suggested_by = models.ForeignKey(User, related_name="suggested_by")
    suggested_date = models.DateTimeField(auto_now_add=True)
    last_modified_date = models.DateTimeField(auto_now=True)
    completed = models.BooleanField(default=False)
    
    rating = RatingField(range=1, allow_delete=True, can_change_vote=True)

    def __unicode__(self):
        return '%s' % self.text

