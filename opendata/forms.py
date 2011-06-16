from django import forms
from models import UpdateFrequency, CoordSystem, UrlType, DataType

class SubmissionForm(forms.Form):
    dataset_name = forms.CharField(max_length=255, label="Data set, API or App name")
    organization = forms.CharField(max_length=255)
    copyright_holder = forms.CharField(max_length=255)
    contact_email = forms.CharField(max_length=255)
    contact_phone = forms.CharField(max_length=255)
    url = forms.CharField(max_length=255, label="Data/API/App url")
    time_period = forms.CharField(required=False, max_length=255, label="Valid time period")
    release_date = forms.DateField(required=False)
    area_of_interest = forms.CharField(max_length=255, label="Geographic area")
    
    update_frequency = forms.ModelChoiceField(required=False, queryset=UpdateFrequency.objects.all())
    coord_system = forms.ModelMultipleChoiceField(required=False, queryset=CoordSystem.objects.all(), label="Coordinate system")
    types = forms.ModelMultipleChoiceField(required=False, queryset=UrlType.objects.all(), label="Data types")
    formats = forms.ModelMultipleChoiceField(required=False, queryset=DataType.objects.all(), label="Data formats")
    
    description = forms.CharField(max_length=1000, widget=forms.Textarea, label="Describe this dataset")
    usage_limitations = forms.CharField(max_length=1000, widget=forms.Textarea, label="Are there usage limitations?")
    collection_process = forms.CharField(max_length=1000, widget=forms.Textarea, label="How was the data collected?")
    data_purpose = forms.CharField(max_length=1000, widget=forms.Textarea, label="Why was the data collected?")
    intended_audience = forms.CharField(max_length=1000, widget=forms.Textarea, label="Who is the intended audience?")
    why = forms.CharField(max_length=1000, widget=forms.Textarea, label="Why should the data be included in this site?")
    certified = forms.BooleanField(required=False, label="", help_text="I am the copyright holder or have permission to release this data")
    terms = forms.BooleanField(label="", help_text="I have read and agree with the site's <a href='/terms/' target='_blank'>terms of use</a>")
    
