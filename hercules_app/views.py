from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from datetime import datetime
from django.contrib.auth.decorators import user_passes_test
from hercules_app.models import (
    Driver,
    Company,
    DriverStatistics,
    Vehicle,
    Disposition,
    Waybill,
    Gielda,
    Rozpiska
    )
from hercules_app.forms import SetNickForm, FirstScreenshotForm, SecondScreenshotForm, AddWaybillForm, EditVehicleForm, AddVehicleForm
from django.utils.encoding import smart_str
from .tasks import get_waybill_info
from django_celery_results.models import TaskResult
from decimal import Decimal


def index(request):
    return render(request, 'hercules_app/index.html')


def login(request):
    return render(request, 'hercules_app/sign-in.html')


@login_required
# TODO: create test for checking if the user
# nick or not
def hello(request):
    current_user = request.user
    form = SetNickForm()
    if request.method == "POST":
        form = SetNickForm(request.POST)
        if form.is_valid():
            Driver.objects.filter(user=current_user).update(
                nick=form.data['nick'])
            return redirect('panel')
        form = SetNickForm()
    return render(request, 'hercules_app/hello.html')


@login_required
def panel(request):
    waybill_success = request.session.get('waybill_success')
    if waybill_success is True:
        request.session.modified = True
        del request.session['waybill_success']

    dispose_offer_success = request.session.get('dispose_offer_success')
    if dispose_offer_success is True:
        request.session.modified = True
        del request.session['dispose_offer_success']

    driver = Driver.objects.get(user=request.user)

    driver_info = Driver.get_driver_info(request)

    statistics = DriverStatistics.get_driver_statistics(driver)
    dispositions = Disposition.objects.filter(driver=driver)[:3]

    args = {
        'nick': driver_info.nick,
        'avatar': driver_info.avatar,
        'company': driver_info.company,
        'statistics': statistics,
        'vehicle': driver_info.vehicle,
        'dispositions': dispositions,
        'waybill_success': waybill_success,
        'dispose_offer_success': dispose_offer_success,
    }
    return render(request, 'hercules_app/panel.html', args)


@login_required
def download_assistant(request):
    driver_info = Driver.get_driver_info(request)
    args = {
        'nick': driver_info.nick,
        'company': driver_info.company,
    }
    return render(request, 'hercules_app/download.html', args)


@login_required
def download_file(request):
    response = HttpResponse(content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(
        'assistant.zip')

    response['X-Sendfile'] = smart_str('assistant.zip')
    return response


@login_required
def drivers_card(request):
    driver = Driver.objects.get(user=request.user)

    driver_info = Driver.get_driver_info(request)

    statistics = DriverStatistics.get_driver_statistics(driver)
    dispositions = Disposition.objects.filter(driver=driver)[:5]
    args = {
        'nick': driver_info.nick,
        'company': driver_info.company,
        'statistics': statistics,
        'dispositions': dispositions,
        'vehicle': driver_info.vehicle,
    }
    return render(request, 'hercules_app/drivers-card.html', args)


@login_required
def add_delivery(request):
    driver_info = Driver.get_driver_info(request)
    args = {
        'nick': driver_info.nick,
        'company': driver_info.company,
    }
    return render(request, 'hercules_app/add_delivery.html', args)


@login_required
def send_first_screenshot(request):
    driver_info = Driver.get_driver_info(request)
    args = {
        'nick': driver_info.nick,
        'company': driver_info.company,
    }
    if request.method == 'POST':
        form = FirstScreenshotForm(request.POST, request.FILES)
        if form.is_valid():
            waybill = form.save()
            request.session['waybill_id'] = waybill.id
        else:
            form = FirstScreenshotForm()
    return render(request, 'hercules_app/automatic_1.html', args)


@login_required
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


@login_required
def loading_page(request):
    driver_info = Driver.get_driver_info(request)
    args = {
        'nick': driver_info.nick,
        'company': driver_info.company,
    }
    return render(request, 'hercules_app/loading.html', args)


@login_required
def manual_step_one(request):
    waybill = Waybill()
    waybill.save()
    request.session['waybill_id'] = waybill.id
    request.session['waybill_automatic'] = False
    return send_second_screenshot(request)


@login_required
def process_waybill(request):
    waybill_id = request.session.get('waybill_id')
    # TODO: check if the waybill_id is passed correctly
    waybill = Waybill.objects.get(id=waybill_id)
    info = get_waybill_info.delay(waybill.first_screen.path,
                                  waybill.end_screen.path)
    args = info.get()
    if args is not None:
        request.session['screen_information'] = args
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=500)


