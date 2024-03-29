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
    path('Gielda/Offers/NewOffer',
         views.CreateOfferView, name="create-offer"),
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
    path('JobApplications', views.ShowJobApplicationsDriversView, name="job-applications"),
    path('Company/EditWaybill/<int:waybill_id>',
         views.EditWaybill, name="edit-delivery"),
    path('Companies/AddNewCompany', views.AddNewCompanyView, name="add-company"),
    path('Companies/AddCompany', views.AddCompany, name="add-company-api"),
     path('Company/CompanyProfile',
         views.ShowCompanyProfileView, name="show-company-profile"),
     path('Company/Drivers/', views.ShowCompanyDriversView, name="show-company-drivers"),
    path('Company/Drivers/<int:driver_id>', views.ShowCompanyDriverView, name="show-company-driver"),
    path('Company/Drivers/DismissDriver/<int:driver_id>', views.DismissDriver, name="dismiss-driver"),
    path('Company/ChangePosition/<int:driver_id>', views.ChangePosition, name="change-position"),
    path('Company/Waybills', views.CompanyWaybillsView, name="show-company-waybills"),
    path('Company/Waybills/<int:waybill_id>', views.VerifyWaybillView, name="verify-waybill"),
    path('Company/Waybill/Accept/<int:waybill_id>', views.AcceptWaybill, name="accept-waybill"),
    path('Company/Waybills/ToEdit/<int:waybill_id>',
         views.ToEditWaybill, name="to-edit-waybill"),
    path('Company/Waybills/Reject/<int:waybill_id>',
         views.RejectWaybill, name="reject-waybill"),
    path('Company/Settings',
         views.CompanySettingsView, name="company-settings"),
    path('Company/Settings/EditCompanyInformation',
         views.EditCompanyInformation, name="edit-company-information"),
    path('Company/Settings/EditCompanySettings',
         views.EditCompanySettings, name="edit-company-information"),
     path('Company/DeleteCompany', views.DeleteCompany, name="delete-company"),
     path("Company/Dispositions", views.ShowCompanyDispositionsView, name="show-company-dispositions"),
     path("Company/Dispositions/AddNewDisposition", views.ChooseDispositionView, name="choose-disposition"),
     path("Company/Dispositions/AddNewDisposition/NewDisposition", views.CreateNewDispositionView, name="create-disposition"),
     path("Company/Dispositions/AddNewDisposition/NewRozpiska",
         views.CreateNewRozpiskaView, name="create-rozpiska"),
     path("Dispositions/RandomDisposition", views.GetRandomDispositionInfo, name="random-disposition"),
     path("Company/JobApplications", views.ShowJobApplicationsCompanyView, name="company-job-applications"),
     path("Company/JobApplications/<int:application_id>", views.ShowJobApplicationDetailsView, name="job-application-details"),
     path("Company/JobApplications/Accept/<int:application_id>",
         views.AcceptJobApplication, name="job-application-accept"),
     path("Company/JobApplications/Reject/<int:application_id>",
         views.RejectJobApplication, name="job-application-reject"),
    path ("JobApplications/SendApplication/<int:company_id>", views.SendJobApplicationView, name="send-job-application"),
    path ("JobApplications/<int:application_id>", views.ShowJobApplicationDetailsView, name="job-application-details-driver"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
