from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from ckeditor_uploader.fields import RichTextUploadingField
from address.models import Address


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
    is_police = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
    user_status = models.IntegerField(choices=APPROVE_USER_STATUS, default=1)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        if self.is_doctor:
            return "{a} -- Doctor".format(a=self.first_name)
        elif self.is_manager:
            return "{a} -- Manager".format(a=self.first_name)
        elif self.is_police:
            return "{a} -- Police".format(a=self.first_name)
        elif self.is_staff:
            return "{a} -- Admin".format(a=self.username)
        else:
            return "{a} -- Normal User".format(a=self.first_name)


from services.models.hospital_models import Hospital   # don't move it at the top. It might
from system.models import Expertise                    # display Import Error


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_info')
    full_name = models.CharField(max_length=100, null=True, blank=True)
    cell = models.CharField(max_length=11, null=True, blank=True)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL,  related_name='user_address', null=True, blank=True)
    profile_picture = models.ImageField(default='default.jpg', upload_to='profile_pics', null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='update_profile', null=True, blank=True)
    description = RichTextUploadingField(null=True, blank=True)
    expertise = models.ManyToManyField(Expertise)
    hospital = models.ForeignKey(Hospital, on_delete=models.SET_NULL, related_name='hospital', null=True, blank=True)

    def __str__(self):
        return "{username}'s Info".format(username=self.user)


@receiver(post_save, sender=User)
def create_user_information(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
