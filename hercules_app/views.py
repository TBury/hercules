import json
from datetime import datetime
from decimal import Decimal
from random import randint

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.encoding import smart_str

from hercules_app.forms import SetNickForm, FirstScreenshotForm, SecondScreenshotForm, AddWaybillForm, EditVehicleForm, \
    AddVehicleForm, EditSettingsForm, EditCompanyInformationForm, NewDispositionForm, NewOfferForm, SendApplicationForm, \
    AddNewCompanyForm
from hercules_app.models import (
    Driver,
    Company,
    DriverStatistics,
    Vehicle,
    Disposition,
    Waybill,
    Gielda,
    Rozpiska,
    Achievement,
    CompanySettings,
    WorkApplications,
    TruckersMPStatus, WaybillImages
)
from .tasks import get_waybill_info
from common.utils.utils import get_country, PROMODS_COMPANIES

def index(request):
    return render(request, 'hercules_app/index.html')


def login(request):
    return render(request, 'hercules_app/sign-in.html')

def handler404(request, exception):
    return render(request, 'hercules_app/404.html', status=404)

def handler500(request):
    return render(request, 'hercules_app/500.html', status=500)

def handler403(request, exception):
    return render(request, 'hercules_app/403.html', status=403)


@login_required(login_url="/login")
def hello(request):
    current_user = request.user
    form = SetNickForm()
    if request.method == "POST":
        form = SetNickForm(request.POST)
        if form.is_valid():
            nick = form.clean_nick()
            Driver.objects.filter(user=current_user).update(nick=nick)
            return redirect('panel')

    return render(request, 'hercules_app/hello.html', {"form": form})


@login_required(login_url="/login")
def panel(request):
    driver = Driver.objects.get(user=request.user)

    driver_info = Driver.get_driver_info(request)

    statistics = DriverStatistics.get_driver_statistics(driver)
    rozpiski = Rozpiska.objects.filter(driver=driver)
    dispositions = None
    if rozpiski is None:
        dispositions = Disposition.objects.filter(driver=driver, is_rozpiska=False, finished=False)[:3]
    if driver_info.company is not None:
        company = Company.objects.get(name=driver_info.company)
        periodic_norm_distance = CompanySettings.check_periodic_norm_distance(
            driver)
        periodic_norm = CompanySettings.objects.get(company=company)
        periodic_norm = periodic_norm.periodic_norm_distance
        realised = periodic_norm_distance >= periodic_norm
    else:
        periodic_norm_distance = None
        periodic_norm = None
        realised = None

    offers = Gielda.objects.all()[:5]
    for offer in offers:
        if offer.loading_spedition in PROMODS_COMPANIES:
            offer.loading_spedition = 'promods_company'
        if offer.unloading_spedition in PROMODS_COMPANIES:
            offer.unloading_spedition = 'promods_company'

    if dispositions is not None:
        for disposition in dispositions:
            if disposition.loading_spedition in PROMODS_COMPANIES:
                disposition.loading_spedition = 'promods_company'
            if disposition.unloading_spedition in PROMODS_COMPANIES:
                disposition.unloading_spedition = 'promods_company'


    status = TruckersMPStatus.get_status_from_database()
    CompanySettings.weekly_random_vehicles()

    args = {
        'nick': driver_info.nick,
        'avatar': driver_info.avatar,
        'company': driver_info.company,
        'statistics': statistics,
        'vehicle': driver_info.vehicle,
        'rozpiski': rozpiski,
        'dispositions': dispositions,
        'position': driver.position,
        'offers': offers,
        'periodic_norm_distance': periodic_norm_distance,
        'periodic_norm': periodic_norm,
        'realised': realised,
        'simulation1_players': status["simulation_1"],
        'simulation2_players': status["simulation_2"],
        'promods_players': status["promods"]
    }
    response = render(request, 'hercules_app/panel.html', args)

    waybill_success = request.session.get('waybill_success')
    if waybill_success is True:
        SetCookie(request, response, 'waybill_success')

    dispose_offer_success = request.session.get('dispose_offer_success')
    if dispose_offer_success is True:
        SetCookie(request, response, 'dispose_offer_success')
    job_application_accepted = request.session.get('job_application_accepted')
    if job_application_accepted is True:
        SetCookie(request, response, 'job_application_accepted')
    job_application_rejected = request.session.get('job_application_rejected')
    if job_application_rejected is True:
        SetCookie(request, response, 'job_application_rejected')
    return response


@login_required(login_url="/login")
def SetCookie(request, response, parameter_name):
    '''
    Set cookie for given parameter
    '''
    request.session.modified = True
    del request.session[parameter_name]
    response.set_cookie(parameter_name, 'True', max_age=5, samesite='Strict')
    return response


@login_required(login_url="/login")
def download_assistant(request):
    driver_info = Driver.get_driver_info(request)
    args = {
        'nick': driver_info.nick,
        'position': driver_info.position,
        'company': driver_info.company,
        'avatar': driver_info.avatar,
    }
    return render(request, 'hercules_app/download.html', args)


