from django.db import models
from django.utils import timezone


class DefaultModel(models.Model):
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.updated = timezone.now()
        super().save(*args, **kwargs)


class Account(models.Model):
    oanda_id = models.CharField(max_length=64)
    balance = models.DecimalField(max_digits=16, decimal_places=5)
