from django.forms import ModelForm
from django import forms
from hercules_app.models import Driver, Waybill, DriverStatistics, Company, Vehicle, CompanySettings


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
            'photo',
            'brand',
            'model',
            'cabin',
            'engine',
            'gearbox',
            'wheelbase',
            'wheels',
            'odometer',
        )

    def __init__(self, drivers, current_driver, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['driver'] = forms.ChoiceField(widget = forms.Select(), choices=drivers, required=True, initial=current_driver)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'input'})

class AddVehicleForm(ModelForm):
    class Meta:
        model = Vehicle
        fields = (
            'photo',
            'brand',
            'model',
            'cabin',
            'engine',
            'gearbox',
            'wheelbase',
            'wheels',
            'odometer',
        )

    def __init__(self, drivers, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['driver'] = forms.ChoiceField(
            widget=forms.Select(), choices=drivers, required=True)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'input'})

class EditCompanyInformationForm(ModelForm):
    is_recruiting = forms.BooleanField(required=False, initial=False)
    games = forms.CharField(required=False)
    class Meta:
        model = Company
        fields = (
            'name',
            'logo',
            'website',
            'dlc',
            'communicator_url',
            'is_recruiting',
            'description',
        )

    def __init__(self, is_recruiting, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field != 'is_recruiting':
                self.fields[field].widget.attrs.update({'class': 'input'})
            else:
                if is_recruiting:
                    self.fields[field].widget.attrs.update({'class': 'switch is-rounded', 'id': 'switchRoundedDefault',
                        'name': 'switchRoundedDefault', 'checked': 'checked'})
                else:
                    self.fields[field].widget.attrs.update({'class': 'switch is-rounded', 'id': 'switchRoundedDefault',
                        'name': 'switchRoundedDefault'})
            if field == 'dlc':
                self.fields[field].widget.attrs.update({'class': 'hidden', 'id': 'dlc'})
            elif field == 'games':
                self.fields[field].widget.attrs.update(
                    {'class': 'hidden', 'id': 'games'})


class EditSettingsForm(ModelForm):
    class Meta:
        model = CompanySettings
        fields = (
            'periodic_norm_type',
            'periodic_norm_distance',
            'disposition_norm',
            'disposition_norm_type',
            'random_vehicle',
            'random_vehicle_type',
            'only_assistant',
            'auto_synchronization',
            'max_90',
        )

    def __init__(self, random_vehicle, auto_sync, only_assistant, max_90, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field == "periodic_norm_type":
                self.fields[field].widget = forms.RadioSelect(attrs=
                    {'id': 'periodic-norm', 'class': 'is-checkradio', 'name': 'periodic-norm', 'type': 'radio'}, choices=CompanySettings.PeriodicNormType.choices)
            elif field == "random_vehicle_type":
                self.fields[field].widget = forms.RadioSelect(
                    attrs={'id': 'random-vehicle', 'class': 'is-checkradio', 'name': 'random-vehicle', 'type': 'radio'}, choices=CompanySettings.PeriodicNormType.choices)
            elif field == "disposition_norm_type":
                self.fields[field].widget = forms.RadioSelect(
                    attrs={'id': 'disposition-norm', 'class': 'is-checkradio', 'name': 'disposition-norm', 'type': 'radio'}, choices=CompanySettings.PeriodicNormType.choices)
            elif field == "random_vehicle":
                if random_vehicle:
                    self.fields[field].widget.attrs.update({'class': 'switch is-rounded', 'id': 'random-vehicle',
                        'name': 'random-vehicle', 'checked': 'checked'})
                else:
                    self.fields[field].widget.attrs.update({'class': 'switch is-rounded', 'id': 'random-vehicle',
                        'name': 'random-vehicle', })
            elif field == "only_assistant":
                if only_assistant:
                    self.fields[field].widget.attrs.update({'class': 'switch is-rounded', 'id': 'only-assistant',
                        'name': 'only-assistant-check', 'checked': 'checked'})
                else:
                    self.fields[field].widget.attrs.update({'class': 'switch is-rounded', 'id': 'only-assistant',
                        'name': 'only-assistant-check', })
            elif field == "auto_synchronization":
                if auto_sync:
                    self.fields[field].widget.attrs.update({'class': 'switch is-rounded', 'id': 'sync-save-check',
                        'name': 'sync-save', 'checked': 'checked'})
                else:
                    self.fields[field].widget.attrs.update({'class': 'switch is-rounded', 'id': 'sync-save-check',
                        'name': 'sync-save', })
            elif field == "max_90":
                if max_90:
                    self.fields[field].widget.attrs.update({'class': 'switch is-rounded', 'id': 'max-90-check',
                        'name': 'max-90', 'checked': 'checked'})
                else:
                    self.fields[field].widget.attrs.update({'class': 'switch is-rounded', 'id': 'max-90-check',
                        'name': 'max-90', })
            else:
                self.fields[field].widget.attrs.update({'class': 'input'})
