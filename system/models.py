from django.db import models

# Create your models here.


class Expertise(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name
