from django.contrib import admin
from .models.accommodation_models import Room, Accommodation

# Register your models here.

admin.site.register(Room)
admin.site.register(Accommodation)