from django import forms

from registration.backends.default import DefaultBackend
from registration.forms import RegistrationForm,RegistrationFormUniqueEmail
from django.db import transaction
from opendata.models import ODPUserProfile

class ODPRegistrationForm(RegistrationForm):
      
    first_name = forms.RegexField(regex=r'^\w', max_length=30, widget=forms.TextInput(), label="First Name",
                                error_messages={ 'invalid': "This value must contain only letters" }, required=True)
    last_name = forms.RegexField(regex=r'^\w', max_length=30, widget=forms.TextInput(), label="Last Name",
                                error_messages={ 'invalid': "This value must contain only letters" }, required=True)
    organization = forms.CharField(max_length=255, required=False, initial="optional")
    can_notify = forms.BooleanField(required=False, label="", help_text="Would you like to receive e-mail updates regarding OpenDataPhilly?")
  
class ODPBackend(DefaultBackend):

    def get_form_class(self, request):
        return ODPRegistrationForm
    
    @transaction.commit_on_success
    def register(self, request, **kwargs):
        new_user = super(ODPBackend,self).register(request, **kwargs)
        new_user.first_name = kwargs['first_name']
        new_user.last_name = kwargs['last_name']
        new_user.save()
        profile = ODPUserProfile()
        profile.user = new_user
        profile.organization = kwargs['organization']
        profile.can_notify = kwargs['can_notify']
        profile.save()
        return new_user

