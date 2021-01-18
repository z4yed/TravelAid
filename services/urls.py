from django.urls import path, include
from .views import accommodation_view as accommodation_views
from .views import hospital_view as hospital_views

app_name = 'services'

urlpatterns = [
    path('accommodations/', accommodation_views.AccommodationList.as_view(), name='accommodation_list_url'),
    path('accommodation/<int:pk>/', accommodation_views.AccommodationDetailView.as_view(), name='accommodation_detail_url'),
    path('room/<int:pk>/', accommodation_views.RoomDetailView.as_view(), name='room_details'),
    path('bookings/<int:user_id>/', accommodation_views.BookingsView.as_view(), name='bookings_url'),
    path('edit_booking/<int:booking_id>/', accommodation_views.BookingsView.as_view(), name='edit_booking_url'),
    path('print_invoice/<int:booking_id>/', accommodation_views.DownloadInvoice.as_view(), name='print_invoice_url'),
    path('make_accommodation_payment/<int:booking_id>/', accommodation_views.AccommodationPaymentView.as_view(), name='make_accommodation_payment_url'),
    path('delete_booking/<int:booking_id>/', accommodation_views.BookingDeleteView.as_view(), name='delete_booking_url'),


    path('hospitals/', hospital_views.HospitalList.as_view(), name='hospital_list_url'),
    path('hospital/<int:id>/', hospital_views.HospitalDetailsView.as_view(), name='hospital_details_url'),
    path('hospital/doctor/<int:doctor_id>', hospital_views.DoctorDetailsView.as_view(), name='doctor_details_url'),
    path('request_appointments/<int:doctor_id>/', hospital_views.DoctorDetailsView.as_view(), name='request_appointments_url'),
    path('my_appointments/<int:user_id>/', hospital_views.UserAppointmentView.as_view(), name='user_appointments_url'),
    path('edit_appointment/<int:appointment_id>/', hospital_views.UserAppointmentView.as_view(), name='edit_appointment_url'),
    path('delete_appointment/<int:appointment_id>/', hospital_views.DeleteAppointmentView.as_view(), name='delete_appointment_url'),

    # Doctor Controls
    path('manage-appointments/<int:doctor_id>/', hospital_views.ManageAppointmentsView.as_view(), name='manage_appointments_url'),
    path('approve-appointment/<int:approve_id>/', hospital_views.ManageAppointmentsView.as_view(), name='approve_appointmetn_url'),
    path('reject-appointment/<int:reject_id>/', hospital_views.ManageAppointmentsView.as_view(), name='reject_appointment_url'),
    path('release-appointment/<int:release_id>/', hospital_views.ManageAppointmentsView.as_view(), name='release_appointment_url'),
    path('download-appointment-invoice/<int:appointment_bill_id>/', hospital_views.DownloadAppointmentInvoice.as_view(), name='download_appointment_invoice'),
]