@login_required(login_url="/login")
def download_file(request):
    response = HttpResponse(content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(
        'assistant.zip')

    response['X-Sendfile'] = smart_str('assistant.zip')
    return response


@login_required(login_url="/login")
def drivers_card(request):
    driver = Driver.objects.get(user=request.user)

    driver_info = Driver.get_driver_info(request)

    statistics = DriverStatistics.get_driver_statistics(driver)
    achievements = Achievement.objects.get(driver=driver)
    waybills = Waybill.objects.filter(driver=driver)[:5]
    try:
        vehicle = Vehicle.objects.get(driver=driver)
    except Vehicle.DoesNotExist:
        vehicle = None
    args = {
        'nick': driver_info.nick,
        'avatar': driver_info.avatar,
        'position': driver_info.position,
        'company': driver_info.company,
        'statistics': statistics,
        'waybills': waybills,
        'vehicle': vehicle,
        'achievements': achievements,
    }
    return render(request, 'hercules_app/drivers-card.html', args)


@login_required(login_url="/login")
def add_delivery(request):
    driver_info = Driver.get_driver_info(request)
    args = {
        'nick': driver_info.nick,
        'position': driver_info.position,
        'company': driver_info.company,
        'avatar': driver_info.avatar,
    }
    return render(request, 'hercules_app/add_delivery.html', args)


@login_required(login_url="/login")
def send_first_screenshot(request):
    driver_info = Driver.get_driver_info(request)
    args = {
        'nick': driver_info.nick,
        'position': driver_info.position,
        'company': driver_info.company,
        'avatar': driver_info.avatar,
    }
    if request.method == 'POST':
        form = FirstScreenshotForm(request.POST, request.FILES)
        if form.is_valid():
            waybill = form.save()
            request.session['waybill_id'] = waybill.id
        else:
            form = FirstScreenshotForm()
    return render(request, 'hercules_app/automatic_1.html', args)


@login_required(login_url="/login")
def send_second_screenshot(request):
    is_automatic = request.session.get('waybill_automatic')
    if is_automatic is None:
        is_automatic = True
    else:
        is_automatic = False

    driver_info = Driver.get_driver_info(request)
    args = {
        'nick': driver_info.nick,
        'company': driver_info.company,
        'is_automatic': is_automatic,
        'position': driver_info.position,
        'avatar': driver_info.avatar,
    }
    waybill_id = request.session.get('waybill_id')
    # TODO: check if the waybill_id is passed correctly
    waybill = Waybill.objects.get(id=waybill_id)
    if request.method == "POST":
        form = SecondScreenshotForm(
            request.POST, request.FILES, instance=waybill)
        if form.is_valid():
            form.save()
    else:
        form = SecondScreenshotForm()
    return render(request, 'hercules_app/automatic_2.html', args)


@login_required(login_url="/login")
def loading_page(request):
    driver_info = Driver.get_driver_info(request)
    args = {
        'nick': driver_info.nick,
        'company': driver_info.company,
        'position': driver_info.position,
        'avatar': driver_info.avatar,
    }
    return render(request, 'hercules_app/loading.html', args)


@login_required(login_url="/login")
def manual_step_one(request):
    waybill = Waybill()
    waybill.save()
    request.session['waybill_id'] = waybill.id
    request.session['waybill_automatic'] = False
    return send_second_screenshot(request)


@login_required(login_url="/login")
def process_waybill(request):
    waybill_id = request.session.get('waybill_id')
    try:
        waybill = Waybill.objects.get(id=waybill_id)
        info = get_waybill_info.delay(waybill.first_screen.file.name,
                                  waybill.end_screen.file.name, waybill.id)
        args = info.get()
        if args is not None:
            request.session['screen_information'] = args

            return HttpResponse(status=200)
    except Waybill.DoesNotExist:
        return HttpResponse(status=500)


@login_required(login_url="/login")
def add_waybill(request):
    is_automatic = True
    driver = Driver.objects.get(user=request.user)
    driver_info = Driver.get_driver_info(request)

    waybill_id = request.session.get('waybill_id')
    waybill = Waybill.objects.get(id=waybill_id)
    if waybill.first_screen.name == "":
        is_automatic = False
    else:
        args = request.session.get('screen_information')
        images = WaybillImages.objects.get(waybill=waybill)

    if request.method == "POST":
        form = AddWaybillForm(request.POST, instance=waybill)
        if form.is_valid():
            waybill = form.save(commit=False)
            waybill.driver = driver
            waybill.loading_spedition = str(waybill.loading_spedition).lower()
            waybill.unloading_spedition = str(waybill.unloading_spedition).lower()
            waybill.loading_country = get_country(waybill.loading_city)
            waybill.unloading_country = get_country(waybill.unloading_city)
            waybill.save()
            try:
                Disposition.objects.filter(
                    driver=driver,
                    loading_city=waybill.loading_city,
                    loading_spedition=waybill.loading_spedition,
                    unloading_city=waybill.unloading_city,
                    unloading_spedition=waybill.unloading_spedition,
                    cargo=waybill.cargo,
                    tonnage=waybill.tonnage,
                ).delete()
            except:
                pass
            if driver.is_employeed == False:
                statistics = DriverStatistics.objects.get(driver_id=driver)
                DriverStatistics.objects.filter(driver_id=driver).update(
                    distance=statistics.distance + int(form.cleaned_data['distance']),
                    tonnage=statistics.tonnage + int(form.cleaned_data['tonnage']),
                    income=statistics.income + int(form.cleaned_data['income']),
                    fuel=statistics.income + int(form.cleaned_data['fuel']),
                    average_fuel=round(Decimal(statistics.fuel + int(form.cleaned_data['fuel'])) / Decimal(
                        statistics.distance + int(form.cleaned_data['distance'])) * 100, 2),
                    deliveries_count=statistics.deliveries_count + 1,
                )
                Waybill.objects.filter(id=waybill_id).update(
                    status="accepted")
            request.session.modified = True
            request.session['waybill_success'] = True
            del request.session['waybill_id']
            del request.session['waybill_information']
            return redirect('panel')
    else:
        if is_automatic:
            form = AddWaybillForm(initial={
                'loading_city': args['loading_city'],
                'loading_spedition': args['loading_spedition'],
                'unloading_city': args['unloading_city'],
                'unloading_spedition': args['unloading_spedition'],
                'cargo': args['cargo'],
                'fuel': args['fuel'],
                'tonnage': args['tonnage'],
                'distance': args['distance'],
                'income': args['income'],
            })
        else:
            form = AddWaybillForm()

    args = {
        'nick': driver_info.nick,
        'position': driver_info.position,
        'company': driver_info.company,
        'avatar': driver_info.avatar,
        'form': form,
        'is_automatic': is_automatic,
        'images': images
    }
    return render(request, 'hercules_app/verify.html', args)


@login_required(login_url="/login")
def OffersView(request):
    if request.session.get('offer_id') is not None:
        del request.session['offer_id']
    driver_info = Driver.get_driver_info(request)

    parameters = ['loading_city', 'loading_country',
                  'unloading_city', 'unloading_country']
    filters = {}
    for parameter in parameters:
        if request.GET.get(parameter):
            filters[parameter] = request.GET.get(parameter)
    income_min = 0
    income_max = 1000000
    sort_by = '-id'
    if request.GET.get('income_min'):
        income_min = int(request.GET.get('income_min'))
    if request.GET.get('income_max'):
        income_max = int(request.GET.get('income_max'))
    if request.GET.get('sort_by'):
        sort_by = request.GET.get('sort_by')
    offers = Gielda.objects.all().filter(**filters, price__gte=income_min,
                                         price__lte=income_max).order_by(sort_by)
    for offer in offers:
        if offer.loading_spedition in PROMODS_COMPANIES:
            offer.loading_spedition = 'promods_company'
        if offer.unloading_spedition in PROMODS_COMPANIES:
            offer.unloading_spedition = 'promods_company'

    args = {
        'nick': driver_info.nick,
        'company': driver_info.company,
        'avatar': driver_info.avatar,
        'position': driver_info.position,
        'offers': offers,
        'sort_by': sort_by
    }
    response = render(request, 'hercules_app/gielda.html', args)

    if request.session.get("offer_added") == True:
        SetCookie(request, response, 'offer_added')
    return response


@login_required(login_url="/login")
def OfferDetailsView(request, offer_id):
    driver_info = Driver.get_driver_info(request)
    offer = Gielda.objects.get(id=offer_id)
    if offer.loading_spedition in PROMODS_COMPANIES:
        offer.loading_spedition = 'promods_company'
    if offer.unloading_spedition in PROMODS_COMPANIES:
        offer.unloading_spedition = 'promods_company'
    driver = Driver.objects.get(nick=driver_info.nick)
    try:
        company_drivers_count = Company.objects.values_list(
            'drivers_count', flat=True).get(name=driver_info.company)
    except:
        company_drivers_count = 1
    is_self_employeed = False
    request.session['offer_id'] = offer_id
    if company_drivers_count == 1:
        is_self_employeed = True
    args = {
        'nick': driver_info.nick,
        'id': driver.id,
        'company': driver_info.company,
        'avatar': driver_info.avatar,
        'position': driver_info.position,
        'offer': offer,
        'is_self_employeed': is_self_employeed
    }
    return render(request, 'hercules_app/offer_details.html', args)

@login_required(login_url="/login")
def CreateOfferView(request):
    driver_info = Driver.get_driver_info(request)
    if request.POST:
        form = NewOfferForm(data=request.POST)
        if form.is_valid():
            offer = form.save(commit=False)
            offer.loading_country = get_country(offer.loading_city)
            offer.unloading_country = get_country(offer.unloading_city)
            offer.save()
            request.session['offer_added'] = True
            return redirect('/Gielda/Offers')
        else:
            form = NewOfferForm()
            args = {
                'nick': driver_info.nick,
                'company': driver_info.company,
                'avatar': driver_info.avatar,
                'position': driver_info.position,
                'form': form
            }
            return render(request, 'hercules_app/create_offer.html', args)
    else:
        form = NewOfferForm()
        args = {
            'nick': driver_info.nick,
            'company': driver_info.company,
            'avatar': driver_info.avatar,
            'position': driver_info.position,
            'form': form
        }
        return render(request, 'hercules_app/create_offer.html', args)


@login_required(login_url="/login")
def ChooseDriverView(request):
    driver_info = Driver.get_driver_info(request)
    company_drivers_count = Company.objects.values_list(
        'drivers_count', flat=True).get(name=driver_info.company)
    if company_drivers_count > 1:
        company = Company.objects.get(name=driver_info.company)
        company_drivers = Driver.objects.all().filter(id=company.id)
        company_drivers_vehicles = []
        for company_driver in company_drivers:
            try:
                company_drivers_vehicles.append(
                    Vehicle.objects.get(driver=company_driver)
                )
            except Vehicle.DoesNotExist:
                pass

        args = {
            'nick': driver_info.nick,
            'company': driver_info.company,
            'avatar': driver_info.avatar,
            'position': driver_info.position,
            'drivers': company_drivers,
            'vehicles': company_drivers_vehicles
        }
        return render(request, 'hercules_app/offer_dispose.html', args)
    else:
        return HttpResponse(status=500)


@login_required(login_url="/login")
def DisposeOffer(request, driver_id):
    offer_id = request.session.get('offer_id')
    offer = Gielda.objects.get(id=offer_id)
    del request.session['offer_id']
    Disposition.objects.create(
        loading_city=offer.loading_city,
        loading_country=offer.unloading_country,
        loading_spedition=offer.loading_spedition,
        unloading_city=offer.unloading_city,
        unloading_country=offer.unloading_country,
        unloading_spedition=offer.unloading_spedition,
        cargo=offer.cargo,
        tonnage=offer.tonnage,
        driver=Driver.objects.get(id=driver_id)
    )
    request.session['dispose_offer_success'] = True
    Gielda.objects.get(id=offer_id).delete()
    return redirect('panel')


@login_required(login_url="/login")
def ShowDispositionsView(request):
    driver_info = Driver.get_driver_info(request)
    driver = Driver.objects.get(user=request.user)
    dispositions = Disposition.objects.all().filter(
        driver=driver).exclude(is_rozpiska=True)
    for disposition in dispositions:
        if disposition.loading_spedition in PROMODS_COMPANIES:
            disposition.loading_spedition = 'promods_company'
        if disposition.unloading_spedition in PROMODS_COMPANIES:
            disposition.unloading_spedition = 'promods_company'
    rozpiski = Rozpiska.objects.all().filter(driver=driver)
    args = {
        'nick': driver_info.nick,
        'company': driver_info.company,
        'avatar': driver_info.avatar,
        'position': driver_info.position,
        'dispositions': dispositions,
        'rozpiski': rozpiski
    }
    return render(request, 'hercules_app/dispositions.html', args)


@login_required(login_url="/login")
def FindCompanyView(request):
    driver_info = Driver.get_driver_info(request)
    companies = Company.objects.all().order_by('is_recruiting')
    args = {
        'nick': driver_info.nick,
        'company': driver_info.company,
        'position': driver_info.position,
        'avatar': driver_info.avatar,
        'companies': companies
    }
    return render(request, 'hercules_app/find_company.html', args)


@login_required(login_url="/login")
def CompanyDetailsView(request, company_id):
    driver_info = Driver.get_driver_info(request)
    company = Company.objects.get(id=company_id)
    args = {
        'nick': driver_info.nick,
        'avatar': driver_info.avatar,
        'position': driver_info.position,
        'company': company
    }
    return render(request, 'hercules_app/company_profile.html', args)


@login_required(login_url="/login")
def CompanyVehiclesView(request):
    driver_info = Driver.get_driver_info(request)
    if driver_info.company is not None:
        company_id = Company.objects.only(
            'id').filter(name=driver_info.company)
        vehicles = Vehicle.objects.all().filter(
            company=company_id[0])  # querysets are lazy
    else:
        driver = Driver.objects.get(nick=driver_info.nick)
        vehicles = Vehicle.objects.all().filter(driver=driver)
    args = {
        'nick': driver_info.nick,
        'avatar': driver_info.avatar,
        'company': driver_info.company,
        'position': driver_info.position,
        'vehicles': vehicles
    }
    response = render(request, 'hercules_app/vehicles.html', args)

    is_edited = request.session.get('vehicle_edited')
    if is_edited:
        SetCookie(request, response, 'vehicle_edited')
    is_added = request.session.get('vehicle_added')
    if is_added:
        SetCookie(request, response, 'vehicle_added')
    is_removed = request.session.get('vehicle_deleted')
    if is_removed:
        SetCookie(request, response, 'vehicle_deleted')

    return response


@login_required(login_url="/login")
def VehicleDetailsView(request, vehicle_id):
    driver_info = Driver.get_driver_info(request)
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    driver = Driver.objects.get(nick=driver_info.nick)
    if driver_info.company != vehicle.company or driver_info.company is None:
        return HttpResponse(status=403)
    else:
        if driver_info.company is not None:
            company_id = Company.objects.only(and
                'id').filter(name=driver_info.company)
            company_drivers = Driver.objects.only(
                'nick').filter(company=company_id[0])
            drivers_dict = {}
            for company_driver in company_drivers:
                drivers_dict[company_driver.id] = company_driver.nick
                drivers = tuple(drivers_dict.items())
        else:
            driver_dict = {driver.id: driver.nick}
            drivers = tuple(driver_dict.items())
        current_driver = vehicle.driver.id
        form = EditVehicleForm(drivers, current_driver, initial={
            'brand': vehicle.brand,
            'model': vehicle.model,
            'cabin': vehicle.cabin,
            'engine': vehicle.engine,
            'engine_power': vehicle.engine_power,
            'gearbox': vehicle.gearbox,
            'wheelbase': vehicle.wheelbase,
            'wheels': vehicle.wheels,
            'odometer': vehicle.odometer,
            'driver': current_driver,
        })
        if request.method == "POST":
            form = EditVehicleForm(drivers, current_driver,
                                   request.POST, request.FILES, instance=vehicle)
            if form.is_valid():
                new_driver = Driver.objects.get(id=form.cleaned_data.get("driver"))
                form = form.save(commit=False)
                Vehicle.objects.update(
                    driver=None,
                    old_driver=vehicle.driver
                )
                form.driver = new_driver
                form.last_driver = Driver.objects.get(id=current_driver)

                form.save()
                request.session['vehicle_edited'] = True
                return redirect('/Vehicles')
        else:
            form = EditVehicleForm(drivers, current_driver, initial={
                'brand': vehicle.brand,
                'model': vehicle.model,
                'cabin': vehicle.cabin,
                'engine': vehicle.engine,
                'engine_power': vehicle.engine_power,
                'gearbox': vehicle.gearbox,
                'wheelbase': vehicle.wheelbase,
                'wheels': vehicle.wheels,
                'odometer': vehicle.odometer,
            })
    args = {
        'nick': driver_info.nick,
        'avatar': driver_info.avatar,
        'company': driver_info.company,
        'position': driver_info.position,
        'form': form,
        'vehicle': vehicle
    }
    return render(request, 'hercules_app/vehicle_details.html', args)


@login_required(login_url="/login")
def AddNewVehicleView(request):
    driver_info = Driver.get_driver_info(request)
    if driver_info.company is not None:
        company_id = Company.objects.only(
            'id').filter(name=driver_info.company)
        company_drivers = Driver.objects.only(
            'nick').filter(company=company_id[0])
        drivers_dict = {}
        for company_driver in company_drivers:
            drivers_dict[company_driver.id] = company_driver.nick
            drivers = tuple(drivers_dict.items())
            form = AddVehicleForm(drivers)
    else:
        driver = Driver.objects.get(nick=driver_info.nick)
        driver_dict = {driver.id: driver.nick}
        drivers = tuple(driver_dict.items())
        form = AddVehicleForm(drivers)
    if request.method == "POST":
        form = AddVehicleForm(drivers, request.POST, request.FILES)
        if form.is_valid():
            vehicle = form.save(commit=False)
            if driver_info.company is not None:
                company = Company.objects.get(name=driver_info.company)
                vehicle.company = company
            vehicle.driver = Driver.objects.get(id=form.cleaned_data['driver'])
            vehicle.last_driver= Driver.objects.get(id=form.cleaned_data.get("driver"))
            vehicle.save()
            request.session['vehicle_added'] = True
            return redirect('/Vehicles')
        else:
            form = AddVehicleForm(drivers)
    args = {
        'nick': driver_info.nick,
        'avatar': driver_info.avatar,
        'position': driver_info.position,
        'company': driver_info.company,
        'form': form
    }
    return render(request, 'hercules_app/add_vehicle.html', args)

@login_required(login_url="/login")
def ShowDeliveriesView(request):
    driver_info = Driver.get_driver_info(request)
    driver = Driver.objects.get(nick=driver_info.nick)
    deliveries = Waybill.objects.all().order_by(
        '-finish_date').filter(driver=driver)
    args = {
        'nick': driver_info.nick,
        'avatar': driver_info.avatar,
        'position': driver_info.position,
        'company': driver_info.company,
        'deliveries': deliveries
    }

    return render(request, 'hercules_app/deliveries.html', args)

@login_required(login_url="/login")
def ShowDeliveryDetailsView(request, waybill_id):
    driver_info = Driver.get_driver_info(request)
    delivery = Waybill.objects.get(id=waybill_id)
    if delivery.status == 'to-edit':
        form = AddWaybillForm(initial={
            'loading_city': delivery.loading_city,
            'loading_spedition': delivery.loading_spedition,
            'unloading_city': delivery.unloading_city,
            'unloading_spedition': delivery.unloading_spedition,
            'cargo': delivery.cargo,
            'fuel': delivery.fuel,
            'tonnage': delivery.tonnage,
            'distance': delivery.distance,
            'income': delivery.income,
        })
        args = {
            'nick': driver_info.nick,
            'avatar': driver_info.avatar,
            'company': driver_info.company,
            'position': driver_info.position,
            'form': form,
            'delivery': delivery
        }
        return render(request, 'hercules_app/delivery_details.html', args)
    else:
        args = {
            'nick': driver_info.nick,
            'avatar': driver_info.avatar,
            'company': driver_info.company,
            'position': driver_info.position,
            'delivery': delivery
        }
        return render(request, 'hercules_app/delivery_details.html', args)

@login_required(login_url="/login")
def EditWaybill(request, waybill_id):
    if request.POST:
        waybill = Waybill.objects.get(id=waybill_id)
        form = AddWaybillForm(request.POST, instance=waybill)
        if form.is_valid():
            new_waybill = form.save(commit=False)
            new_waybill.status = 'not-checked'
            new_waybill.finish_date = datetime.now
            new_waybill.save()
            request.session.modified = True
            request.session['waybill_success'] = True
            return redirect('panel')
    else:
        return HttpResponse(status=500)

@login_required(login_url="/login")
def DeleteVehicle(request, vehicle_id):
    if request.POST:
        Vehicle.objects.filter(id=vehicle_id).delete()
        request.session.modified = True
        request.session['vehicle_deleted'] = True
        return redirect('/Vehicles')
    else:
        return HttpResponse(status=500)

@login_required(login_url="/login")
def ShowCompanyProfileView(request):
    driver_info = Driver.get_driver_info(request)
    if driver_info.company is not None:
        company = Company.objects.get(name=driver_info.company)
        args = {
            'nick': driver_info.nick,
            'avatar': driver_info.avatar,
            'position': driver_info.position,
            'company': company,
            'is_employeed': driver_info.is_employeed,
        }
        return render(request, 'hercules_app/company_profile.html', args)
    else:
        return HttpResponse(status=500)

@login_required(login_url="/login")
def ShowCompanyDriversView(request):
    driver_info = Driver.get_driver_info(request)

    changed_position = request.session.get('changed-position')
    if driver_info.company is not None:
        company = Company.objects.get(name=driver_info.company)
        sort_type = request.GET.get('sort_by')
        if sort_type is not None:
            company_drivers = Company.get_company_drivers_info(
                company.id, sort_type)
        else:
            company_drivers = Company.get_company_drivers_info(
                '-position', company.id)
        driver_nick = request.GET.get('driver_nick')
        if driver_nick is not None:
            for company_driver in company_drivers:
                if company_driver['nick'] == driver_nick:
                    args = {
                        'nick': driver_info.nick,
                        'position': driver_info.position,
                        'avatar': driver_info.avatar,
                        'company': driver_info.company,
                        'company_driver': company_driver
                    }
                    response = render(request, 'hercules_app/drivers.html', args)
                    break
                else:
                    args = {
                        'nick': driver_info.nick,
                        'position': driver_info.position,
                        'avatar': driver_info.avatar,
                        'company': driver_info.company,
                        'not_found': True,
                        'sort_by': sort_type
                    }
                    response = render(request, 'hercules_app/drivers.html',
                                      args)
        else:
            args = {
                'nick': driver_info.nick,
                'position': driver_info.position,
                'avatar': driver_info.avatar,
                'company': driver_info.company,
                'company_drivers': company_drivers,
                'sort_by': sort_type
            }
            response = render(request, 'hercules_app/drivers.html', args)
        if changed_position is True:
            SetCookie(request, response, 'changed-position')
        return response

@login_required(login_url="/login")
def ShowCompanyDriverView(request, driver_id):
    driver_info = Driver.get_driver_info(request)
    current_driver = Driver.objects.get(nick=driver_info.nick)
    company_driver = Driver.objects.get(id=driver_id)
    if company_driver == current_driver:
        return redirect('/drivers-card')
    statistics = DriverStatistics.get_driver_statistics(company_driver)
    achievements = Achievement.objects.get(driver=company_driver)
    waybills = Waybill.objects.filter(driver=company_driver)[:5]

    if company_driver.company.name == driver_info.company and current_driver.position == 'Szef':
        is_chef = True
    else:
        is_chef = False

    args = {
        'nick': driver_info.nick,
        'avatar': driver_info.avatar,
        'company': driver_info.company,
        'company_driver_id': company_driver.id,
        'company_driver_nick': company_driver.nick,
        'company_driver_position': company_driver.position,
        'company_driver_company': company_driver.company,
        'statistics': statistics,
        'achievements': achievements,
        'waybills': waybills,
        'position': driver_info.position,
        'is_chef': is_chef,
        'is_company_driver': True,
    }

    return render(request, 'hercules_app/drivers-card.html', args)

@login_required(login_url="/login")
def ChangePosition(request, driver_id):
    if request.POST:
        company_driver = Driver.objects.get(id=driver_id)
        new_position = request.POST['change-position']
        company_driver.position = new_position
        company_driver.save()
        request.session['changed-position'] = True
        return redirect('/Company/Drivers')
    else:
        return HttpResponse(status=403)

@login_required(login_url="/login")
def DismissDriver(request, driver_id):
    if request.POST:
        driver = Driver.objects.get(user=request.user)
        if driver.position != "Szef":
            return HttpResponse(status=403)
        else:
            company_driver = Driver.objects.get(id=driver_id)
            company = company_driver.company
            company_driver.company = None
            company_driver.is_employeed = False
            company_driver.position = None
            company_driver.save()
            company.drivers_count -= 1
            company.save()
            request.session['dismissed-driver'] = True
            return redirect('/Company/Drivers')
    else:
        return HttpResponse(status=403)

@login_required(login_url="/login")
def CompanyWaybillsView(request):
    driver_info = Driver.get_driver_info(request)
    company = Company.objects.get(name=driver_info.company)
    drivers = Driver.objects.all().filter(company=company)
    company_deliveries = []
    for company_driver in drivers:
        deliveries = Waybill.objects.all().order_by(
            '-finish_date').filter(driver=company_driver)
        for delivery in deliveries:
            company_deliveries.append(delivery)
    company_deliveries = sorted(
        company_deliveries, key=lambda x: x.finish_date)
    company_deliveries = reversed(company_deliveries)
    args = {
        'nick': driver_info.nick,
        'position': driver_info.position,
        'avatar': driver_info.avatar,
        'company': driver_info.company,
        'deliveries': company_deliveries,
        'is_speditor_view': True
    }
    response = render(request, 'hercules_app/deliveries.html',
                      args)
    waybill_accepted = request.session.get('waybill_accepted')
    if waybill_accepted is True:
        SetCookie(request, response, 'waybill_accepted')
    waybill_to_edit = request.session.get('waybill_to_edit')
    if waybill_to_edit is True:
        SetCookie(request, response, 'waybill_to_edit')
    waybill_rejected = request.session.get('waybill_rejected')
    if waybill_rejected is True:
        SetCookie(request, response, 'waybill_rejected')
    return response

@login_required(login_url="/login")
def VerifyWaybillView(request, waybill_id):
    driver_info = Driver.get_driver_info(request)
    waybill = Waybill.objects.get(id=waybill_id)
    images = WaybillImages.objects.get(waybill=waybill)
    args = {
        'nick': driver_info.nick,
        'position': driver_info.position,
        'avatar': driver_info.avatar,
        'company': driver_info.company,
        'waybill': waybill,
        'images': images,
    }
    return render(request, 'hercules_app/verify_waybill.html', args)

@login_required(login_url="/login")
def AcceptWaybill(request, waybill_id):
    if request.GET:
        return HttpResponse(status=403)
    else:
        driver_info = Driver.get_driver_info(request)
        if (driver_info.position == "Szef" or driver_info.position == "Spedytor"):
            waybill = Waybill.objects.get(id=waybill_id)
            driver = waybill.driver
            if driver.company.name != driver_info.company:
                return HttpResponse(status=403)
            else:
                waybill.status = "accepted"
                waybill.save()
                driver_statistics = DriverStatistics.objects.get(
                    driver_id=driver)
                DriverStatistics.objects.filter(driver_id=driver).update(
                    distance=driver_statistics.distance + waybill.distance,
                    tonnage=driver_statistics.tonnage + waybill.tonnage,
                    income=driver_statistics.income + waybill.income,
                    fuel=driver_statistics.fuel + waybill.fuel,
                    average_fuel=round(Decimal(driver_statistics.fuel + waybill.fuel) / Decimal(
                        driver_statistics.distance + waybill.distance) * 100, 2),
                    deliveries_count=driver_statistics.deliveries_count + 1,
                )
                company = Company.objects.filter(name=driver_info.company)
                Company.objects.filter(name=driver_info.company).update(
                    distance=company.distance + waybill.distance,
                    tonnage=company.tonnage + waybill.tonnage,
                    income=company.income + waybill.income,
                    fuel=company.fuel + waybill.fuel,
                    average_fuel=round(Decimal(company.fuel + waybill.fuel) / Decimal(
                        company.distance + waybill.distance) * 100, 2),
                    waybill_count=company.deliveries_count + 1,
                )
                request.session['waybill_accepted'] = True
                return redirect('/Waybills')
        else:
            return HttpResponse(status=403)

@login_required(login_url="/login")
def ToEditWaybill(request, waybill_id):
    if request.GET:
        return HttpResponse(status=403)
    else:
        driver_info = Driver.get_driver_info(request)
        if (driver_info.position == "Szef" or driver_info.position == "Spedytor"):
            waybill = Waybill.objects.get(id=waybill_id)
            driver = waybill.driver
            if driver.company.name != driver_info.company:
                return HttpResponse(status=403)
            else:
                waybill.status = "to-edit"
                waybill.to_edit_reason = request.POST['to-edit-reason']
                waybill.save()
                request.session['waybill_to_edit'] = True
                return redirect('/Waybills')
        else:
            return HttpResponse(status=403)

@login_required(login_url="/login")
def RejectWaybill(request, waybill_id):
    if request.GET:
        return HttpResponse(status=403)
    else:
        driver_info = Driver.get_driver_info(request)
        if (driver_info.position == "Szef" or driver_info.position == "Spedytor"):
            waybill = Waybill.objects.get(id=waybill_id)
            driver = waybill.driver
            if driver.company.name != driver_info.company:
                return HttpResponse(status=403)
            else:
                waybill.status = "declined"
                waybill.to_edit_reason = request.POST['reject-reason']
                waybill.save()
                request.session['waybill_rejected'] = True
                return redirect('/Waybills')
        else:
            return HttpResponse(status=403)
@login_required(login_url="/login")
def AddNewCompanyView(request):
    driver_info = Driver.get_driver_info(request)
    if (driver_info.position is None):
        add_company_form = AddNewCompanyForm()
        args = {
            'nick': driver_info.nick,
            'position': driver_info.position,
            'avatar': driver_info.avatar,
            'form': add_company_form
        }
        response = render(request, 'hercules_app/add_company.html',
                          args)
        return response
    else:
        return HttpResponse(status=403)
@login_required(login_url="/login")
def AddCompany(request):
    if request.GET:
        return HttpResponse(status=403)
    else:
        driver_info = Driver.get_driver_info(request)
        if driver_info.position is None:
            form = AddNewCompanyForm(request.POST, request.FILES)
            if form.is_valid():
                company = form.save(commit=False)
                dlc = form.cleaned_data.get("dlc")
                games = Company.convert_select_from_company_form(form.cleaned_data.get("games"), False, True)
                if games is not None:
                    for game in games:
                        if game == "ETS2":
                            company.is_ets2 = True
                        elif game == "ATS":
                            company.is_ats = True
                        elif game == "Singleplayer":
                            company.is_singleplayer = True
                        elif game == "Multiplayer":
                            company.is_multiplayer = True
                        elif game == "Promods":
                            company.is_ats = True
                company.dlc = dlc
                company.is_recruiting = form.cleaned_data.get("is_recruiting")
                company.save()
                driver = Driver.objects.get(nick=driver_info.nick)
                driver.company = Company.objects.get(name=form.cleaned_data.get("name"))
                driver.position = "Szef"
                driver.is_employeed = True
                driver.save()
                settings = CompanySettings()
                settings.company = Company.objects.get(name=form.cleaned_data.get("name"))
                settings.save()
                return redirect('/panel')
            else:
                return redirect('/Companies')
        else:
            return HttpResponse(status=403)
@login_required(login_url="/login")
def CompanySettingsView(request):
    driver_info = Driver.get_driver_info(request)
    if (driver_info.position == "Szef"):
        company = Company.objects.get(name=driver_info.company)
        settings = CompanySettings.objects.get(company=company)
        edit_company_form = EditCompanyInformationForm(
            company.is_recruiting, instance=company)
        edit_company_settings_form = EditSettingsForm(settings.random_vehicle, settings.auto_synchronization,
                                                      settings.only_assistant, settings.max_90, instance=settings)
        args = {
            'nick': driver_info.nick,
            'position': driver_info.position,
            'avatar': driver_info.avatar,
            'company': company,
            'edit_company_form': edit_company_form, 'edit_company_settings_form': edit_company_settings_form,
        }
        response = render(request, 'hercules_app/settings.html',
                          args)
        information_changed = request.session.get('information_changed')
        if information_changed is True:
            SetCookie(request, response, 'information_changed')
        settings_changed = request.session.get('settings_changed')
        if settings_changed is True:
            SetCookie(request, response, 'settings_changed')
        games = ""
        if company.is_ats:
            games += "1"
        if company.is_ets2:
            games += "2"
        if company.is_singleplayer:
            games += "3"
        if company.is_multiplayer:
            games += "4"
        if company.is_promods:
            games += "5"
        response.set_cookie('dlc', company.dlc, max_age=5, samesite='Strict')
        response.set_cookie('games', games, max_age=5, samesite='Strict')
        return response
    else:
        return HttpResponse(status=403)

@login_required(login_url="/login")
def EditCompanyInformation(request):
    if request.GET:
        return HttpResponse(status=503)
    else:
        driver_info = Driver.get_driver_info(request)
        if (driver_info.position == "Szef"):
            company = Company.objects.get(name=driver_info.company)
            form = EditCompanyInformationForm(
                company.is_recruiting, request.POST, request.FILES, instance=company)
            if form.is_valid():
                information = form.save(commit=False)
                dlc = form.cleaned_data.get("dlc")
                games = Company.convert_select_from_company_form(form.cleaned_data.get("games"), False, True)
                if games is not None:
                    for game in games:
                        if game == "ETS2":
                            information.is_ets2 = True
                        elif game == "ATS":
                            information.is_ats = True
                        elif game == "Singleplayer":
                            information.is_singleplayer = True
                        elif game == "Multiplayer":
                            information.is_multiplayer = True
                        elif game == "Promods":
                            information.is_ats = True
                information.dlc = dlc
                information.save()
                request.session['information_changed'] = True
                return redirect('/Settings')
            else:
                return redirect('/Settings')
        else:
            return HttpResponse(status=403)

@login_required(login_url="/login")
def EditCompanySettings(request):
    if request.GET:
        return HttpResponse(status=403)
    else:
        driver_info = Driver.get_driver_info(request)
        if driver_info.position == "Szef":
            company = Company.objects.get(name=driver_info.company)
            settings = CompanySettings.objects.get(company=company)
            form = EditSettingsForm(settings.random_vehicle, settings.auto_synchronization, settings.only_assistant,
                                    settings.max_90, request.POST, instance=settings)
            if form.is_valid():
                form.save()
                request.session['settings_changed'] = True
                return redirect('/Company/Settings')
            else:
                return redirect('/Company/Settings')
        else:
            return HttpResponse(status=403)

@login_required(login_url="/login")
def DeleteCompany(request):
    if request.GET:
        return HttpResponse(status=403)
    else:
        driver_info = Driver.get_driver_info(request)
        if driver_info.position == "Szef" or driver_info.position == "Spedytor":
            company = Company.objects.get(name=driver_info.company)
            if company.name != driver_info.company:
                return HttpResponse(status=403)
            else:
                drivers = Driver.objects.filter(company=company)
                for driver in drivers:
                    Driver.objects.filter(nick=driver.nick).update(is_employeed=False, company=None, position=None)
                Vehicle.objects.filter(company=company).delete()
                CompanySettings.objects.filter(company=company).delete()
                WorkApplications.objects.filter(company=company).delete()
                Company.objects.filter(name=driver_info.company).delete()
                return redirect('/panel')
        else:
            return HttpResponse(status=403)


@login_required(login_url="/login")
def ShowCompanyDispositionsView(request):
    driver_info = Driver.get_driver_info(request)
    company = Company.objects.get(name=driver_info.company)
    company_drivers_count = Company.objects.values_list(
        'drivers_count', flat=True).get(name=company.name)
    company_dispositions = []
    company_rozpiski = []
    if company_drivers_count >= 1:
        company_drivers = Driver.objects.all().filter(company=company)
        for company_driver in company_drivers:
            dispositions = Disposition.objects.filter(
                driver=company_driver).exclude(is_rozpiska=True)
            if dispositions:
                company_dispositions.append(dispositions)
                for disposition in dispositions:
                    if disposition.loading_spedition in PROMODS_COMPANIES:
                        disposition.loading_spedition = 'promods_company'
                    if disposition.unloading_spedition in PROMODS_COMPANIES:
                        disposition.unloading_spedition = 'promods_company'
            rozpiski = Rozpiska.objects.filter(driver=company_driver)
            if rozpiski:
                company_rozpiski.append(rozpiski)
    args = {
        'nick': driver_info.nick,
        'position': driver_info.position,
        'avatar': driver_info.avatar,
        'company': driver_info.company,
        'dispositions': company_dispositions,
        'rozpiski': company_rozpiski
    }
    return render(request, 'hercules_app/dispositions_chef.html', args)

@login_required(login_url="/login")
def ChooseDispositionView(request):
    driver_info = Driver.get_driver_info(request)
    args = {
        'nick': driver_info.nick,
        'position': driver_info.position,
        'avatar': driver_info.avatar,
        'company': driver_info.company,
    }
    return render(request, 'hercules_app/choose_disposition_type.html', args)

@login_required(login_url="/login")
def CreateNewDispositionView(request):
    driver_info = Driver.get_driver_info(request)
    if driver_info.company is not None:
        company_id = Company.objects.only(
            'id').filter(name=driver_info.company)
        company_drivers = Driver.objects.only(
            'nick').filter(company=company_id[0])
        drivers_dict = {}
        for company_driver in company_drivers:
            drivers_dict[company_driver.id] = company_driver.nick
            drivers = tuple(drivers_dict.items())
    else:
        return HttpResponse(status=500)
    if request.POST:
        form = NewDispositionForm(drivers, data=request.POST)
        if form.is_valid():
            disposed_driver = Driver.objects.get(id=request.POST['driver'])
            disposition = form.save(commit=False)
            disposition.loading_country = get_country(disposition.loading_city)
            disposition.driver = disposed_driver
            disposition.save()
            request.session['created_disposition'] = True
            return redirect('/Company/Dispositions')
        else:
            form = NewDispositionForm(drivers)
            args = {
                'nick': driver_info.nick,
                'position': driver_info.position,
                'avatar': driver_info.avatar,
                'company': driver_info.company,
                'form': form
            }
            return render(request, 'hercules_app/create_disposition.html', args)
    else:
        form = NewDispositionForm(drivers)
        args = {
            'nick': driver_info.nick,
            'position': driver_info.position,
            'avatar': driver_info.avatar,
            'company': driver_info.company,
            'form': form
        }
        return render(request, 'hercules_app/create_disposition.html', args)

@login_required(login_url="/login")
def CreateNewRozpiskaView(request):
    driver_info = Driver.get_driver_info(request)
    if driver_info.company is not None:
        company_id = Company.objects.only(
            'id').filter(name=driver_info.company)
        company_drivers = Driver.objects.only(
            'nick').filter(company=company_id[0])
        drivers_dict = {}
        for company_driver in company_drivers:
            drivers_dict[company_driver.id] = company_driver.nick
            drivers = tuple(drivers_dict.items())
    else:
        return HttpResponse(status=500)
    dispositions = []
    forms = []
    if request.POST:
        first_disposition_form = NewDispositionForm(
            drivers, data=request.POST, prefix="first_disposition_form")
        second_disposition_form = NewDispositionForm(
            drivers, data=request.POST, prefix="second_disposition_form")
        third_disposition_form = NewDispositionForm(
            drivers, data=request.POST, prefix="third_disposition_form")
        fourth_disposition_form = NewDispositionForm(
            drivers, data=request.POST, prefix="fourth_disposition_form")
        fifth_disposition_form = NewDispositionForm(
            drivers, data=request.POST, prefix="fifth_disposition_form")
        forms.append(first_disposition_form)
        forms.append(second_disposition_form)
        forms.append(third_disposition_form)
        forms.append(fourth_disposition_form)
        forms.append(fifth_disposition_form)
        rozpiska = Rozpiska()
        rozpiska.driver = Driver.objects.get(nick=driver_info.nick)
        rozpiska.save()
        disposed_driver = Driver.objects.get(
            id=request.POST['first_disposition_form-driver'])
        for form in forms:
            if form.is_valid():
                disposition = form.save(commit=False)
                disposition.loading_country = get_country(disposition.loading_city)
                disposition.unloading_country = get_country(disposition.unloading_city)
                disposition.driver = disposed_driver
                disposition.is_rozpiska = True
                disposition.rozpiska = rozpiska
                disposition.save()
                dispositions.append(disposition)
            else:
                first_disposition_form = NewDispositionForm(
                    drivers, prefix="first_disposition_form")
                second_disposition_form = NewDispositionForm(
                    drivers, prefix="second_disposition_form")
                third_disposition_form = NewDispositionForm(
                    drivers, prefix="third_disposition_form")
                fourth_disposition_form = NewDispositionForm(
                    drivers, prefix="fourth_disposition_form")
                fifth_disposition_form = NewDispositionForm(
                    drivers, prefix="fifth_disposition_form")
                return render(request, 'hercules_app/create_rozpiska.html', {
                    'driver': driver,
                    'first_disposition_form': first_disposition_form,
                    'second_disposition_form': second_disposition_form,
                    'third_disposition_form': third_disposition_form,
                    'fourth_disposition_form': fourth_disposition_form,
                    'fifth_disposition_form': fifth_disposition_form
                })
        rozpiska.first_disposition = dispositions[0]
        rozpiska.second_disposition = dispositions[1]
        rozpiska.third_disposition = dispositions[2]
        rozpiska.fourth_disposition = dispositions[3]
        rozpiska.fifth_disposition = dispositions[4]
        rozpiska.save()
        request.session['created_disposition'] = True
        return redirect('/Company/Dispositions')
    else:
        first_disposition_form = NewDispositionForm(
            drivers, prefix="first_disposition_form")
        second_disposition_form = NewDispositionForm(
            drivers, prefix="second_disposition_form")
        third_disposition_form = NewDispositionForm(
            drivers, prefix="third_disposition_form")
        fourth_disposition_form = NewDispositionForm(
            drivers, prefix="fourth_disposition_form")
        fifth_disposition_form = NewDispositionForm(
            drivers, prefix="fifth_disposition_form")
        args = {
            'nick': driver_info.nick,
            'position': driver_info.position,
            'avatar': driver_info.avatar,
            'company': driver_info.company,
            'first_disposition_form': first_disposition_form, 'second_disposition_form': second_disposition_form,
            'third_disposition_form': third_disposition_form,
            'fourth_disposition_form': fourth_disposition_form,
            'fifth_disposition_form': fifth_disposition_form
        }
        return render(request, 'hercules_app/create_rozpiska.html', args)

@login_required(login_url="/login")
def GetRandomDispositionInfo(request):
    with open('static/assets/files/companies.json', 'r') as cities_json:
        cities = json.load(cities_json)
    first_city = cities[randint(0, len(cities) - 1)].get("city_name")
    for city in cities:
        if city["city_name"] == first_city:
            companies = city["companies"]
            loading_country = city.get("country")
    loading_company = companies[randint(0, len(companies) - 1)]
    unloading_city = cities[randint(0, len(cities) - 1)].get("city_name")
    for city in cities:
        if city["city_name"] == unloading_city:
            companies = city["companies"]
            unloading_country = city.get("country")
    unloading_company = companies[randint(0, len(companies) - 1)]
    with open('static/assets/files/cargo.json', 'r', encoding="utf-8") as cargo_json:
        cargos = json.load(cargo_json)
    cargo = cargos[randint(0, len(cargos) - 1)]
    cargo_name = cargo["cargo_name"]
    tonnage = cargo["mass"]
    disposition = {
        'loading_city': first_city,
        'loading_country': loading_country,
        'loading_spedition': loading_company,
        'unloading_city': unloading_city,
        'unloading_spedition': unloading_company,
        'unloading_country': unloading_country,
        'cargo': cargo_name,
        'tonnage': tonnage,
    }
    return JsonResponse(disposition)

@login_required(login_url="/login")
def ShowJobApplicationsCompanyView(request):
    driver_info = Driver.get_driver_info(request)
    if driver_info.position == "Szef":
        company = Company.objects.get(name=driver_info.company)
        if company.name != driver_info.company:
            return HttpResponse(status=403)
        else:
            work_applications = WorkApplications.get_company_applications(company)
            args = {
                'nick': driver_info.nick,
                'position': driver_info.position,
                'avatar': driver_info.avatar,
                'company': driver_info.company,
                'applications': work_applications
            }
            return render(request, 'hercules_app/job_applications_chef.html', args)

@login_required(login_url="/login")
def ShowJobApplicationsDriversView(request):
    driver_info = Driver.get_driver_info(request)
    if driver_info.position is None:
        work_applications = WorkApplications.get_driver_applications(driver_info.nick)
        args = {
                'nick': driver_info.nick,
                'position': None,
                'avatar': driver_info.avatar,
                'company': None,
                'applications': work_applications
        }
        return render(request, 'hercules_app/job_applications_driver.html', args)
    else:
        return HttpResponse(status=403)

@login_required(login_url="/login")
def ShowJobApplicationDetailsView(request, application_id):
    driver_info = Driver.get_driver_info(request)
    if driver_info.position == "Szef":
        company = Company.objects.get(name=driver_info.company)
        if company.name != driver_info.company:
            return HttpResponse(status=403)
        else:
            work_application = WorkApplications.get_application(application_id)
            args = {
                'nick': driver_info.nick,
                'position': driver_info.position,
                'avatar': driver_info.avatar,
                'company': driver_info.company,
                'application': work_application
            }
            return render(request, 'hercules_app/verify_application.html', args)
    elif driver_info.position is None:
        work_application = WorkApplications.get_application(application_id)
        args = {
            'nick': driver_info.nick,
            'position': driver_info.position,
            'avatar': driver_info.avatar,
            'company': driver_info.company,
            'application': work_application
        }
        return render(request, 'hercules_app/application_details.html', args)
    else:
        return HttpResponse(status=403)

@login_required(login_url="/login")
def AcceptJobApplication(request, application_id):
    if request.POST:
        driver_info = Driver.get_driver_info(request)
        if driver_info.position == "Szef":
            company = Company.objects.get(name=driver_info.company)
            if company.name != driver_info.company:
                return HttpResponse(status=403)
            else:
                work_application = WorkApplications.get_application(application_id)
                new_driver = Driver.objects.get(nick=work_application.driver)
                new_driver.company = company
                new_driver.save()
                Company.objects.filter(name=driver_info.company).update(drivers_count=company.drivers_count + 1)
                work_application.status = "ACCEPTED"
                work_application.save()
                request.session['job_application_accepted'] = True
                return redirect('/panel')

        else:
            return HttpResponse(status=403)
    else:
        return HttpResponse(status=403)

@login_required(login_url="/login")
def RejectJobApplication(request, application_id):
    if request.POST:
        driver_info = Driver.get_driver_info(request)
        if driver_info.position == "Szef":
            company = Company.objects.get(name=driver_info.company)
            if company.name != driver_info.company:
                return HttpResponse(status=403)
            else:
                work_application = WorkApplications.get_application(application_id)
                work_application.status = "REJECTED"
                work_application.save()
                request.session['job_application_rejected'] = True
                return redirect('/Company/JobApplications')
        else:
            return HttpResponse(status=403)
    else:
        return HttpResponse(status=403)

@login_required(login_url="/login")
def SendJobApplicationView(request, company_id):
    driver_info = Driver.get_driver_info(request)
    company = Company.objects.get(id=company_id)
    if request.POST:
        form = SendApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.company = company
            application.save()
            return redirect("/JobApplications")
        else:
            form = SendApplicationForm(initial={'driver': driver_info.nick})
    else:
        form = SendApplicationForm(initial={'driver': driver_info.nick})
        args = {
            'nick': driver_info.nick,
            'position': None,
            'avatar': driver_info.avatar,
            'company': None,
            'form': form,
        }
        return render(request, "hercules_app/send_application.html", args)