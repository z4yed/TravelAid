from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from address.models import Address
from users_auth.models import User, APPROVE_USER_STATUS
from .accommodation_models import PAYMENT_STATUS_CHOICES

Government = 1
Private = 2

PENDING = 1
APPROVED = 2
REJECTED = 3
ON_HOLD = 4
RELEASED = 5


HOSPITAL_TYPES = (
    (Government, "Government"),
    (Private, "Private")
)

APPOINTMENT_STATUS = (
    (PENDING, 'Pending'),
    (APPROVED, 'Approved'),
    (REJECTED, 'Rejected'),
    (ON_HOLD, 'On Hold'),
    (RELEASED, 'Released'),
)


class Hospital(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    type = models.IntegerField(choices=HOSPITAL_TYPES, default=1)
    image = models.ImageField(upload_to='hospitals', null=True, blank=True)
    description = RichTextUploadingField(null=True, blank=True)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
    doctors = models.ManyToManyField(User, blank=True)
    emergency_cell = models.CharField(max_length=11)

    def __str__(self):
        return self.name


class Appointment(models.Model):
    doctor = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='doctor', null=True, blank=True)
    patient = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='patient', null=True, blank=True)
    date = models.DateField()
    description = RichTextUploadingField(null=True, blank=True)
    status = models.IntegerField(choices=APPOINTMENT_STATUS, default=1)
    doctors_note = RichTextUploadingField(null=True, blank=True)
    requested_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "P:{a} --> D:{b}".format(a=self.patient.get_full_name(), b=self.doctor.get_full_name() )


class AppointmentBill(models.Model):
    appointment = models.ForeignKey(Appointment, related_name='appointment', on_delete=models.SET_NULL, null=True, blank=True)
    room_charge = models.FloatField(default=0)
    medicine_charge = models.FloatField(default=0)
    doctors_charge = models.FloatField(default=0)
    others_charge = models.FloatField(default=0)
    total_bills = models.FloatField(default=0)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return "Bill ID : {a}".format(a=str(self.id))
