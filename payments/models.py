import requests
from django.db import models

from core.models import AbstractTimeStampedModel
from django.conf import settings


class Payment(AbstractTimeStampedModel):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    ticket = models.ForeignKey("tickets.Ticket", on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    gateway_ref = models.CharField(max_length=100, null=True)
    amount_paid = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.payment_id
