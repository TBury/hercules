from django.forms import ModelForm
from django import forms
from hercules_app.models import Driver, Waybill, DriverStatistics, Vehicle


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
    note = forms.IntegerField(max_value=100, min_value=0, required=False)
    note = forms.CharField(required=False)

    class Meta:
        model = Waybill
        fields = (
            'loading_city',
            'unloading_city',
            'loading_spedition',
            'unloading_spedition',
            'cargo',
            'tonnage',
            'distance',
            'fuel',
            'income',
            'damage',
            'note',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'input'})


class EditVehicleForm(ModelForm):
    class Meta:
        model = Vehicle
        fields = (
            'brand',
            'model',
            'cabin',
            'engine',
            'gearbox',
            'wheelbase',
            'wheels',
            'odometer',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'input'})