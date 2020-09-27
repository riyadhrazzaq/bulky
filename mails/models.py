from django.db import models

# Create your models here.

class Email(models.Model):
    sender = models.EmailField(verbose_name="From")
    receiver = []
    subject = models.CharField(verbose_name="Subject", max_length=75)
    # content_alternative = models.TextField(verbose_name="Alternative HTML")
    content_plain = models.TextField(blank=True)
    date = models.DateTimeField(default=None)
