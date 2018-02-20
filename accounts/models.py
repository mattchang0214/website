# Source:
# https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html

from decimal import Decimal
from django.contrib.auth.models import User
from django.core.validators import RegexValidator, MinValueValidator
from django.db import models
from django.db.models.signals import post_save

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id_valid = RegexValidator(regex=r'^[0-9]{7}$', message="Please enter a valid Tufts ID number")
    tufts_id = models.CharField(validators=[id_valid], max_length=7)
    venmo_username = models.CharField(max_length=250)
    phone_valid = RegexValidator(regex=r'^[0-9]{10}$', message="Please enter a valid phone number")
    phone = models.CharField(validators=[phone_valid], max_length=10, blank=True, null=True)
    total = models.DecimalField(default=0, max_digits=5, decimal_places=2, validators=[MinValueValidator(Decimal('0'))])
    # image = models.FileField(upload_to='profile_pic', blank=True, null=True)

    def __str__(self):
        return self.user.username

    def create_profile(sender, created, instance, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    def save_profile(sender, instance, **kwargs):
        if instance.userprofile:
            instance.userprofile.save()

    post_save.connect(create_profile, sender=User)
    post_save.connect(save_profile, sender=User)