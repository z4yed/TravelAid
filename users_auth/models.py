from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver
from ckeditor_uploader.fields import RichTextUploadingField

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


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_info')
    full_name = models.CharField(max_length=100, null=True, blank=True)
    cell = models.CharField(max_length=11, null=True, blank=True)
    address = models.CharField(max_length=200)
    profile_picture = models.ImageField(default='default.jpg', upload_to='profile_pics', null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='update_profile', null=True, blank=True)
    description = RichTextUploadingField(null=True, blank=True)

    def __str__(self):
        return "{username}'s Info".format(username=self.user)


@receiver(post_save, sender=User)
def create_user_information(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
