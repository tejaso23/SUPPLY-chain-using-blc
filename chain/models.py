from email.policy import default
from enum import unique
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class ChainUser(AbstractUser):
    first_name=models.CharField(max_length=10)
    last_name=models.CharField(max_length=10)
    # fullname=models.CharField(max_length=10)
    user_kyc = models.CharField(max_length=15, default="")
    user_address=models.CharField(max_length=60, default=False)
    phoneno = models.CharField(max_length=13, default=False)
    email=models.CharField(max_length=50)    
    username=models.CharField(max_length=20, unique=True)    
    password=models.CharField(max_length=50)
    userimg=models.ImageField(upload_to='User/images', default="")
    is_purchaser= models.BooleanField('Is admin', default=False)
    is_distributor = models.BooleanField('Is distributor', default=False)
    is_retailor = models.BooleanField('Is retailor', default=False)


class cropImage(models.Model):
    fid = models.CharField(max_length=50)
    cropname=models.CharField(max_length=50)
    image=models.ImageField(upload_to='crop/images', default="")

    def __str__(self):
        return self.cropname

class Product(models.Model):
    product_id = models.CharField(max_length=10, default=0)
    cropused = models.CharField(max_length=50, default="")
    farmer_name = models.CharField(max_length=50, default="") 
    farmer_address = models.CharField(max_length=200, default="") 
    product_name = models.CharField(max_length=50, default="")
    product_price = models.IntegerField(default=0)
    product_category = models.CharField(max_length=50, default="")
    manu_date = models.DateField()
    subcategory = models.CharField(max_length=50, default="")
    product_qt = models.IntegerField(default=0)
    desc = models.CharField(max_length=1000)
    process_used = models.CharField(max_length=300, default="")
    image = models.ImageField(upload_to='veggies/images', null=True, blank=True)
    def __str__(self):
        return self.product_name


class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    items_json = models.CharField(max_length=5000)
    amount = models.IntegerField( default=0)
    name = models.CharField(max_length=90)
    email = models.CharField(max_length=111)
    address = models.CharField(max_length=111)
    city = models.CharField(max_length=111)
    state = models.CharField(max_length=111)
    zip_code = models.CharField(max_length=111)
    phone = models.CharField(max_length=111, default="")


class OrderUpdate(models.Model):
    update_id  = models.AutoField(primary_key=True)
    order_id = models.IntegerField(default="")
    update_desc = models.CharField(max_length=5000)
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.update_desc[0:7] + "..."


class ExcelFileUpload(models.Model):
    excel_file_upload = models.FileField(upload_to="excel")