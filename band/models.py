from __future__ import unicode_literals

from django.db import models


# Create your models here.
class PicDirectory(models.Model):
    filename = models.CharField(max_length=40)
    image = models.ImageField(upload_to='images/diseaseImage')
