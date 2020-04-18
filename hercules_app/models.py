from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from datetime import datetime
from typing import NamedTuple
from django.utils import timezone


class Company(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)
    drivers_count = models.SmallIntegerField(default=0)
    logo = models.ImageField(upload_to='logos', default='')
    distance = models.PositiveIntegerField(default=0)
    average_fuel = models.FloatField(default=0.0)
    income = models.PositiveIntegerField(default=0)
    tonnage = models.PositiveIntegerField(default=0)
    waybill_count = models.PositiveIntegerField(default=0)
    description = models.TextField(default='')
    is_recruiting = models.BooleanField(default=True)
    is_ets2 = models.BooleanField(default=True)
    is_ats = models.BooleanField(default=False)
    is_singleplayer = models.BooleanField(default=True)
    is_multiplayer = models.BooleanField(default=True)
    is_promods = models.BooleanField(default=False)

    def get_company_name(self):
        return self.name

    def get_company_statistics(self):
        statistics = {
            'distance': self.distance,
            'average_fuel': self.average_fuel,
            'income': self.income,
            'waybills': self.waybill_count,
            'drivers_count': self.drivers_count,
        }
        return statistics

    def __str__(self):
        return self.name


class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    nick = models.CharField(max_length=64, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars', null=True)
    last_delivery = models.DateTimeField(auto_now_add=True)
    length_of_service = models.DateTimeField(auto_now_add=True)
    position = models.CharField(max_length=20, null=True)
    is_employeed = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


    def get_vehicle_info(driver):
        try:
            vehicle = Vehicle.objects.get(driver=driver)
            vehicle_info = {
                'brand': vehicle.brand,
                'model': vehicle.model,
                'cabin': vehicle.cabin,
                'engine': vehicle.engine,
                'odometer': vehicle.odometer,
                'photo': vehicle.photo.url,
            }
        except:
            vehicle_info = ''
        finally:
            return vehicle_info

    def get_driver_info_from_database(username):
        driver = Driver.objects.get(user=username)
        if driver.is_employeed:
            company = Company.objects.get(name=driver.company.name)
            company = company.name
        else:
            company = ""

        vehicle = Driver.get_vehicle_info(driver)

        try:
            avatar = driver.avatar.url
        except:
            avatar = ''

        driver_info = {
            'nick': driver.nick,
            'company': company,
            'vehicle': vehicle,
            'avatar': driver.avatar.url,
        }
        return driver_info


    def set_driver_info(request):
        driver_info = Driver.get_driver_info_from_database(request.user)
        request.session['driver_info'] = driver_info

    def get_driver_info(request):
        Driver.set_driver_info(request)

        class DriverInfo(NamedTuple):
            nick: str
            company: str
            vehicle: Vehicle
            avatar: str
        try:
            driver_info = request.session.get('driver_info')
        except driver_info is None:
            SetDriverInfo(request)
        finally:
            info = DriverInfo(
                driver_info['nick'],
                driver_info['company'],
                driver_info['vehicle'],
                driver_info['avatar'],
            )
        return info


class Vehicle(models.Model):
    id = models.AutoField(primary_key=True)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, null=True, blank=True)
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, null=True, blank=True)
    photo = models.ImageField(upload_to='vehicles', null=True)
    model = models.CharField(max_length=80)
    cabin = models.CharField(max_length=64)
    registration_number = models.CharField(max_length=8)
    engine = models.CharField(max_length=100)
    gearbox = models.CharField(max_length=100)
    wheelbase = models.CharField(max_length=4)
    wheels = models.CharField(max_length=75)
    odometer = models.PositiveIntegerField(default=0)

    class Brand(models.TextChoices):
        MAN = 'MAN', _('MAN')
        MERCEDES_BENZ = 'Mercedes-Benz', _('Mercedes-Benz')
        DAF = 'DAF', _('DAF')
        RENAULT = 'Renault', _('Renault')
        SCANIA = 'Scania', _('Scania')
        IVECO = 'Iveco', _('Iveco')
    brand = models.CharField(choices=Brand.choices,
                             default=Brand.MAN, max_length=20)

    def __str__(self):
        return str(self.id)


