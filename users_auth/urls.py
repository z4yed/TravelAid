from django.urls import path, include
from . import views

app_name = 'authenticate'

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login_url'),
    path('logout/', views.LogoutView.as_view(), name='logout_url'),
    path('profile/<int:pk>/', views.ProfileView.as_view(), name='profile_url'),
    path('register/', views.RegistrationView.as_view(), name='registration_url'),
    path('admin_dashboard/', views.AdminDashboardView.as_view(), name='admin_dashboard_url'),
    path('doctor_dashboard/<int:doctor_id>', views.DoctorDashboardView.as_view(), name='doctor_dashboard_url'),
    path('police_dashboard/', views.PoliceDashboardView.as_view(), name='police_dashboard_url'),
    path('manager_dashboard/', views.ManagerDashboardView.as_view(), name='manager_dashboard_url'),
]
