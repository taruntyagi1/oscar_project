from oscar.apps.customer import forms as base_forms
from oscar.core.loading import get_class, get_model, get_profile_class
from oscar.apps.customer.utils import get_password_reset_url, normalise_email
from oscar.core.compat import (
    existing_user_fields, get_user_model)

from django import forms
from django.utils.http import is_safe_url
from django.utils.translation import gettext_lazy as _
from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError





class CustomAuthenticationForm(base_forms.EmailAuthenticationForm):
    """
    customized authentication form
    """

    email = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'email', 'class': 'form-control'}),
        
        max_length=200
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}),
        required=False
    )

    

    redirect_url = forms.CharField(
        widget=forms.HiddenInput, required=False)

    def __init__(self, host, *args, **kwargs):
        self.host = host
        super().__init__(host, *args, **kwargs)

    def clean_redirect_url(self):
        url = self.cleaned_data['redirect_url'].strip()
        if url and is_safe_url(url, self.host):
            return url

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        print(self.cleaned_data)

        
        if password:
            self.user_cache = authenticate(self.request, email=email, password=password)
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)
       


        return self.cleaned_data