from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.contrib.auth.decorators import user_passes_test
from hercules_app.models import Driver, Company, DriverStatistics, Vehicle, Disposition, Waybill, Gielda
from hercules_app.forms import SetNickForm, FirstScreenshotForm, SecondScreenshotForm, AddWaybillForm
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
    statistics = DriverStatistics.objects.get(driver_id=driver)
    if driver.company_id is not None:
        company = Company.objects.get(id=driver.company_id)
    company = ""
    try:
        vehicle = Vehicle.objects.get(driver=driver)
    except:
        vehicle = ""

    dispositions = Disposition.objects.filter(driver=driver)[:3]
    args = {
        'driver': driver,
        'company': company,
        'statistics': statistics,
        'vehicle': vehicle,
        'dispositions': dispositions,
        'waybill_success': waybill_success,
        'dispose_offer_success': dispose_offer_success,
    }
    return render(request, 'hercules_app/panel.html', args)


@login_required
def download_assistant(request):
    args = Driver.get_username(request.user)
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
    statistics = DriverStatistics.objects.get(driver_id=driver)
    if driver.company_id is not None:
        company = Company.objects.get(id=driver.company_id)
    vehicle = Vehicle.objects.get(driver=driver)
    dispositions = Disposition.objects.filter(driver=driver)[:5]
    args = {
        'driver': driver,
        'company': company,
        'statistics': statistics,
        'dispositions': dispositions,
        'vehicle': vehicle
    }
    return render(request, 'hercules_app/drivers-card.html', args)


@login_required
def add_delivery(request):
    driver = Driver.objects.get(user=request.user)
    args = {
        'driver': driver,
    }
    return render(request, 'hercules_app/add_delivery.html', args)


@login_required
def send_first_screenshot(request):
    driver = Driver.objects.get(user=request.user)
    args = {
        'driver': driver,
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
def send_second_screenshot(request, is_automatic):
    if is_automatic is None:
        is_automatic = True
    driver = Driver.objects.get(user=request.user)
    args = {
        'driver': driver,
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
    return render(request, 'hercules_app/loading.html')

@login_required
def manual_step_one(request):
    waybill = Waybill()
    waybill.save()
    request.session['waybill_id'] = waybill.id
    return send_second_screenshot(request, is_automatic=False)

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
        return HttpResponse(status = 200)
    else:
        return HttpResponse(status = 500)


@login_required
def add_waybill(request):
    is_automatic = True
    args = ''
    waybill_id = request.session.get('waybill_id')
    # TODO: check if the waybill_id is passed correctly
    waybill = Waybill.objects.get(id=waybill_id)
    driver = Driver.objects.get(user=request.user)
    if waybill.first_screen.name == "":
        is_automatic = False
    else:
        args = request.session['screen_information']
    if request.method == "POST":
        form = AddWaybillForm(request.POST, instance=waybill)
        if form.is_valid():
            form.save()
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

    return render(request, 'hercules_app/verify.html', {'form': form, 'args': args, 'driver': driver})


@login_required
def OffersView(request):
    if request.session.get('offer_id') is not None:
        del request.session['offer_id']
    driver = Driver.objects.get(user=request.user)
    parameters = ['loading_city', 'loading_country', 'unloading_city', 'unloading_country']
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
    offers = Gielda.objects.all().filter(**filters, price__gte=income_min, price__lte=income_max).order_by(sort_by)
    return render(request, 'hercules_app/gielda.html', {'offers': offers, 'driver': driver, 'sort_by': sort_by})

@login_required
def OfferDetailsView(request, offer_id):
    driver = Driver.objects.get(user=request.user)
    offer = Gielda.objects.get(id=offer_id)
    company_drivers_count = Company.objects.values_list(
        'drivers_count', flat=True).get(name=driver.company)
    is_self_employed = False
    request.session['offer_id'] = offer_id
    if company_drivers_count == 1:
        is_self_employed = True
    return render(request, 'hercules_app/offer_details.html', {'offer': offer, 'driver': driver, 'is_self_employed': is_self_employed})

@login_required
def ChooseDriverView(request):
    driver = Driver.objects.get(user=request.user)
    company_drivers_count = Company.objects.values_list(
            'drivers_count', flat=True).get(name=driver.company)
    if company_drivers_count > 1:
        company_drivers = Driver.objects.all().filter(company=driver.company)
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
