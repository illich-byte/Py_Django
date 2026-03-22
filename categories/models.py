# Create your models here.
import uuid
from django.db import models
# from .util import upload_image
# from django_resized import ResizedImageField

class Category(models.Model):
    name = models.CharField(
        max_length=100, 
        unique=True
    )
    description = models.TextField(
        blank=True
    )
    slug = models.SlugField(
        max_length=255, 
        null=True, 
        blank=True
    )
    # image = models.ImageField(
    #     upload_to='images/',
    #     null=True,
    #     blank=True
    # )
    # image = ResizedImageField(
    #     size=[600, 600],
    #     quality=90,
    #     force_format='WEBP',
    #     upload_to=upload_image,
    #     null=True,
    #     blank=True
    # )
    image = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name
    


