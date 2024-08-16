from django.db import models

# Create your models here.

class TemporaryData(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=150)
    pin = models.IntegerField()
    conformation = models.BooleanField()
    code = models.IntegerField()



class UserNamePassword(models.Model):
    email = models.EmailField( max_length=254)
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    pin = models.IntegerField()

