from django.db import models
from django.core.validators import FileExtensionValidator
from django.conf import settings


class Vehicle(models.Model):
    image = models.ImageField(upload_to=settings.VEHICLES_MEDIA_LOCATION,
                              validators=[
                                  FileExtensionValidator(allowed_extensions=(['png', 'jpg', 'jpeg']))],
                              blank=False,
                              null=False
                              )
    vehicle_coords = models.CharField(max_length=100, null=True, blank=True)
    plate_coords = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
