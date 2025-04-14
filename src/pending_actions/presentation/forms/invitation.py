# -*- coding: utf-8 -*-

from django import forms


class TenantUserInvitationForm(forms.Form):
    first_name = forms.CharField(required=False)
    paternal_surname = forms.CharField(required=False)
    maternal_surname = forms.CharField(required=False)
    password = forms.CharField(required=True)

