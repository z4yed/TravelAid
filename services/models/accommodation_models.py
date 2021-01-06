from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from address.models import Address
from users_auth.models import User
# Create your models here.

AVAILABLE = 1
PENDING = 2
BOOKED = 3

STATUS_CHOICES = (
    (AVAILABLE, "Available"),
    (PENDING, "Pending"),
    (BOOKED, "Booked")
)


class Room(models.Model):
    room_number = models.CharField(max_length=100)
    description = RichTextUploadingField(null=True, blank=True)
    cost_per_day = models.FloatField(default=0)
    current_status = models.IntegerField(choices=STATUS_CHOICES, default=1)

    def __str__(self):
        return self.room_number


class Accommodation(models.Model):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)
    rooms = models.ManyToManyField(Room)
    image = models.ImageField(upload_to='accommodations', null=True, blank=True)
    address = models.ForeignKey(Address, on_delete=models.DO_NOTHING, related_name='accommodation_address' , null=True, blank=True)

    def __str__(self):
        return self.name