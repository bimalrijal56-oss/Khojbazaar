from userpage.models import Contact
from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Setting)
class AdminSetting(admin.ModelAdmin):
    list_display = ['title','email','address','phone']
    

admin.site.register(Cart)

admin.site.register(Order)

@admin.register(Contact)
class AdminContact(admin.ModelAdmin):
    list_display =['name','email','created_at']


        