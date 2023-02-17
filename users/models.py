from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.tokens import default_token_generator


# ACCOUNT VERIFICATION IMPORTS
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.db import models
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode
from shortuuidfield import ShortUUIDField


class User(AbstractUser):
    phone_number = models.CharField(max_length=20, null=True)
    skills = models.ManyToManyField("skills.Skill", related_name="users")
    uuid = ShortUUIDField(max_length=18)

    def save(self, *args, **kwargs):
        self.first_name = str.capitalize(self.first_name)
        self.last_name = str.capitalize(self.last_name)
        super().save(*args, **kwargs)

    def get_full_name(self) -> str:
        return super().get_full_name()

    def __str__(self):
        return self.get_full_name()

    def verify_email(self, request):
        current_site = get_current_site(request)
        domain = current_site
        uid = urlsafe_base64_encode(force_bytes(self.uuid))
        token = default_token_generator.make_token(self)
        html_message = render_to_string(
            "users/verification_email.html",
            {"domain": domain, "uidb64": uid, "token": token, "first_name": self.first_name},
        )
        send_mail(
            "Confirm your mail",
            strip_tags(html_message),
            settings.EMAIL_HOST_USER,
            [self.email],
            fail_silently=False,
            html_message=html_message,
        )
        self.save()
