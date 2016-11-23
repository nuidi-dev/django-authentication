#! -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import Account
from django.utils.translation import ugettext as _
from captcha.fields import ReCaptchaField

class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = Account
        fields = ("email", "password")

class PasswordChangeForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = Account
        fields = ("password",)

class UserCreateForm(UserCreationForm):

    captcha = ReCaptchaField()

    class Meta:
        model = Account
        fields = ("email", "username", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if len(password) < 8:
            raise ValidationError(_('Password too short'))
        return password