@login_required
def add_waybill(request):
    is_automatic = True
    args = ''
    driver = Driver.objects.get(user=request.user)
    driver_info = Driver.get_driver_info(request)
    driver_inf = {
        'nick': driver_info.nick,
        'company': driver_info.company,
    }

    waybill_id = request.session.get('waybill_id')
    # TODO: check if the waybill_id is passed correctly
    waybill = Waybill.objects.get(id=waybill_id)
    if waybill.first_screen.name == "":
        is_automatic = False
    else:
        args = request.session['screen_information']
    if request.method == "POST":
        form = AddWaybillForm(request.POST, instance=waybill)
        if form.is_valid():
            waybill = form.save(commit=False)
            waybill.driver = driver
            waybill.screens_id = args['screen_id']
            waybill.save()
            if driver.is_employeed == False:
                statistics = DriverStatistics.objects.get(driver_id=driver)
                DriverStatistics.objects.filter(driver_id=driver).update(
                    distance=statistics.distance + int(form.data['distance']),
                    tonnage=statistics.tonnage + int(form.data['tonnage']),
                    income=statistics.income + int(form.data['income']),
                    fuel=statistics.income + int(form.data['fuel']),
                    average_fuel=round(Decimal(statistics.fuel + int(form.data['fuel']))/Decimal(
                        statistics.distance + int(form.data['distance']))*100, 2),
                    deliveries_count=statistics.deliveries_count + 1,
                )
                Waybill.objects.filter(id=waybill_id).update(
                    status="accepted")
            request.session.modified = True
            request.session['waybill_success'] = True
            del request.session['waybill_id']
            if is_automatic:
                del request.session['screen_information']
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

    return render(request, 'hercules_app/verify.html', {'form': form, 'args': args, 'driver': driver_inf, 'is_automatic': is_automatic})


@login_required
def OffersView(request):
    if request.session.get('offer_id') is not None:
        del request.session['offer_id']
    driver_info = Driver.get_driver_info(request)
    driver = {
        'nick': driver_info.nick,
        'company': driver_info.company,
    }
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
    return render(request, 'hercules_app/gielda.html', {'offers': offers, 'driver': driver, 'sort_by': sort_by})


@login_required
def OfferDetailsView(request, offer_id):
    driver_info = Driver.get_driver_info(request)
    driver = {
        'nick': driver_info.nick,
        'company': driver_info.company,
    }
    offer = Gielda.objects.get(id=offer_id)
    try:
        company_drivers_count = Company.objects.values_list(
            'drivers_count', flat=True).get(name=driver_info.company)
    except:
        company_drivers_count = 1
    is_self_employed = False
    request.session['offer_id'] = offer_id
    if company_drivers_count == 1:
        is_self_employed = True
    return render(request, 'hercules_app/offer_details.html', {'offer': offer, 'driver': driver, 'is_self_employed': is_self_employed})


@login_required
def ChooseDriverView(request):
    driver_info = Driver.get_driver_info(request)
    driver = {
        'nick': driver_info.nick,
        'company': driver_info.company,
    }
    company_drivers_count = Company.objects.values_list(
        'drivers_count', flat=True).get(name=driver_info.company)
    if company_drivers_count > 1:
        company_drivers = Driver.objects.all().filter(company=driver_info.company)
        company_drivers_vehicles = []
        for company_driver in company_drivers:
            company_drivers_vehicles.append(
                Vehicle.objects.get(driver=company_driver))
        return render(request, 'hercules_app/offer_dispose.html', {'driver': driver, 'drivers': company_drivers, 'vehicles': company_drivers_vehicles})
    else:
        return HttpResponse(status=500)


