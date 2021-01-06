from django.contrib import admin
from .models.accommodation_models import Room, Accommodation, BookAccommodation, AccommodationBill

# Register your models here.

admin.site.register(Room)
admin.site.register(Accommodation)
admin.site.register(BookAccommodation)
admin.site.register(AccommodationBill)
