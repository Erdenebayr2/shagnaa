from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Account(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    phone_number = models.PositiveIntegerField(null=False)
    date_of_passport = models.DateField(blank=True, null=True)
    licenseid = models.CharField(max_length=255, unique=True, blank=True, null=True)
    passport_image = models.ImageField(upload_to='photos/accounts', blank=True)
    pro_image = models.ImageField(upload_to='photos/accounts', blank=True)
    def __str__(self):
        return self.user.first_name
    
