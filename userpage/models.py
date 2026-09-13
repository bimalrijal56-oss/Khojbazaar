from django.db import models
from django.core.validators import MinLengthValidator
from django_ckeditor_5.fields import CKEditor5Field
from product.models import *
from django.contrib.auth.models import User
# Create your models here.

class Setting(models.Model):
    title = models.CharField(max_length=100)
    favicon = models.ImageField(upload_to='static/uploads/')
    logo = models.ImageField(upload_to='static/uploads/')
    bio = CKEditor5Field()
    email = models.EmailField()
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=14,validators=[MinLengthValidator(10)])
    fb_link = models.URLField(blank=True)
    insta_link = models.URLField(blank=True)
    
    def __str__(self):
        return self.title
    
class Cart(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.product.title
    
    
class Order(models.Model):
    STATUS = (('In Progress','In Progress'),('Way to Deliver','Way to Deliver'),('Completed','Completed'))
    PAYMENTS = (('COD','COD'),('Card','Card'))
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total_price = models.DecimalField(decimal_places=2,max_digits=15)
    address = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=14,validators=[MinLengthValidator(10)])   
    payment_method = models.CharField(max_length=100,choices=PAYMENTS)
    payment_status = models.BooleanField(default=False,null=True)
    order_status = models.CharField(max_length=100,choices=STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__ (self):
        return f"{self.user.username},'-',{self.product.title}"
     
    
