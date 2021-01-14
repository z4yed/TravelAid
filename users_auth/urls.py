from django.urls import path, include
from . import views

app_name = 'authenticate'

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login_url'),
    path('logout/', views.LogoutView.as_view(), name='logout_url'),
    path('profile/<int:pk>/', views.ProfileView.as_view(), name='profile_url'),
    path('register/', views.RegistrationView.as_view(), name='registration_url'),
    path('admin_dashboard/', views.AdminDashboardView.as_view(), name='admin_dashboard_url'),
    path('doctor_dashboard/<int:doctor_id>/', views.DoctorDashboardView.as_view(), name='doctor_dashboard_url'),
    path('police_dashboard/', views.PoliceDashboardView.as_view(), name='police_dashboard_url'),
    path('manager_dashboard/<int:manager_id>/', views.ManagerDashboardView.as_view(), name='manager_dashboard_url'),

    # Manager's Control
    path('add-accommodation/', views.AccommodationManageView.as_view(), name='add_accommodation'),
    path('edit-accommodation/<int:editable_id>',  views.AccommodationManageView.as_view(), name='edit_accommodation'),
    path('delete-accommodation/<int:deletable_id>', views.AccommodationManageView.as_view(), name='delete_accommodation'),

    path('add-room/', views.RoomManageView.as_view(), name='add_room_url'),
    path('edit-room/<int:editable_id>', views.RoomManageView.as_view(), name='edit_room_url'),
    path('delete-room/<int:deletable_id>', views.RoomManageView.as_view(), name='delete_room_url'),

    path('manage-booking-request/<int:manager_id>', views.ManageBookingRequestView.as_view(), name='manage_booking_request'),
    path('approve-booking-request/<int:approvable_id>', views.ManageBookingRequestView.as_view(), name='approve_booking_request'),
    path('reject-booking-request/<int:rejectable_id>', views.ManageBookingRequestView.as_view(), name='reject_booking_request'),
]
