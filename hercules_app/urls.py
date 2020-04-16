from django.urls import path
from . import views
from register import views as register_views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('login', auth_views.LoginView.as_view(
        template_name="hercules_app/sign-in.html",
        extra_context={
            'next': '/panel',
        }, redirect_authenticated_user=True), name='login'),
    path('register', register_views.register, name='register'),
    path('hello', views.hello, name='hello'),
    path('logout', register_views.logout_user, name='logout'),
    path('panel', views.panel, name="panel"),
    path('download', views.download_assistant, name="download"),
    path('get-assistant', views.download_file, name="get-assistant"),
    path('drivers-card', views.drivers_card, name="drivers-card"),
    path('add-delivery', views.add_delivery, name="add-delivery"),
    path('automatic-step-1', views.send_first_screenshot, name="automatic-step-1"),
    path('automatic-step-2', views.send_second_screenshot, name="step-2-automatic"),
    path('processing-waybill', views.loading_page, name="processing-waybill"),
    path('process-waybill-api', views.process_waybill, name='process-waybill-api'),
    path('add-waybill', views.add_waybill, name="add-waybill"),
    path('Waybill/AddWaybill/Manual/step-one', views.manual_step_one, name="manual-step-one"),
    path('Gielda/Offers/', views.OffersView, name="gielda"),
    path('Gielda/Offers/<int:offer_id>', views.OfferDetailsView, name="offer-details"),
    path('Gielda/Offers/ChooseDriver',
         views.ChooseDriverView, name="dispose-offer"),
    path('Gielda/Offers/DisposeOffer/<int:driver_id>',
         views.DisposeOffer, name="dispose-offer"),
    path('Dispositions',
         views.ShowDispositionsView, name="user-dispositions"),
    path('Companies',
         views.FindCompanyView, name="find-company"),
    path('Companies/<int:company_id>',
         views.CompanyDetailsView, name="find-company"),
    path('Vehicles',
         views.CompanyVehiclesView, name="vehicles"),
    path('Vehicles/<int:vehicle_id>',
         views.VehicleDetailsView, name="vehicle-details"),
    path('Vehicles/AddNewVehicle',
         views.AddNewVehicleView, name="add-vehicle"),
    path('Vehicles/<int:vehicle_id>/DeleteVehicle',
         views.DeleteVehicle, name="edit-delivery"),
    path('Deliveries',
         views.ShowDeliveriesView, name="user-deliveries"),
     path('Deliveries/<int:waybill_id>',
         views.ShowDeliveryDetailsView, name="delivery-details"),
    path('EditWaybill/<int:waybill_id>',
         views.EditWaybill, name="edit-delivery"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

