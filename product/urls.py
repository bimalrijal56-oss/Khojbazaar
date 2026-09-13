from django.urls import path
from .views import *

urlpatterns = [
    path('profile',vendor_profile,name='vendor-profile'),
    path('dashboard',vendor_dashboard,name='vendor-dashboard'),
    path('add-category',add_category,name='add-category'),
    path('all-category',all_category,name='all-category'),
    path('delete-category/<int:category_id>',delete_category,name='delete-category'),
    path('update-category/<int:category_id>',update_category,name='update-category'),
    
    path('add-product',add_product,name='add-product'),
    path('all-product',all_product,name='all-product'),
    path('delete-product/<int:product_id>',delete_product,name='delete-product'),
    path('update-product/<int:product_id>',update_product,name='update-product'),
]