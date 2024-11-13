from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.hashers import make_password, check_password
# Create your models here.
class Forms(models.Model):
    # name=models.CharField(max_length=122)
    email=models.EmailField()
    message=models.TextField()






class Events_Ticket(models.Model):
    name=models.CharField(max_length=1000)
    date=models.DateField()
    time=models.CharField(max_length=100)
    venue=models.CharField(max_length=100)
    ticket_available=models.IntegerField()
    image = models.ImageField(upload_to='images/')
    

class User(models.Model):
    username=models.EmailField(unique=True)
    password=models.CharField(max_length=20)

class Event_Bookings(models.Model):
    name=models.CharField(max_length=1000)
    date=models.DateField()
    time=models.CharField(max_length=100)
    venue=models.CharField(max_length=100)
    ticket_no=models.CharField(max_length=11)
    ticket_count=models.IntegerField()
    user=models.ForeignKey(User,on_delete=models.CASCADE)

class TurfBooking(models.Model):
    game=models.CharField(max_length=100)
    turf_type=models.CharField(max_length=100)
    date=models.DateField()
    time=models.CharField(max_length=100)
    ticket_no=models.CharField(max_length=11)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
      
#     # ######
    
    # def save(self, *args, **kwargs):
    #     # Hash the password before saving
    #     if self.pk is None or self.password != self.__original_password:
    #         self.password = make_password(self.password)
    #     super().save(*args, **kwargs)

    # def check_password(self, raw_password):
    #     return check_password(raw_password, self.password)

