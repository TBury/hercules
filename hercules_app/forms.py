from django.forms import ModelForm
from django import forms
from hercules_app.models import Driver, Waybill, Company, Vehicle, CompanySettings, Disposition, \
    Gielda, WorkApplications


class SetNickForm(ModelForm):
    class Meta:
        model = Driver
        fields = [
            'nick',
        ]

    def clean_nick(self):
        if Driver.objects.filter(nick=self.cleaned_data.get("nick")).exists():
            if (self.cleaned_data.get("nick") == "JanuszTransportu"):
                raise forms.ValidationError("Kurła, Pjoter, zajęli mi tego nicka. Musimy coś innego wymyśleć.")
            raise forms.ValidationError("Ten nick został już zajęty. Wybierz inny nick.")
        return self.cleaned_data.get("nick")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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
            if field == "loading_city":
                self.fields[field].widget.attrs.update(
                    {'id': 'autoCompleteCities'})
            if field == "unloading_city":
                self.fields[field].widget.attrs.update(
                    {'id': 'autoCompleteUnloadingCities'})
            if field == "loading_spedition":
                self.fields[field].widget.attrs.update(
                    {'id': 'autoCompleteSpedition'})
            if field == "unloading_spedition":
                self.fields[field].widget.attrs.update(
                    {'id': 'autoCompleteUnloadingSpedition'})
            if field == "cargo":
                self.fields[field].widget.attrs.update(
                    {'id': 'autoCompleteCargo'})
            self.fields[field].widget.attrs.update(
                {'class': 'input', 'autocomplete': 'off'})


class EditVehicleForm(ModelForm):
    class Meta:
        model = Vehicle
        fields = (
            'photo',
            'brand',
            'model',
            'cabin',
            'engine',
            'engine_power',
            'gearbox',
            'wheelbase',
            'wheels',
            'odometer',
        )

    def __init__(self, drivers, current_driver, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['driver'] = forms.ChoiceField(widget = forms.Select(), choices=drivers, required=True, initial=current_driver)
        for field in self.fields:
            if field == "brand":
                self.fields[field].widget.attrs.update(
                    {'id': 'autoCompleteBrand'})
            if field == "model":
                self.fields[field].widget.attrs.update(
                    {'id': 'autoCompleteModel'})
            if field == "cabin":
                self.fields[field].widget.attrs.update(
                    {'id': 'autoCompleteCabin'})
            if field == "engine":
                self.fields[field].widget.attrs.update(
                    {'id': 'autoCompleteEngine'})
            if field == "gearbox":
                self.fields[field].widget.attrs.update(
                    {'id': 'autoCompleteGearbox'})
            if field == "wheelbase":
                self.fields[field].widget.attrs.update(
                    {'id': 'autoCompleteWheelbase'})
            if field == "wheels":
                self.fields[field].widget.attrs.update(
                    {'id': 'autoCompleteWheels'})
            if field == "engine_power":
                self.fields[field].widget.attrs.update(
                    {'min': '0', 'required': 'required'})
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
            'engine_power',
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
            if field == "brand":
                self.fields[field].widget.attrs.update(
                    {'id': 'autoCompleteBrand'})
            if field == "model":
                self.fields[field].widget.attrs.update(
                    {'id': 'autoCompleteModel'})
            if field == "cabin":
                self.fields[field].widget.attrs.update(
                    {'id': 'autoCompleteCabin'})
            if field == "engine":
                self.fields[field].widget.attrs.update(
                    {'id': 'autoCompleteEngine'})
            if field == "gearbox":
                self.fields[field].widget.attrs.update(
                    {'id': 'autoCompleteGearbox'})
            if field == "wheelbase":
                self.fields[field].widget.attrs.update(
                    {'id': 'autoCompleteWheelbase'})
            if field == "wheels":
                self.fields[field].widget.attrs.update(
                    {'id': 'autoCompleteWheels'})
            if field == "engine_power":
                self.fields[field].widget.attrs.update(
                    {'min': '0', 'required': 'required'})
            self.fields[field].widget.attrs.update({'class': 'input', 'autocomplete': 'off'})

class AddNewCompanyForm(ModelForm):
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'input'})
            if field == 'is_recruiting':
                self.fields[field].widget.attrs.update({'class': 'switch is-rounded', 'id': 'switchRoundedDefault',
                                                        'name': 'switchRoundedDefault'})
            if field == 'dlc':
                self.fields[field].widget.attrs.update({'class': 'hidden', 'id': 'dlc'})
            if field == 'description':
                self.fields[field].widget.attrs.update({'class': 'textarea', 'rows': '20'})
            elif field == 'games':
                self.fields[field].widget.attrs.update(
                    {'class': 'hidden', 'id': 'games'})


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
            if field != 'is_recruiting' and field != 'description':
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
            if field == 'description':
                self.fields[field].widget.attrs.update({'class': 'textarea', 'rows': '20'})
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

