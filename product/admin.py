from django.contrib import admin
from.models import *

# Register your models here.

class AdminCategory(admin.ModelAdmin):
    list_display=['name','created_at']

admin.site.register(Category,AdminCategory)

class AdminProduct(admin.ModelAdmin):
    list_display=['title','actual_price','trending','stock','created_at']
    
    
admin.site.register(Product)