from django import forms
from django.contrib.auth.admin import UserChangeForm, AdminUserCreationForm
from django.contrib.auth.forms import AuthenticationForm

from .models import *


class ShopUserCreationForm(AdminUserCreationForm):
    class Meta:
        model = ShopUser
        fields = ['phone', 'first_name', 'last_name', 'address', 'is_active', 'is_staff', 'is_superuser', 'date_joined']

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')

        if ShopUser.objects.filter(phone=phone).exists():
            raise forms.ValidationError('Entered phone already exists.')

        if not phone.startswith('09'):
            raise forms.ValidationError('Phone number must start with 09 digits')

        if len(phone) != 11:
            raise forms.ValidationError('Phone number must have 11 digits')

        if not phone.isdigit():
            raise forms.ValidationError('Phone must be a number')

        return phone


class ShopUserChangeForm(UserChangeForm):
    class Meta:
        model = ShopUser
        fields = ['phone', 'first_name', 'last_name', 'address', 'is_active', 'is_staff', 'is_superuser', 'date_joined']

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')

        if self.instance.pk:
            if ShopUser.objects.filter(phone=phone).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError('Entered phone already exists.')

        else:
            if ShopUser.objects.filter(phone=phone).exists():
                raise forms.ValidationError('Entered phone already exists.')

        if not phone.startswith('09'):
            raise forms.ValidationError('Phone number must start with 09 digits')

        if len(phone) != 11:
            raise forms.ValidationError('Phone number must have 11 digits')

        if not phone.isdigit():
            raise forms.ValidationError('Phone must be a number')

        return phone


class LoginForm(AuthenticationForm):
    phone = forms.CharField(label='phone', max_length=11, required=True,
                            widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(max_length=20, required=True,
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(max_length=100, required=True, widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=100, required=True, widget=forms.PasswordInput, label='Repeat Password')

    class Meta:
        model = ShopUser
        fields = ['phone', 'first_name', 'last_name', 'address']

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')

        if self.instance.pk:
            if ShopUser.objects.filter(phone=phone).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError('Entered phone already exists.')

        else:
            if ShopUser.objects.filter(phone=phone).exists():
                raise forms.ValidationError('Entered phone already exists.')

        if not phone.startswith('09'):
            raise forms.ValidationError('Phone number must start with 09 digits')

        if len(phone) != 11:
            raise forms.ValidationError('Phone number must have 11 digits')

        if not phone.isdigit():
            raise forms.ValidationError('Phone must be a number')

        return phone

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password2'] != cd['password']:
            raise forms.ValidationError('Passwords don\'t match')
        else:
            return cd['password2']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = ShopUser
        fields = ["phone", "first_name", "last_name", 'address']

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')

        if self.instance.pk:
            if ShopUser.objects.filter(phone=phone).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError('Entered phone already exists.')

        else:
            if ShopUser.objects.filter(phone=phone).exists():
                raise forms.ValidationError('Entered phone already exists.')

        if not phone.startswith('09'):
            raise forms.ValidationError('Phone number must start with 09 digits')

        if len(phone) != 11:
            raise forms.ValidationError('Phone number must have 11 digits')

        if not phone.isdigit():
            raise forms.ValidationError('Phone must be a number')

        return phone

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password2'] != cd['password']:
            raise forms.ValidationError('Passwords don\'t match')
        else:
            return cd['password2']


class PhoneVerificationForm(forms.Form):
    phone = forms.CharField(max_length=11, label='شماره همراه')

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')

        if len(phone) != 11:
            raise forms.ValidationError('Phone number must have 11 digits')

        if not phone.isdigit():
            raise forms.ValidationError('Phone must be a number')

        return phone


class CodeVerificationForm(forms.Form):
    verification_code = forms.CharField(max_length=6, label='کد تایید')

    def clean_vcode(self):
        verification_code = self.cleaned_data.get('verification_code')

        # if not phone.startswith('09'):
        #     raise forms.ValidationError('Phone number must start with 09 digits')

        if len(verification_code) != 6:
            raise forms.ValidationError('code must have 6 digits')

        if not verification_code.isdigit():
            raise forms.ValidationError('code must be a number')

        return verification_code
