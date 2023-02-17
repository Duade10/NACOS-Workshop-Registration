from django.shortcuts import render
from django.views import View
from skills.models import Skill
from users.forms import SignUpForm
from users.mixins import LoggedInOnlyView


class PaymentView(LoggedInOnlyView, View):
    def get(self, request, *args, **kwargs):
        return render(request, "core/payment.html")


class TicketView(LoggedInOnlyView, View):
    def get(self, request, *args, **kwargs):
        return render(request, "core/ticket.html")
