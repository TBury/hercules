from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User


class Company(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)
    drivers_count = models.SmallIntegerField(default=0)
    logo = models.FileField(upload_to='logos/', default='')
    distance = models.PositiveIntegerField(default=0)
    average_fuel = models.FloatField(default=0.0)
    income = models.PositiveIntegerField(default=0)
    waybill_count = models.PositiveIntegerField(default=0)
    description = models.TextField(default='')

    def get_company_name(self):
        return self.name

    def get_company_statistics(self):
        statistics = {'distance': self.distance,
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
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    avatar = models.FileField(upload_to='avatars/', null=True)
    last_delivery = models.DateTimeField(auto_now_add=True)
    length_of_service = models.DateTimeField(auto_now_add=True)
    position = models.CharField(max_length=20, null=True)
    is_employeed = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def get_username(username):
        driver = Driver.objects.get(user=username)
        args = {
            'driver': driver,
        }
        return args


class Vehicle(models.Model):
    id = models.AutoField(primary_key=True)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
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

    def __str__(self):
        return self.driver.nick


class Waybill(models.Model):
    id = models.AutoField(primary_key=True)
    loading_city = models.CharField(max_length=64)
    unloading_city = models.CharField(max_length=64)
    loading_spedition = models.CharField(max_length=100)
    unloading_spedition = models.CharField(max_length=100)
    cargo = models.CharField(max_length=64)
    tonnage = models.IntegerField(default=0)
    distance = models.IntegerField(default=0)
    income = models.IntegerField(default=0)
    fuel = models.IntegerField(default=0)
    damage = models.SmallIntegerField(default=0)
    note = models.TextField(default='')
    first_screen = models.ImageField(upload_to='media/', default="")
    end_screen = models.ImageField(upload_to='media/', default="")

    class WaybillStatus(models.TextChoices):
        ACCEPTED = 'acc', _('accepted')
        DECLINED = 'dec', _('declined')
        TO_EDIT = 'edt', _('to_edit')
        NOT_CHECKED = 'ntc', _('not_checked')

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
    adr = models.CharField(default='Nie dotyczy', max_length=24)
    oversized = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)


class Disposition(models.Model):
    id = models.AutoField(primary_key=True)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, default='')
    loading_city = models.CharField(max_length=64)
    unloading_city = models.CharField(max_length=64)
    loading_spedition = models.CharField(max_length=100)
    unloading_spedition = models.CharField(max_length=100)
    cargo = models.CharField(max_length=64)
    tonnage = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

# TODO: klasa rozpiski
# class Rozpiska(models.Model):


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
