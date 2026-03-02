from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
   
   email = models.EmailField(unique=True)
   phone = models.IntegerField(blank=True,null=True)
   adress = models.CharField(max_length=50,blank=True,null=True)

   USERNAME_FIELD = 'email'
   REQUIRED_FIELDS = ['username']

   def __str__(self):
      
      return self.email

