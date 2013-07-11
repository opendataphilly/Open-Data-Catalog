from django import forms

from registration.backends.default.views import RegistrationView
# from registration.backends.default import DefaultBackend
from registration.forms import RegistrationForm,RegistrationFormUniqueEmail
from django.db import transaction
from OpenDataCatalog.opendata.models import ODPUserProfile
from widgets import *
from fields import *


class ODPRegistrationForm(RegistrationForm):

    first_name = forms.RegexField(regex=r'^\w', max_length=30, widget=forms.TextInput(), label="First Name",
                                error_messages={ 'invalid': "This value must contain only letters" }, required=True)
    last_name = forms.RegexField(regex=r'^\w', max_length=30, widget=forms.TextInput(), label="Last Name",
                                error_messages={ 'invalid': "This value must contain only letters" }, required=True)
    organization = forms.CharField(max_length=255, required=False, initial="optional")
    can_notify = forms.BooleanField(required=False, label="", help_text="Would you like to receive e-mail updates regarding OpenDataPhilly?")
    recaptcha = ReCaptchaField(label="")


class CatalogRegistrationView(RegistrationView):
    """Custom registration view that uses our custom form."""

    form_class = ODPRegistrationForm

    @transaction.commit_on_success
    def register(self, request, **cleaned_data):
        new_user = super(CatalogRegistrationView, self).register(request, **cleaned_data)
        new_user.first_name = cleaned_data['first_name']
        new_user.last_name = cleaned_data['last_name']
        new_user.save()
        profile = ODPUserProfile()
        profile.user = new_user
        profile.organization = cleaned_data['organization']
        profile.can_notify = cleaned_data['can_notify']
        profile.save()
        return new_user
