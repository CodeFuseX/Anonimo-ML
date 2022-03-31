from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Session(models.Model):
    patient_username = models.CharField(max_length=1000)
    required_sessions = models.IntegerField(max_length=1000)
    doctor_username = models.CharField(max_length=1000)
    completed_sessions = models.IntegerField(max_length=1000, default=0)


class Report(models.Model):
    patient_username = models.CharField(max_length=1000)
    required_reports = models.IntegerField(max_length=1000)
    completed_reports = models.IntegerField(max_length=1000)