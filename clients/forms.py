from django import forms
from django.core.exceptions import ValidationError
from .models import Client
import re


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}),
        label='Пароль',
        min_length=6
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Подтверждение пароля'}),
        label='Подтверждение пароля'
    )

    class Meta:
        model = Client
        fields = ['name', 'surname', 'middle_name', 'phone', 'email', 'birth_date', 'passport_number']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя'}),
            'surname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Фамилия'}),
            'middle_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Отчество'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+7 (XXX) XXX-XX-XX'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@example.com'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'passport_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'XXXX XXXXXX'}),
        }
        labels = {
            'name': 'Имя',
            'surname': 'Фамилия',
            'middle_name': 'Отчество',
            'phone': 'Телефон',
            'email': 'Email',
            'birth_date': 'Дата рождения',
            'passport_number': 'Номер паспорта',
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        phone = re.sub(r'[\s\-\(\)]', '', phone)
        if not re.match(r'^\+?[0-9]{10,15}$', phone):
            raise ValidationError('Введите корректный номер телефона')
        return phone

    def clean_passport_number(self):
        passport = self.cleaned_data.get('passport_number')
        passport = re.sub(r'\s', '', passport)
        if not re.match(r'^[0-9]{4}[0-9]{6}$', passport):
            raise ValidationError('Введите корректный номер паспорта (XXXX XXXXXX)')
        return passport

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            raise ValidationError('Пароли не совпадают')

        return cleaned_data

    def save(self, commit=True):
        client = super().save(commit=False)
        client.set_password(self.cleaned_data['password'])
        if commit:
            client.save()
        return client


class LoginForm(forms.Form):
    phone = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+7 (XXX) XXX-XX-XX'}),
        label='Телефон'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}),
        label='Пароль'
    )