from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .access import vendor_only

# Create your views here.
@vendor_only
@login_required
def vendor_profile(request):
     return render(request,'vendor/profile.html')

@vendor_only
@login_required
def vendor_dashboard(request):
     return render(request,'vendor/dashboard.html')

@vendor_only
@login_required
def add_category(request):
     if request.method == 'POST':
          form = CategoryForm(request.POST)
          if form.is_valid():
               form.save()
               messages.success(request,'Category added successfully')
               return redirect('all-category')
          else:
               messages.error(request,'Failed to add category')
               return render(request,'vendor/addcategory.html',{'form':form})
     context ={
          'form' : CategoryForm
     }
     return render(request,'vendor/addcategory.html',context)

@vendor_only
@login_required
def all_category(request):
     context = {
          'categories' : Category.objects.all()
     }
     return render(request,'vendor/allcategory.html',context)

@vendor_only
@login_required
def add_product(request):
     if request.method == 'POST':
          form = ProductForm(request.POST, request.FILES)
          if form.is_valid():
               form.save()
               messages.success(request,'Product added successfully')
               return redirect('all-product')
          else:
               messages.error(request,'Failed to add product')
               return render(request,'vendor/addproduct.html',{'form':form})
     context ={
          'form' : ProductForm
     }
     return render(request,'vendor/addproduct.html',context)

@vendor_only
@login_required
def all_product(request):
     context = {
          'products' : Product.objects.all()
     }
     return render(request,'vendor/allproduct.html',context)

@vendor_only
@login_required
def delete_category(request,category_id):
     category = Category.objects.get(id=category_id)
     category.delete()
     messages.success(request,'Category deleted successfully')
     return redirect('all-category')

@vendor_only
@login_required
def update_category(request,category_id):
     category = Category.objects.get(id = category_id)
     if request.method == "POST":
          form = CategoryForm(request.POST,instance=category)
          if form.is_valid():
               form.save()
               messages.success(request,'Category updated successfully')
               return redirect('all-category')
          else:
               messages.error(request,'Failed to update category')
               return render(request,'vendor/updatecategory.html',{'form':form})
     context = {
          'form': CategoryForm(instance = category)
     }     
     return render(request,'vendor/updatecategory.html',context)



@vendor_only
@login_required
def delete_product(request,product_id):
     product = Product.objects.get(id=product_id)
     product.delete()
     messages.success(request,'Product deleted successfully')
     return redirect('all-product')

@vendor_only
@login_required
def update_product(request,product_id):
     product = Product.objects.get(id = product_id)
     if request.method == "POST":
          form = ProductForm(request.POST,request.FILES, instance=product)
          if form.is_valid():
               form.save()
               messages.success(request,'Product updated successfully')
               return redirect('all-product')
          else:
               messages.error(request,'Failed to update product')
               return render(request,'vendor/updateproduct.html',{'form':form})
     context = {
          'form': ProductForm(instance = product)
     }     
     return render(request,'vendor/updateproduct.html',context)