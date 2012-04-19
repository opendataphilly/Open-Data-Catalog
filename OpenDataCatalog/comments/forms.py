from django import forms
from django.contrib.comments.forms import CommentForm
from comments.models import CommentWithRating
from comments.widgets import StarsRadioFieldRenderer

RATING_CHOICES = (
    (1,1),
    (2,2),
    (3,3),
    (4,4),
    (5,5),
)

class CommentFormWithRating(CommentForm):
    rating = forms.CharField(widget=forms.RadioSelect(renderer=StarsRadioFieldRenderer, attrs={'class':'star'}, choices=RATING_CHOICES))
    
    def get_comment_model(self):
        # Use our custom comment model instead of the built-in one.
        return CommentWithRating

    def get_comment_create_data(self):
        # Use the data of the superclass, and add in the title field
        data = super(CommentFormWithRating, self).get_comment_create_data()
        data['rating'] = self.cleaned_data['rating']
        return data
        
