from django.urls import path, include
from . import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login_url'),
    path('register/', views.Registration.as_view(), name='registration_url')
]
