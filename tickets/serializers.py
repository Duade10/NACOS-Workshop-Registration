from rest_framework.serializers import ModelSerializer
from . import models


class TicketSerializer(ModelSerializer):
    class Meta:
        model = models.Ticket
        fields = "__all__"