class DriverStatistics(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    distance = models.PositiveIntegerField(default=0)
    tonnage = models.PositiveIntegerField(default=0)
    income = models.PositiveIntegerField(default=0)
    fuel = models.PositiveIntegerField(default=0)
    average_fuel = models.FloatField(default=0.0)
    deliveries_count = models.PositiveIntegerField(default=0)

    def get_driver_statistics(driver):
        try:
            statistics = DriverStatistics.objects.get(driver_id=driver)
        except:
            # TODO: implement exception
            statistics = ''
        finally:
            return statistics

    def __str__(self):
        return self.driver.nick


class Waybill(models.Model):
    id = models.AutoField(primary_key=True)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, null=True)
    loading_city = models.CharField(max_length=64)
    loading_country = models.CharField(max_length=100, default='')
    unloading_city = models.CharField(max_length=64)
    unloading_country = models.CharField(max_length=100, default='')
    loading_spedition = models.CharField(max_length=100)
    unloading_spedition = models.CharField(max_length=100)
    cargo = models.CharField(max_length=64)
    tonnage = models.IntegerField(default=0)
    distance = models.IntegerField(default=0)
    income = models.IntegerField(default=0)
    fuel = models.IntegerField(default=0)
    damage = models.SmallIntegerField(default=0)
    note = models.TextField(default='', blank=True)
    first_screen = models.ImageField(upload_to='waybills', default="")
    end_screen = models.ImageField(upload_to='waybills', default="")
    finish_date = models.DateTimeField(auto_now_add=True)
    screens_id = models.CharField(max_length=72, default='')

    class WaybillStatus(models.TextChoices):
        ACCEPTED = 'accepted', _('accepted')
        DECLINED = 'declined', _('declined')
        TO_EDIT = 'to-edit', _('to_edit')
        NOT_CHECKED = 'not-checked', _('not_checked')

    status = models.CharField(
        choices=WaybillStatus.choices, default=WaybillStatus.NOT_CHECKED, max_length=12)

    def __str__(self):
        return str(self.id)


class Gielda(models.Model):
    id = models.AutoField(primary_key=True)
    loading_city = models.CharField(max_length=64)
    loading_country = models.CharField(max_length=64)
    unloading_city = models.CharField(max_length=64)
    unloading_country = models.CharField(max_length=64)
    loading_spedition = models.CharField(max_length=100)
    unloading_spedition = models.CharField(max_length=100)
    cargo = models.CharField(max_length=64)
    tonnage = models.IntegerField(default=0)

    class Trailer(models.TextChoices):
        CURTAIN = 'Firanka', _('curtain')
        REEFER = 'Chłodnia', _('reefer')
        LOWDECK = 'Niskopodłogowa', _('low_deck')
        CISTERN = 'Cysterna', _('cistern')
        TARP = 'Plandeka', _('tarp')  # plandeka
    trailer = models.CharField(choices=Trailer.choices, max_length=14)
    price = models.PositiveIntegerField(default=0)
    creator = models.CharField(default='SYSTEM', max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)

    class Adr(models.TextChoices):
        NONE = 'Nie dotyczy', _('none')
        EXPLOSIVES = 'ADR-1: materiały wybuchowe', _('explosives')
        GASES = 'ADR-2: gazy', _('gases')
        LIQUIDS = 'ADR-3: płyny łatwopalne', _('liquids')
        SOLIDS = 'ADR-4: materiały stałe zapalne', _('solids')
        TOXIC = 'ADR-6: toksyczne i zakaźne substancje', _('toxic')
        CORROSIVE = 'ADR-8: toksyczne substancje', _('corrosive')
    adr = models.CharField(choices=Adr.choices, max_length=64)
    oversized = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)


class Rozpiska(models.Model):
    rozpiska_id = models.IntegerField(default=0)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, default='')
    first_disposition_id = models.IntegerField(default=0)
    second_disposition_id = models.IntegerField(default=0)
    third_disposition_id = models.IntegerField(default=0)
    fourth_disposition_id = models.IntegerField(default=0)
    fifth_disposition_id = models.IntegerField(default=0)


class Disposition(models.Model):
    id = models.AutoField(primary_key=True)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, default='')
    loading_city = models.CharField(max_length=64)
    loading_country = models.CharField(max_length=64, default='')
    unloading_city = models.CharField(max_length=64)
    unloading_country = models.CharField(max_length=64, default='')
    loading_spedition = models.CharField(max_length=100)
    unloading_spedition = models.CharField(max_length=100)
    cargo = models.CharField(max_length=64)
    tonnage = models.IntegerField(default=0)
    deadline = models.DateTimeField(default=datetime.now, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_rozpiska = models.BooleanField(default=False)
    # field for dispositions from rozpiska only
    finished = models.BooleanField(default=False)
    rozpiska = models.ForeignKey(Rozpiska, on_delete=models.CASCADE, default=0)

    def __str__(self):
        return str(self.id)


class CompanySettings(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    class PeriodicNormType(models.TextChoices):
        WEEK = 'wk', _('week')
        MONTH = 'mth', _('month')
    periodic_norm_type = models.CharField(
        choices=PeriodicNormType.choices, default=PeriodicNormType.WEEK, max_length=5)
    periodic_norm_distance = models.PositiveIntegerField(default=0)
    disposition_norm = models.IntegerField(default=0)
    disposition_norm_type = models.CharField(
        choices=PeriodicNormType.choices, default=PeriodicNormType.WEEK, max_length=5)
    random_vehicle = models.BooleanField(default=False)
    random_vehicle_timestamp = models.DateTimeField(auto_now_add=True)
    only_assistant = models.BooleanField(default=False)
    auto_synchronization = models.BooleanField(default=False)

    def __str__(self):
        return str(self.company_id)


class WorkApplications(models.Model):
    id = models.AutoField(primary_key=True)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(default='')

    def __str__(self):
        return str(self.id)
