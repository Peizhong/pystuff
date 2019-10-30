from django.db import models

# Create your models here.
# python manage.py makemigrations days
# python manage.py migrate

class Entry(models.Model):
    text = models.TextField(blank=True, null=True)
    date_time = models.DateTimeField()
    location = models.CharField(max_length=1024, null=True, blank=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=6)
    longitude = models.DecimalField(max_digits=10, decimal_places=6)
    weather = models.CharField(max_length=512, null=True, blank=True)
    picture = models.CharField(max_length=1024, null=True, blank=True)