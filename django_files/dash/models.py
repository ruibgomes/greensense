from django.db import models
from django.utils import timezone

# Create your models here.

class Sensorset(models.Model):
    name = models.CharField(max_length=30)
    ip_address = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    plant = models.CharField(max_length=50)
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class Data(models.Model):
    
    sensorset = models.ForeignKey(Sensorset, on_delete=models.CASCADE)
    temp = models.FloatField()
    humid = models.FloatField()
    soilh = models.FloatField()
    li_vis = models.FloatField()
    li_IR = models.FloatField()
    li_UV = models.FloatField()
    datetime = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.datetime)


