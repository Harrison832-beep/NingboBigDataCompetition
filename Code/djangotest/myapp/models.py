from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField(primary_key=True, max_length=255)
    password = models.CharField(max_length=255)
    realname = models.CharField(max_length=255)
    passport = models.CharField(unique=True, max_length=255)
    phone = models.CharField(unique=True, max_length=11)
    email = models.CharField(unique=True, max_length=255)
    wechat = models.CharField(max_length=255, blank=True, null=True)
    shipaddress = models.CharField(max_length=255, blank=True, null=True)
    idnumber = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'
