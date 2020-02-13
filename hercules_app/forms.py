from django.forms import ModelForm
from django import forms
from hercules_app.models import Driver


class SetNickForm(ModelForm):
    nick = forms.CharField()
    class Meta:
        model = Driver
        fields = [
            'nick',
        ]
