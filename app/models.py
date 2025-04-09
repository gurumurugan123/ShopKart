from django.db import models
import datetime
import os
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
def gettime(request,filename):
    now=datetime.datetime.now().strftime("%Y%m%d%H:%M%S")
    new_filename="%s%s"%(now,filename)
    return os.path.join('uploads/',new_filename)

class category(models.Model):
    name=models.CharField(max_length=150,null=False,blank=False)
    image=models.ImageField(upload_to=gettime,null=False,blank=False)
    description=models.TextField(max_length=500,null=False,blank=False)
    status=models.BooleanField(default=False,help_text="0-show,1-Hidden")
    create_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
class product(models.Model):
    category=models.ForeignKey(category,on_delete=models.CASCADE)
    name=models.CharField(max_length=150,null=False,blank=False)
    vendor=models.CharField(max_length=150,null=False,blank=False)
    product_image=models.ImageField(upload_to=gettime,null=False,blank=False)
    quantity=models.IntegerField(null=False,blank=False)
    original_price=models.FloatField(null=False,blank=False)
    selling_price=models.FloatField(null=False,blank=False)
    description=models.TextField(max_length=500,null=False,blank=False)
    status=models.BooleanField(default=False,help_text="0-show,1-Hidden")
    trending=models.BooleanField(default=False,help_text="0-default,1-Trending")
    create_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
    
class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(product,on_delete=models.CASCADE)
    product_quantity=models.IntegerField(null=False ,blank=False)
    create_at=models.DateTimeField(auto_now_add=True)
