from django.urls import path
from . import views

app_name = "tickets"

urlpatterns = [
    path("detail/<str:id>/", views.TicketDetailView.as_view(), name="detail"),
    path("create", views.TicketCreate.as_view(), name="create"),
]
