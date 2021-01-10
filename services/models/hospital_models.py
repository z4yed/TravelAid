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
    doctors_note = models.TextField(null=True, blank=True)

    def __str__(self):
        return "P:{a} --> D:{b}".format(a=self.patient.first_name, b=self.doctor.first_name)


class AppointmentBill(models.Model):
    appointment = models.ForeignKey(Appointment, related_name='appointment', on_delete=models.SET_NULL, null=True, blank=True)
    total_bills = models.FloatField()
    due_bills = models.FloatField(default=0)
    paid_bills = models.FloatField(default=0)
    notes = models.TextField()
    payment_status = models.CharField(choices=PAYMENT_STATUS_CHOICES, default='Unpaid', max_length=20)

    def __str__(self):
        return "Bill ID : {a}".format(a=str(self.id))


class AppointmentBillPayment(models.Model):
    bill = models.ForeignKey(AppointmentBill, related_name='appointment_bill', on_delete=models.SET_NULL, null=True, blank=True)
    payment_bdt = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(null=True, blank=True)
    proof = models.FileField(upload_to='doctors_payments', null=True, blank=True)

    def __str__(self):
        return "Payment for : {a}".format(a=self.bill)
