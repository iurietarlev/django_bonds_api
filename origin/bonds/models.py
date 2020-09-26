from django.db import models
from django.contrib.auth.models import User


class Bond(models.Model):
    owner = models.ForeignKey(
        User, related_name='bonds', on_delete=models.CASCADE, null=True)
    isin = models.CharField(max_length=200)
    size = models.IntegerField()
    currency = models.CharField(max_length=3)
    maturity = models.DateField()
    lei = models.CharField(max_length=20)
    legal_name = models.CharField(max_length=200)
