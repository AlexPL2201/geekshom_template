from datetime import timedelta

from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from django.utils.timezone import now
from django.dispatch import receiver
from django.db.models.signals import post_save


class User(AbstractUser):
    image = models.ImageField(upload_to='users_image',blank=True)
    age = models.PositiveIntegerField(default=18)

    activation_key = models.CharField(max_length=128, blank=True)
    activation_key_expires = models.DateTimeField(auto_now=True, blank=True, null=True)


    def is_activation_key_expires(self):
        if now() <= self.activation_key_expires + timedelta(hours=48):
            return False
        return True


class UserProfile(models.Model):
    male = 'm'
    female = 'f'
    gender_choices = ((male, 'М'), (female, 'Ж'))

    user = models.OneToOneField(User, unique=True, null=True, db_index=True, on_delete=models.CASCADE)
    about = models.TextField(verbose_name='О себе', blank=True, null=False)
    gender = models.CharField(verbose_name='Пол', choices=gender_choices, blank=True, max_length=2)
    langs = models.CharField(verbose_name='язык',blank=True,max_length=5,default='RU')

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, created, **kwargs):
        if not created:
            instance.userprofile.save()