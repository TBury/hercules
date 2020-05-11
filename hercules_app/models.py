from django.db import models
from django.db.models import Sum
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from typing import NamedTuple
from django.utils import timezone
import pytz




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
    website = models.URLField(default='', blank=True, null=True)
    communicator_url = models.URLField(default='', blank=True, null=True)
    is_recruiting = models.BooleanField(default=True, blank=True)
    is_ets2 = models.BooleanField(default=True)
    is_ats = models.BooleanField(default=False)
    is_singleplayer = models.BooleanField(default=True)
    is_multiplayer = models.BooleanField(default=True)
    is_promods = models.BooleanField(default=False)
    dlc = models.CharField(max_length=256, default='', blank=True, null=True)

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

    def get_company_drivers_info(company_id, sort_by):
        if sort_by == "-position":
            drivers = Driver.objects.all().filter(company=company_id).order_by(sort_by)
        else:
            drivers = Driver.objects.all().filter(company=company_id)
        company_drivers = []
        for driver in drivers:
            statistics = DriverStatistics.objects.get(driver=driver)

            try:
                last_waybill = Waybill.objects.get(driver=driver)
                last_waybill = last_waybill.finish_date
            except Waybill.DoesNotExist:
                last_waybill = "Brak danych"
            today = datetime.today().replace(tzinfo=None)
            length_of_service = abs(
                (today - driver.length_of_service).days)
            periodic_norm_distance = CompanySettings.check_periodic_norm_distance(
                driver)
            periodic_norm = CompanySettings.objects.get(company=company_id)
            periodic_norm = periodic_norm.periodic_norm_distance
            realised = periodic_norm_distance >= periodic_norm
            company_driver = {
                'id': driver.id,
                'nick': driver.nick,
                'avatar': driver.avatar.url,
                'position': driver.position,
                'distance': statistics.distance,
                'last_delivery': last_waybill,
                'length_of_service': length_of_service,
                'realised': realised,
            }
            if sort_by == 'realised':
                if realised:
                    company_drivers.append(company_driver)
            elif sort_by == 'not-realised':
                if not realised:
                    company_drivers.append(company_driver)
            else:
                company_drivers.append(company_driver)
        if sort_by == "service-length":
            company_drivers = sorted(company_drivers, key = lambda i: i['length_of_service'])
        elif sort_by == "-service-length":
            company_drivers = sorted(company_drivers, key = lambda i: i['length_of_service'], reverse = True)
        elif sort_by == 'last-delivery':
            company_drivers = sorted(
                company_drivers, key=lambda i: i['last_delivery'])
        elif sort_by == '-last-delivery':
            company_drivers = sorted(
                company_drivers, key=lambda i: i['last_delivery'], reverse = True)
        else:
            pass
        return company_drivers

    def convert_select_from_company_form(input, is_dlc, is_games):
        dlc_dictionary = {
            '1': 'Going East!',
            '2': 'Skandynawia',
            '3': 'Viva la France',
            '4': 'Italia',
            '5': 'Beyond the Baltic Sea',
            '6': 'Road to the Black Sea',
            '7': 'Iberia',
        }
        games_dictionary = {
            '1': 'ATS',
            '2': 'ETS2',
            '3': 'Singleplayer',
            '4': 'Multiplayer',
            '5': 'Promods',
        }
        if input is not None:
            translation = []
            if is_dlc:
                for number in input:
                    translation.append(dlc_dictionary.get(number, ""))
            elif is_games:
                for number in input:
                    translation.append(games_dictionary.get(number, ""))
            else:
                return "error"
            return translation
        else:
            return None

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
            company_id = company.id
            company = company.name
        else:
            company = None
            company_id = 0

        vehicle = Driver.get_vehicle_info(driver)

        try:
            avatar = driver.avatar.url
        except:
            avatar = ''

        driver_info = {
            'nick': driver.nick,
            'position': driver.position,
            'company': company,
            'company_id': company_id,
            'vehicle': vehicle,
            'avatar': driver.avatar.url,
            'is_employeed': driver.is_employeed,
        }
        return driver_info


    def set_driver_info(request):
        driver_info = Driver.get_driver_info_from_database(request.user)
        request.session['driver_info'] = driver_info

    def get_driver_info(request):
        Driver.set_driver_info(request)

        class DriverInfo(NamedTuple):
            nick: str
            position: str
            company: str
            vehicle: Vehicle
            avatar: str
            is_employeed: bool
        try:
            driver_info = request.session.get('driver_info')
        except driver_info is None:
            SetDriverInfo(request)
        finally:
            info = DriverInfo(
                driver_info['nick'],
                driver_info['position'],
                driver_info['company'],
                driver_info['vehicle'],
                driver_info['avatar'],
                driver_info['is_employeed'],
            )
        return info


