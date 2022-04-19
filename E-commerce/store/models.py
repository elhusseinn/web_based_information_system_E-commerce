from datetime import datetime
from email.mime import image
from unicodedata import category
from xmlrpc.client import DateTime
from django.db import models
from django.forms import CharField
from django.contrib.auth.models import User
from PIL import Image

import datetime
import os

# Create your models here.

def get_file_path(request,filename):
    original_filename = filename
    nowTime = datetime.datetime.now().strftime('%Y%m%d%H;%M;%S')
    filename ="%s%s" %(nowTime, original_filename)
    return os.path.join('upload/',filename)



class Category(models.Model):
    slug = models.CharField( max_length=150,null=False,blank=False)
    name = models.CharField( max_length=150,null=False,blank=False)
    image = models.ImageField(upload_to=get_file_path, null=True,blank=True)
    description =models.TextField(max_length=500,null=False,blank=False)
    status=models.BooleanField(default=False,help_text="0 = default, 1 = Hidden")
    trending=models.BooleanField(default=False,help_text="0 = default, 1 = Hidden")
    meta_title=models.CharField(max_length=150,null=False,blank=False)
    meta_keywords=models.CharField(max_length=150,null=False,blank=False)
    meta_description =models.TextField(max_length=500,null=False,blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
        
    def save(self, **kwargs):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Product(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    slug = models.CharField( max_length=150,null=False,blank=False)
    name = models.CharField( max_length=150,null=False,blank=False)
    product_image = models.ImageField(upload_to=get_file_path, null=True,blank=True)
    small_description =models.CharField(max_length=260,null=False,blank=False)
    quantity = models.IntegerField(null=False,blank=False)
    description =models.TextField(max_length=500,null=False,blank=False)
    original_price = models.FloatField(null=False,blank=False)
    selling_price = models.FloatField(null=False,blank=False)
    status=models.BooleanField(default=False,help_text="0 = default, 1 = Hidden")
    trending=models.BooleanField(default=False,help_text="0 = default, 1 = Hidden")
    tag = models.CharField(max_length=150,null=False,blank=False)
    meta_title=models.CharField(max_length=150,null=False,blank=False)
    meta_keywords=models.CharField(max_length=150,null=False,blank=False)
    meta_description =models.TextField(max_length=500,null=False,blank=False)
    
    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE) 
    product_qty = models.IntegerField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    