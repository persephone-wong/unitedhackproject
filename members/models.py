from django.db import models

# Create your models here.


class User(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    departure_time = models.TimeField()
    arrival_time = models.TimeField()
    start_address = models.TextField()
    arrival_address = models.TextField()

