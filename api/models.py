from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    is_camper = models.BooleanField(default=False)
    is_organizer = models.BooleanField(default=False)
    is_approver = models.BooleanField(default=False)
    phone = models.CharField(max_length=12, default='')

class UserImage(models.Model):
    user = models.ForeignKey(User, related_name='image', on_delete=models.CASCADE, default='')
    imgpath = models.TextField(max_length=None)

    class Meta:
        ordering = ['user']
    
    def __str__(self):
        return '%s' % (self.imgpath)

class UserEvent(models.Model):
    user = models.ForeignKey(User, related_name='event', on_delete=models.CASCADE, default='')
    organizer = models.CharField(max_length=255)
    location = models.TextField(max_length=None)
    duration = models.TextField(max_length=None)
    event_name = models.CharField(max_length=255, default='', unique=True)
    event_image = models.TextField(max_length=None)
    detail = models.TextField(max_length=None)
    approved_by = models.CharField(max_length=255, default='none')

    class Meta:
        ordering = ['organizer']


class UserRegisterEvent(models.Model):
    event = models.ForeignKey(UserEvent, related_name='register_user', on_delete=models.CASCADE,  default='')
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE,  default='')

    class Meta:
        ordering = ['event']

class EventHistory(models.Model):
    event = models.ForeignKey(UserRegisterEvent, related_name='event_user', on_delete=models.CASCADE, default='')
    status = models.CharField(max_length=255, default='')
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['event']

    
