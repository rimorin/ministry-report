from unicodedata import name
from django.db import models

# Create your models here.
class Congregation(models.Model):
    code = models.CharField(max_length=24)
    name = models.CharField(max_length=52)

    def __str__(self):
        return f"{self.id} - {self.name}"


class Group(models.Model):
    congregation = models.ForeignKey(
        "congregation.Congregation", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=52)
    language = models.CharField(max_length=52, null=True, blank=True)

    def __str__(self):
        return f"{self.congregation.code} - {self.name}"


class Publisher(models.Model):
    group = models.ForeignKey("congregation.Group", on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=256)
    status = models.CharField(
        max_length=5, choices=(("0", "Inactive"), ("1", "Active"))
    )
    regular_pioneer = models.BooleanField(default=False)
    ministerial_servant = models.BooleanField(default=False)
    elder = models.BooleanField(default=False)
    contact_number = models.CharField(max_length=24, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    remarks = models.TextField(max_length=5000, null=True, blank=True)

    def __str__(self):
        return self.name
