from django.db import models
from core.models import AbstractTimeStampedModel
from django.utils.text import slugify


class Skill(AbstractTimeStampedModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
