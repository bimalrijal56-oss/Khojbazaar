from django.db import models

# Create your models here.

class Category(models.Model):
    name=models.CharField(max_length=50,unique=True)
    description=models.TextField(blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
            return self.name
    
    
class Product(models.Model):
    category =models.ForeignKey(Category,on_delete=models.CASCADE)
    title=models.CharField(max_length=100)
    actual_price=models.DecimalField(max_digits=12,decimal_places=2)
    discount_price=models.DecimalField(max_digits=12,decimal_places=2)
    tag=models.CharField(max_length=50)
    trending=models.BooleanField(default=False)
    image=models.ImageField(upload_to='static/uploads/')
    description=models.TextField()
    stock=models.IntegerField()
    created_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    