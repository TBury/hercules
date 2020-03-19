from django.forms import ModelForm
from django import forms
from hercules_app.models import Driver, Waybill

class SetNickForm(ModelForm):
    nick = forms.CharField()
    class Meta:
        model = Driver
        fields = [
            'nick',
        ]

class FirstScreenshotForm(ModelForm):
    class Meta:
        model = Waybill
        fields = ('first_screen', )

class SecondScreenshotForm(ModelForm):
    class Meta:
        model = Waybill
        fields = ('end_screen', )

class AddWaybillForm(ModelForm):
    class Meta:
        model = Waybill
        fields = (
            'loading_city',
            'unloading_city',
            'loading_spedition',
            'unloading_spedition',
            'cargo',
            'tonnage',
            'fuel',
            'damage',
            'note',
            )
