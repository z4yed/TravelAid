from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from address.models import Address
# Create your models here.
from users_auth.models import APPROVE_USER_STATUS, User

AVAILABLE = 1
PENDING = 2
BOOKED = 3

ROOM_STATUS_CHOICES = (
    (AVAILABLE, "Available"),
    (PENDING, "Pending"),
    (BOOKED, "Booked")
)


PAYMENT_STATUS_CHOICES = (
    ('Paid', 'Paid'),
    ('Unpaid', 'Unpaid'),
    ('Partially Paid', 'Partially Paid'),
    ('Over Paid', 'Over Paid'),
)


class Accommodation(models.Model):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='home_owner', null=True, blank=True)
    image = models.ImageField(upload_to='accommodations', null=True, blank=True)
    address = models.ForeignKey(Address, on_delete=models.DO_NOTHING, related_name='accommodation_address' , null=True, blank=True)
    description = RichTextUploadingField(null=True, blank=True)

    def __str__(self):
        return self.name


class Room(models.Model):
    accommodation = models.ForeignKey(Accommodation, on_delete=models.SET_NULL, null=True, blank=True)
    room_number = models.CharField(max_length=100)
    image = models.ImageField(upload_to='rooms', null=True, blank=True)
    description = RichTextUploadingField(null=True, blank=True)
    cost_per_day = models.FloatField(default=0)
    current_status = models.IntegerField(choices=ROOM_STATUS_CHOICES, default=1)

    def __str__(self):
        return "{a} -> {b}".format(a=self.room_number, b=self.accommodation.name)


class BookAccommodation(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='book_user', null=True, blank=True)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, related_name='book_room', null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    requested_date = models.DateTimeField(auto_now_add=True)
    total_bills = models.FloatField()
    paid_bills = models.FloatField(default=0)
    due_bills = models.FloatField(default=0)
    payment_status = models.CharField(choices=PAYMENT_STATUS_CHOICES, default="Unpaid", max_length=20)
    status = models.IntegerField(choices=APPROVE_USER_STATUS, default=1)

    def __str__(self):
        return "{a} by {b} ".format(a=self.room.room_number, b=self.user.first_name)


class AccommodationBillPayment(models.Model):
    bill = models.ForeignKey(BookAccommodation, on_delete=models.SET_NULL, related_name='bill', null=True, blank=True)
    payment_bdt = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)
    note = models.TextField()

    def __str__(self):
        return "Bill of - {a}".format(a=self.bill.room.room_number)
