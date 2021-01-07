from django.contrib import admin
from services.models.accommodation_models import Room, Accommodation, BookAccommodation, AccommodationBillPayment
from services.models.hospital_models import Hospital, Appointment, AppointmentBill, AppointmentBillPayment
# Register your models here.

admin.site.register(Room)
admin.site.register(Accommodation)
admin.site.register(BookAccommodation)
admin.site.register(AccommodationBillPayment)

admin.site.register(Hospital)
admin.site.register(Appointment)
admin.site.register(AppointmentBill)
admin.site.register(AppointmentBillPayment)
