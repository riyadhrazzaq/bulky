from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class BulkEmail(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    sender = models.EmailField(verbose_name="From")
    receiver = models.JSONField(verbose_name='Receipients')
    subject = models.CharField(verbose_name="Subject", max_length=75)
    content = models.TextField(blank=True)
    date = models.DateTimeField(default=None)
