from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver


PENDING = 1
APPROVED = 2
REJECTED = 3

APPROVE_USER_STATUS = (
    (PENDING, 'Pending'),
    (APPROVED, 'Approved'),
    (REJECTED, 'REJECTED'),
)


class User(AbstractUser):
    is_doctor = models.BooleanField(default=False)
    is_user = models.BooleanField(default=False)
    user_status = models.CharField(max_length=50, choices=APPROVE_USER_STATUS, default=1)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor')
    full_name = models.CharField(max_length=100, null=True, blank=True)
    cell = models.CharField(max_length=11, null=True, blank=True)
    address = models.CharField(max_length=200)
    doctor_status = models.CharField(max_length=50, choices=APPROVE_USER_STATUS, default=1)

    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='update_doctor', null=True, blank=True)


class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_info')
    full_name = models.CharField(max_length=100, null=True, blank=True)
    cell = models.CharField(max_length=11, null=True, blank=True)
    address = models.CharField(max_length=200)

    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='update_info', null=True, blank=True)

    def __str__(self):
        return "{username}'s Info".format(username=self.user.username)


@receiver(post_save, sender=User)
def create_user_information(sender, instance, created, **kwargs):
    if created:
        UserInfo.objects.create(user=instance)
