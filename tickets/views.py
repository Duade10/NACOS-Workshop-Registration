from django.views.generic import DetailView
from rest_framework.views import APIView
from rest_framework.response import Response
from . import models, serializers


class TicketDetailView(DetailView):
    model = models.Ticket
    template_name = "tickets/ticket.html"
    context_object_name = "ticket"

    def get_object(self):
        return models.Ticket.objects.get(id=self.kwargs["id"])


class TicketCreate(APIView):
    def post(self, request, *args, **kwargs):
        user = request.user
        reference = request.data.get("order_id")
        ticket = models.Ticket.objects.create(user=user, reference=reference)
        ticket.draw_qr_code(self.request)
        serializer = serializers.TicketSerializer(ticket)
        return Response(serializer.data)
