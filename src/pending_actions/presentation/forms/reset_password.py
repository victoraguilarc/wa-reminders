# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import gettext_lazy as _


class UserResetPasswordForm(forms.Form):
    password1 = forms.CharField()
    password2 = forms.CharField()

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_('Passwords Mismatch'))
        return password2
