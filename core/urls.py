from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.PaymentView.as_view(), name="payment"),
    path("ticket/", views.TicketView.as_view(), name="ticket"),
]
