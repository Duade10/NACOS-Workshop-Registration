from django.contrib import admin
from . import models


class TicketAdmin(admin.ModelAdmin):
    list_display = ("user", "reference")


admin.site.register(models.Ticket, TicketAdmin)
