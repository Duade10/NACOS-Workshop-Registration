from io import BytesIO

import qrcode
from django.core.files import File
from django.db import models
from django.urls import reverse
from PIL import Image, ImageDraw
from shortuuidfield import ShortUUIDField
from django.contrib.sites.shortcuts import get_current_site


from core.models import AbstractTimeStampedModel


class Ticket(AbstractTimeStampedModel):
    user = models.OneToOneField("users.User", verbose_name="ticket", on_delete=models.CASCADE)
    qr_code = models.ImageField(upload_to="tickets/qr_code", null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    reference = models.CharField(max_length=255, null=True, blank=True)
    uuid = ShortUUIDField()
    # payment = models.ForeignKey()

    def __str__(self):
        return "Ticket"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("ticket:detail", kwargs={"id": self.id})

    def draw_qr_code(self, request):
        domain = get_current_site(request)
        self.url = f"http://{domain}/tickets/detail/{self.id}"
        qrcode_img = qrcode.make(self.url)
        canvas = Image.new("RGB", (400, 400), "white")
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        file_name = f"QR_CODE{self.user.get_full_name()}.png"
        buffer = BytesIO()
        canvas.save(buffer, "PNG")
        self.qr_code.save(file_name, File(buffer), save=False)
        canvas.close
        self.save()
