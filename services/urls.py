from django.urls import path, include
from .views import accommodation_view as accommodation_views
from .views import hospital_view as hospital_views

app_name = 'services'

urlpatterns = [
    path('accommodations/', accommodation_views.AccommodationList.as_view(), name='accommodation_list_url'),
    path('accommodation/<int:pk>/', accommodation_views.AccommodationDetailView.as_view(), name='accommodation_detail_url'),
    path('room/<int:pk>/', accommodation_views.RoomDetailView.as_view(), name='room_details'),
    path('hospitals/', hospital_views.HospitalList.as_view(), name='hospital_list_url'),
]