class NewOfferForm(ModelForm):
    class Meta:
        model = Gielda
        fields = (
            'loading_city',
            'loading_country',
            'loading_spedition',
            'unloading_city',
            'unloading_country',
            'unloading_spedition',
            'cargo',
            'tonnage',
            'price',
            'adr',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field == "loading_city":
                self.fields[field].widget.attrs.update({'id': 'autoCompleteCities'})
            if field == "unloading_city":
                self.fields[field].widget.attrs.update(
                    {'id': 'autoCompleteUnloadingCities'})
            if field == "loading_spedition":
                self.fields[field].widget.attrs.update({'id': 'autoCompleteSpedition'})
            if field == "unloading_spedition":
                self.fields[field].widget.attrs.update(
                    {'id': 'autoCompleteUnloadingSpedition'})
            if field == "cargo":
                self.fields[field].widget.attrs.update({'id': 'autoCompleteCargo'})
            if field == "loading_country" or field == "unloading_country" or field == "adr":
                self.fields[field].widget.attrs.update({'class': 'hidden'})
                self.fields[field].required = False
            else:
                self.fields[field].widget.attrs.update(
                    {'class': 'input', 'autocomplete': 'off'})

class NewDispositionForm(ModelForm):
    deadline = forms.DateTimeField(
                                   widget=forms.DateTimeInput(attrs={
                                       'class': 'datetimepicker',
                                       'type': 'datetime'
                                   }, format="%d/%m/%Y %H:%M",
                                   )
    )
    class Meta:
        model = Disposition
        fields = (
            'loading_city',
            'loading_country',
            'loading_spedition',
            'unloading_city',
            'unloading_country',
            'unloading_spedition',
            'cargo',
            'tonnage',
            'deadline',
        )

    def __init__(self, drivers, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['driver'] = forms.ChoiceField(
            widget=forms.Select(), choices=drivers, required=True)
        for field in self.fields:
            if field == "loading_city":
                self.fields[field].widget.attrs.update({'id': 'autoCompleteCities'})
            if field == "unloading_city":
                self.fields[field].widget.attrs.update(
                    {'id': 'autoCompleteUnloadingCities'})
            if field == "loading_spedition":
                self.fields[field].widget.attrs.update({'id': 'autoCompleteSpedition'})
            if field == "unloading_spedition":
                self.fields[field].widget.attrs.update(
                    {'id': 'autoCompleteUnloadingSpedition'})
            if field == "cargo":
                self.fields[field].widget.attrs.update({'id': 'autoCompleteCargo'})
            if field == "loading_country" or field == "unloading_country":
                self.fields[field].widget.attrs.update({'class': 'hidden'})
                self.fields[field].required = False
            else:
                self.fields[field].widget.attrs.update(
                    {'class': 'input', 'autocomplete': 'off'})

class SendApplicationForm(ModelForm):
    class Meta:
        model = WorkApplications
        fields = (
            'driver',
            'town',
            'dlc',
            'age',
            'steam_profile',
            'truckers_mp_profile',
            'about_me',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['driver'] = forms.CharField(widget=forms.TextInput, required=True)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'input'})
            if field == "driver":
                self.fields[field].widget.attrs.update({'class': 'input', 'readonly': 'readonly'})
            if field == 'about_me':
                self.fields[field].widget.attrs.update({'class': 'textarea', 'rows': '20'})
            if field == 'dlc':
                self.fields[field].widget.attrs.update({'class': 'hidden', 'id': 'dlc'})