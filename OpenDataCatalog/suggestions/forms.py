from django import forms

from OpenDataCatalog.suggestions.models import *

class SuggestionForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(), max_length=255, label="My Nomination")
    
