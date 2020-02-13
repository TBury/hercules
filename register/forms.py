from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

class CreateUserForm(forms.ModelForm):
    username = forms.CharField(
        label="Nazwa użytkownika", widget=forms.TextInput(attrs={'class': 'input'}))
    email = forms.EmailField(
        label="Adres e-mail", widget=forms.EmailInput(attrs={'class': 'input'}))
    password = forms.CharField(
        label="Hasło", widget=forms.PasswordInput(attrs={'class': 'input'}))

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
        ]