class Vehicle(models.Model):
    id = models.AutoField(primary_key=True)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, null=True, blank=True)
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, null=True, blank=True)
    photo = models.ImageField(upload_to='vehicles', null=True, blank=True)
    model = models.CharField(max_length=80)
    cabin = models.CharField(max_length=64)
    registration_number = models.CharField(max_length=8)
    engine = models.CharField(max_length=100)
    engine_power = models.PositiveSmallIntegerField(default=0)
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
    reject_reason = models.TextField(default='', blank=True)
    to_edit_reason = models.TextField(default='', blank=True)

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
    id = models.AutoField(primary_key=True)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, default=None)
    first_disposition = models.ForeignKey(
        'Disposition', on_delete=models.CASCADE, related_name='first_disposition', default=None, null=True)
    second_disposition = models.ForeignKey(
        'Disposition', on_delete=models.CASCADE, related_name='second_disposition', default=None, null=True)
    third_disposition = models.ForeignKey(
        'Disposition', on_delete=models.CASCADE, related_name='third_disposition', default=None, null=True)
    fourth_disposition = models.ForeignKey(
        'Disposition', on_delete=models.CASCADE, related_name='fourth_disposition', default=None, null=True)
    fifth_disposition = models.ForeignKey(
        'Disposition', on_delete=models.CASCADE, related_name='fifth_disposition', default=None, null=True)

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
    deadline = models.DateTimeField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_rozpiska = models.BooleanField(default=False)
    # field for dispositions from rozpiska only
    finished = models.BooleanField(default=False)
    rozpiska = models.ForeignKey("Rozpiska", on_delete=models.CASCADE, default=None, blank=True, null=True)

    def __str__(self):
        return str(self.id)

class CompanySettings(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    class PeriodicNormType(models.TextChoices):
        WEEK = 'wk', _('Tydzień')
        MONTH = 'mth', _('Miesiąc')
    periodic_norm_type = models.CharField(
        choices=PeriodicNormType.choices, default=PeriodicNormType.WEEK, max_length=5)
    periodic_norm_distance = models.PositiveIntegerField(default=0)
    periodic_norm_start_date = models.DateTimeField(default=datetime.now())
    periodic_norm_end_date = models.DateTimeField(default=datetime.now())
    disposition_norm = models.IntegerField(default=0)
    disposition_norm_type = models.CharField(
        choices=PeriodicNormType.choices, default=PeriodicNormType.WEEK, max_length=5)
    random_vehicle = models.BooleanField(default=False)
    random_vehicle_type = models.CharField(choices=PeriodicNormType.choices, default=PeriodicNormType.WEEK, max_length=5)
    random_vehicle_timestamp = models.DateTimeField(auto_now_add=True)
    only_assistant = models.BooleanField(default=False)
    auto_synchronization = models.BooleanField(default=False)
    max_90 = models.BooleanField(default=False)

    def __str__(self):
        return str(self.company_id)

    def check_periodic_norm_distance(driver):
        settings = CompanySettings.objects.get(company=driver.company)
        distance_count = Waybill.objects.filter(driver=driver, finish_date__gte=settings.periodic_norm_start_date, finish_date__lte=settings.periodic_norm_end_date).aggregate(Sum('distance'))
        distance_count = distance_count.get('distance__sum')
        if distance_count is None:
            distance_count = 0
        return distance_count



class WorkApplications(models.Model):
    id = models.AutoField(primary_key=True)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(default='')

    def __str__(self):
        return str(self.id)

class Achievement(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    first_timer = models.BooleanField(default=True)
    eco_driver = models.BooleanField(default=False)
    long_distance_driver = models.BooleanField(default=False)
    heavy_driver = models.BooleanField(default=False)
