from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from . import models


class LoggedInOnlyView(LoginRequiredMixin):
    login_url = reverse_lazy("users:sign_up")


class LoggedOutOnlyView(UserPassesTestMixin):
    def test_func(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        messages.error(self.request, "Permission Denied!")
        try:
            url = self.request.META.get("HTTP_REFERER")
            return redirect(url)
        except TypeError:
            url = "users:sign_up"
            return redirect(url)


class EmailUserOnlyView(UserPassesTestMixin):
    def test_func(self) -> bool:
        user = self.request.user
        return user.login_method == models.User.LOGIN_EMAIL or user.login_method == None

    def handle_no_permission(self) -> HttpResponseRedirect:
        messages.error(self.request, "Permission Denied!")
        try:
            url = self.request.META.get("HTTP_REFERER")
            return redirect(url)
        except TypeError:
            url = "core:index"
            return redirect(url)