@login_required
def DisposeOffer(request, driver_id):
    disposition = Disposition()
    offer_id = request.session.get('offer_id')
    offer = Gielda.objects.get(id=offer_id)
    del request.session['offer_id']
    disposition.loading_city = offer.loading_city
    disposition.loading_spedition = offer.loading_spedition
    disposition.unloading_city = offer.unloading_city
    disposition.unloading_spedition = offer.unloading_spedition
    disposition.cargo = offer.cargo
    disposition.tonnage = offer.tonnage
    disposition.driver = Driver.objects.get(id=driver_id)
    request.session['dispose_offer_success'] = True
    return redirect('panel')


@login_required
def ShowDispositionsView(request):
    driver = Driver.objects.get(user=request.user)
    dispositions = Disposition.objects.all().filter(driver=driver)
    rozpiski_objects = Rozpiska.objects.all().filter(driver=driver)
    rozpiski = []
    for rozpiska in rozpiski_objects:
        rozpiski.append(Disposition.objects.get(
            id=rozpiska.first_disposition_id))
        rozpiski.append(Disposition.objects.get(
            id=rozpiska.second_disposition_id))
        rozpiski.append(Disposition.objects.get(
            id=rozpiska.third_disposition_id))
        rozpiski.append(Disposition.objects.get(
            id=rozpiska.fourth_disposition_id))
        rozpiski.append(Disposition.objects.get(
            id=rozpiska.fifth_disposition_id))
    return render(request, 'hercules_app/dispositions.html', {'driver': driver, 'dispositions': dispositions, 'rozpiski': rozpiski})


def FindCompanyView(request):
    driver_info = Driver.get_driver_info(request)
    driver = {
        'nick': driver_info.nick,
        'company': driver_info.company,
    }
    companies = Company.objects.all().order_by('is_recruiting')
    return render(request, 'hercules_app/find_company.html', {'driver': driver, 'companies': companies})


def CompanyDetailsView(request, company_id):
    driver_info = Driver.get_driver_info(request)
    driver = {
        'nick': driver_info.nick,
        'avatar': driver_info.avatar,
        'company': driver_info.company,
    }
    company = Company.objects.get(id = company_id)

    return render(request, 'hercules_app/company_profile.html', {'driver': driver, 'company': company})

def CompanyVehiclesView(request):
    try:
        is_edited = request.session.get('vehicle_edited')
        del request.session['vehicle_edited']
    except:
        is_edited = False

    try:
        is_added = request.session.get('vehicle_added')
        del request.session['vehicle_added']
    except:
        is_added = False
    try:
        is_removed = request.session.get('vehicle_deleted')
        del request.session['vehicle_deleted']
    except:
        is_removed = False

    driver_info = Driver.get_driver_info(request)
    driver = {
        'nick': driver_info.nick,
        'avatar': driver_info.avatar,
        'company': driver_info.company,
    }
    company_id = Company.objects.only('id').filter(name=driver_info.company)
    vehicles = Vehicle.objects.all().filter(
        company=company_id[0])  # querysets are lazy
    return render(request, 'hercules_app/vehicles.html', {'driver': driver, 'vehicles': vehicles, 'is_edited': is_edited, 'is_added': is_added, 'is_removed': is_removed})

