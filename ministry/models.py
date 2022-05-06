from django.db import models
from datetime import datetime

# Create your models here.
class Report(models.Model):
    publisher = models.ForeignKey("congregation.Publisher", on_delete=models.CASCADE)
    hours = models.IntegerField(default=0)
    return_visits = models.IntegerField(default=0)
    bible_studies = models.IntegerField(default=0)
    placements = models.IntegerField(default=0)
    videos = models.IntegerField(default=0)
    remarks = models.TextField(max_length=5000, null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_change_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.creation_date.month}/{self.creation_date.year} - {self.publisher.name}"
