from django.db import models

# Create your models here.


class District(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name


class Address(models.Model):
    address = models.CharField(max_length=25, null=True, blank=True)
    district = models.ForeignKey(District, on_delete=models.DO_NOTHING, null=True, blank=True)
    zip_code = models.CharField(max_length=4, null=True, blank=True)

    def __str__(self):
        return "{a}, {b} - {c}".format(a=self.address, b=self.district, c=self.zip_code)

    @property
    def get_full_address(self):
        return "{a}, {b} - {c}".format(a=self.address, b=self.district, c=self.zip_code)