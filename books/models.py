from datetime import datetime
from decimal import Decimal
from django.contrib.auth.models import User
from django.core.validators import RegexValidator, MinValueValidator
from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=250)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    class_valid = RegexValidator(regex=r'^[A-Z]{2,4} 0+[0-9]+$', message="Please enter class in the form of XXXX #### (e.x. PHY 0011)")
    class_id = models.CharField(max_length=20, validators=[class_valid])
    edition = models.IntegerField(validators=[MinValueValidator(1)])
    price = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(Decimal('0'))])
    details = models.CharField(max_length=500, null=True, blank=True)
    posted = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.title + ' - ' + self.seller.username
