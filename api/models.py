from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    phone = models.CharField(max_length=12, default='')

class Image(models.Model):
    user = models.ForeignKey(User, related_name='image', on_delete=models.CASCADE, default='')
    imgpath = models.TextField(max_length=None)

    class Meta:
        unique_together = ['user', 'imgpath']
        ordering = ['imgpath']
    
    def __str__(self):
        return '%s' % (self.imgpath)
    
