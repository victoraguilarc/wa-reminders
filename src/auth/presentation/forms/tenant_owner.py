# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth import password_validation
from django.utils.translation import gettext_lazy as _

from src.common.database.models import TenantCustomerORM


class TenantOwnerForm(forms.ModelForm):
    """Validates the user creation process."""

    email = forms.EmailField()

    password1 = forms.CharField(
        strip=False,
        widget=forms.PasswordInput,
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput,
        strip=False,
        help_text=_('Put your password again'),
    )

    class Meta:
        model = TenantCustomerORM
        fields = (
            'email',
            'first_name',
            'paternal_surname',
            'maternal_surname',
        )

    def clean_password2(self):
        """Validates two passwords and username."""
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_('Passwords Mismatch'))

        self.instance.username = self.cleaned_data.get('username')
        password_validation.validate_password(self.cleaned_data.get('password2'), self.instance)
        return password2

    def save(self, commit=True):
        """Saves the user data."""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.register()
        return user
