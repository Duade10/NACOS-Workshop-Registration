import requests
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.views.generic import FormView

from . import forms, mixins, models


class LoginView(mixins.LoggedOutOnlyView, FormView):
    template_name = "users/login.html"
    form_class = forms.LoginForm

    def form_valid(self, form):
        email = form.cleaned_data.get("email", None)
        password = form.cleaned_data.get("password")
        username = email.split("@")[0]
        user = authenticate(self.request, email=email, username=username, password=password)
        if user is not None:
            user.save()
            login(self.request, user)
        else:
            return redirect(reverse("users:login"))
        url = self.request.GET.get("next")
        return redirect(self.get_success_url())

    def get_success_url(self) -> str:
        messages.success(self.request, f"Welcome {self.request.user.first_name}")
        return self.request.GET.get("next", "/")


class LogoutView(mixins.LoggedInOnlyView, View):
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, "See you later")
        return redirect(reverse("users:login"))


class SignUpView(FormView):
    template_name = "users/signup.html"
    form_class = forms.SignUpForm

    def form_valid(self, form):
        user = form.save()
        email = form.cleaned_data.get("email")
        if user.email == email:
            user.is_active = False
            user.save()
            user.verify_email(self.request)
        return redirect("?command=verification&email=" + email)


class UserDetailView(mixins.LoggedInOnlyView, View):
    def get(self, request, *args, **kwargs):
        current_user = self.request.user
        return render(request, "users/dashboard.html", {"current_user": current_user})


class UserUpdateView(mixins.LoggedInOnlyView, View):
    def get(self, request, *args, **kwargs):
        user = self.request.user
        form = forms.UpdateForm(instance=user)
        context = {"user": user, "form": form}
        return redirect(request, "users/edit_user.html", context)

    def post(self, request, *args, **kwargs):
        form = forms.UpdateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("users:profile")


class ActivateMail(View):
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = models.User._default_manager.get(uuid=uid)
        except (TypeError, ValueError, OverflowError, models.User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            messages.success(request, "Email Verification Activation Successfull")
        return redirect("core:payment")


class ForgotPassword(View):
    def get(self, request, *args, **kwargs):
        return render(request, "users/forgot_password.html")

    def post(self, request, *args, **kwargs):
        email = request.POST["email"]
        if models.User.objects.filter(email=email).exists():
            user = models.User.objects.get(email__exact=email)
            if user.login_method != models.User.LOGIN_EMAIL:
                messages.error(request, f"Invalid Login Method")
                return redirect("users:login")
        else:
            messages.error(request, "Account does not exist")
            return redirect("users:forgot_password")
        return redirect(request, "users:forgot_password.html")


class ValidateResetPasswordView(View):
    def post(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = models.User._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, models.User.DoesNotExist):
            user = None
        if user is not None and default_token_generator.check_token(user, token):
            request.session["uid"] = uid
            messages.success(request, "Please reset your Password")
            return redirect("users:reset_password")
        else:
            messages.error(request, "This reset link has expired.")
            return redirect("users:reset_password")


class ResetPassword(View):
    def get(self, request, *args, **kwargs):
        return render(request, "users/reset_password.html")

    def post(self, request, *args, **kwargs):
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect("user:reset_password")
        else:
            uid = request.session.get("uid")
            user = models.User.objects.get(uuid=uid)
            user.set_password(password)
            user.save()
            messages.success(request, "Password reset successful")
            return redirect("users:login")
        return render(request, "users/reset_password.html")