def VehicleDetailsView(request, vehicle_id):
    driver_info = Driver.get_driver_info(request)
    driver = {
        'nick': driver_info.nick,
        'avatar': driver_info.avatar,
        'company': driver_info.company,
    }
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    company_id = Company.objects.only('id').filter(name=driver_info.company)
    company_drivers = Driver.objects.only('nick').filter(company=company_id[0])
    drivers_dict = {}
    for company_driver in company_drivers:
        drivers_dict[company_driver.id] = company_driver.nick
    drivers = tuple(drivers_dict.items())
    current_driver = vehicle.driver.id
    form = EditVehicleForm(drivers, current_driver, initial={
        'brand': vehicle.brand,
        'model': vehicle.model,
        'cabin': vehicle.cabin,
        'engine': vehicle.engine,
        'gearbox': vehicle.gearbox,
        'wheelbase': vehicle.wheelbase,
        'wheels': vehicle.wheels,
        'odometer': vehicle.odometer,
        'driver': current_driver,
    })
    if request.method == "POST":
        form = EditVehicleForm(drivers, current_driver, request.POST, instance=vehicle)
        if form.is_valid():
            new_driver = Driver.objects.get(id=form.data['driver'])
            form = form.save(commit=False)
            form.driver = new_driver
            form.save()
            request.session['vehicle_edited'] = True
            return redirect('/Vehicles')
        else:
            form = EditVehicleForm(drivers, current_driver, initial={
            'brand': vehicle.brand,
            'model': vehicle.model,
            'cabin': vehicle.cabin,
            'engine': vehicle.engine,
            'gearbox': vehicle.gearbox,
            'wheelbase': vehicle.wheelbase,
            'wheels': vehicle.wheels,
            'odometer': vehicle.odometer,
            }
            )
    return render(request, 'hercules_app/vehicle_details.html', {'driver': driver, 'form': form, 'vehicle': vehicle})

def AddNewVehicleView(request):
    driver_info = Driver.get_driver_info(request)
    driver = {
        'nick': driver_info.nick,
        'avatar': driver_info.avatar,
        'company': driver_info.company,
    }
    company_id = Company.objects.only('id').filter(name=driver_info.company)
    company_drivers = Driver.objects.only('nick').filter(company=company_id[0])
    drivers_dict = {}
    for company_driver in company_drivers:
        drivers_dict[company_driver.id] = company_driver.nick
    drivers = tuple(drivers_dict.items())
    form = AddVehicleForm(drivers)
    if request.method == "POST":
        form = AddVehicleForm(drivers, request.POST, request.FILES)
        if form.is_valid():
            vehicle = form.save(commit=False)
            company = Company.objects.get(name=driver_info.company)
            vehicle.company = company
            vehicle.driver = Driver.objects.get(id=form.data['driver'])
            vehicle.save()
            request.session['vehicle_added'] = True
            return redirect('/Vehicles')
        else:
            form = AddVehicleForm(drivers)
    return render(request, 'hercules_app/add_vehicle.html', {'driver': driver, 'form': form})

def ShowDeliveriesView(request):
    driver_info = Driver.get_driver_info(request)
    driver = {
        'nick': driver_info.nick,
        'avatar': driver_info.avatar,
        'company': driver_info.company,
    }
    driver = Driver.objects.get(nick=driver_info.nick)
    deliveries = Waybill.objects.all().order_by(
        '-finish_date').filter(driver=driver)

    return render(request, 'hercules_app/deliveries.html', {'driver': driver, 'deliveries': deliveries})

def ShowDeliveryDetailsView(request, waybill_id):
    driver_info = Driver.get_driver_info(request)
    driver = {
        'nick': driver_info.nick,
        'avatar': driver_info.avatar,
        'company': driver_info.company,
    }
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
        return render(request, 'hercules_app/delivery_details.html', {'driver': driver, 'form': form, 'delivery': delivery})
    else:
        return render(request, 'hercules_app/delivery_details.html', {'driver': driver, 'delivery': delivery})

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

def DeleteVehicle(request, vehicle_id):
    if request.POST:
        Vehicle.objects.filter(id=vehicle_id).delete()
        request.session.modified = True
        request.session['vehicle_deleted'] = True
        return redirect('/Vehicles')
    else:
        return HttpResponse(status=500)
