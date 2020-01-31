from django.db import models
from django.utils.translation import gettext_lazy as _

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
    def __str__(self):
        return self.name

class Driver(models.Model):
    id = models.AutoField(primary_key=True)
    login = models.CharField(max_length=64)
    nick = models.CharField(max_length=64)
    email = models.EmailField(max_length=128)
    password = models.CharField(max_length=64)
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE)
    avatar = models.FileField(upload_to='avatars/')
    last_delivery = models.DateTimeField(auto_now_add=True)
    length_of_service = models.DateTimeField(auto_now_add=True)
    position = models.CharField(max_length=20)
    def __str__(self):
        return self.nick

class Vehicle(models.Model):
    id = models.AutoField(primary_key=True)
    driver_id = models.ForeignKey(Driver, on_delete=models.CASCADE)
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE)
    brand = models.CharField(max_length=20)
    model = models.CharField(max_length=80)
    cabin = models.CharField(max_length=64)
    registration_number = models.CharField(max_length=8)
    engine = models.CharField(max_length=100)
    gearbox = models.CharField(max_length=100)
    wheelbase = models.CharField(max_length=4)
    wheels = models.CharField(max_length=75)
    odometer = models.PositiveIntegerField(default=0)
    def __str__(self):
        return self.id

class DriverStatistics(models.Model):
    driver_id = models.ForeignKey(Driver, on_delete=models.CASCADE)
    distance = models.PositiveIntegerField(default=0)
    tonnage = models.PositiveIntegerField(default=0)
    income = models.PositiveIntegerField(default=0)
    average_fuel = models.FloatField(default=0.0)
    deliveries_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.driver_id

class Waybills(models.Model):
    id = models.AutoField(primary_key=True)
    loading_city = models.CharField(max_length=64)
    unloading_city = models.CharField(max_length=64)
    loading_spedition = models.CharField(max_length=100)
    unloading_spedition = models.CharField(max_length=100)
    cargo = models.CharField(max_length=64)
    tonnage = models.IntegerField(default=0)
    fuel = models.IntegerField(default=0)
    damage = models.SmallIntegerField(default=0)
    note = models.TextField(default='')
    class WaybillStatus(models.TextChoices):
        ACCEPTED = 'acc', _('accepted')
        DECLINED = 'dec', _('declined')
        TO_EDIT = 'edt', _('to_edit')
        NOT_CHECKED = 'ntc', _('not_checked')

    status = models.CharField(choices=WaybillStatus.choices, default=WaybillStatus.NOT_CHECKED, max_length=12)

    def __str__(self):
        return self.id

class Gielda(models.Model):
    id = models.AutoField(primary_key=True)
    loading_city = models.CharField(max_length=64)
    unloading_city = models.CharField(max_length=64)
    loading_spedition = models.CharField(max_length=100)
    unloading_spedition = models.CharField(max_length=100)
    cargo = models.CharField(max_length=64)
    tonnage = models.IntegerField(default=0)

    class Trailer(models.TextChoices):
        CURTAIN = 'curt', _('curtain')
        REEFER = 'reef', _('reefer')
        LOWDECK = 'ldc', _('low_deck')
        CISTERN = 'cis', _('cistern')
        TARP = 'trp', _('tarp') #plandeka
    trailer = models.CharField(choices=Trailer.choices, max_length=8)
    price = models.PositiveIntegerField(default=0)
    creator = models.CharField(default='SYSTEM', max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    adr = models.BooleanField(default=False)
    oversized = models.BooleanField(default=False)

    def __str__(self):
        return self.id

class Disposition(models.Model):
    id = models.AutoField(primary_key=True)
    loading_city = models.CharField(max_length=64)
    unloading_city = models.CharField(max_length=64)
    loading_spedition = models.CharField(max_length=100)
    unloading_spedition = models.CharField(max_length=100)
    cargo = models.CharField(max_length=64)
    tonnage = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    class DispositionType(models.TextChoices):
        ROZPISKA = 'roz', _('rozpiska')
        DYSPOZYCJA = 'dys', _('dyspozycja')
    disposition_type = models.CharField(choices=DispositionType.choices, default=DispositionType.DYSPOZYCJA, max_length=10)

    def __str__(self):
        return self.id

class CompanySettings(models.Model):
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE)
    class PeriodicNormType(models.TextChoices):
        WEEK = 'wk', _('week')
        MONTH = 'mth', _('month')
    periodic_norm_type = models.CharField(choices=PeriodicNormType.choices, default=PeriodicNormType.WEEK, max_length=5)
    periodic_norm_distance = models.PositiveIntegerField(default=0)
    disposition_norm = models.IntegerField(default=0)
    disposition_norm_type = models.CharField(choices=PeriodicNormType.choices, default=PeriodicNormType.WEEK, max_length=5)
    random_vehicle = models.BooleanField(default=False)
    random_vehicle_timestamp = models.DateTimeField(auto_now_add=True)
    only_assistant = models.BooleanField(default=False)
    auto_synchronization = models.BooleanField(default=False)

    def __str__(self):
        return self.company_id

class WorkApplications(models.Model):
    id = models.AutoField(primary_key=True)
    driver_id = models.ForeignKey(Driver, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(default='')

    def __str__(self):
        return self.id
