from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    path("", views.SignUpView.as_view(), name="sign_up"),
    path("activate/<uidb64>/<token>/", views.ActivateMail.as_view(), name="activate"),
]
