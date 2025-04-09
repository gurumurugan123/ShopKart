from http.client import HTTPResponse
import json
from django.http import JsonResponse
from django.shortcuts import redirect, render
from .models import category,product,Cart# Ensure you're importing your model correctly
from django.contrib import messages
from app.form import customuserform
from django.contrib.auth import authenticate,login,logout
from django.http import JsonResponse
import json
from .models import product, Cart  # Make sure 'product' model is imported
from django.http import JsonResponse
import json
from .models import product, Cart  # ✅ Correct

def home(request):
    products=product.objects.filter(trending=1)
    return render(request, "shop/index.html",{"trending":products})
def cart_page(request):

    if request.user.is_authenticated:
        cart=Cart.objects.filter(user=request.user)
        return render(request,"shop/cart.html",{"cart":cart})
    else:
        return redirect("/")
def add_to_cart(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if request.user.is_authenticated:
            try:
                data = json.loads(request.body)
                product_qty = int(data.get('product_qty'))
                product_id = data.get('pid')

                try:
                    product_status = product.objects.get(id=product_id)

                    if Cart.objects.filter(user=request.user, product_id=product_id).exists():
                        return JsonResponse({'status': 'Product Already in Cart'}, status=200)

                    if product_status.quantity >= product_qty:
                        Cart.objects.create(
                            user=request.user,
                            product=product_status,
                            product_quantity=product_qty  # Use correct field name here
                        )
                        return JsonResponse({'status': 'Product Added to Cart'}, status=200)
                    else:
                        return JsonResponse({'status': 'Product Stock not available'}, status=200)

                except product.DoesNotExist:
                    return JsonResponse({'status': 'Product Not Found'}, status=404)

            except json.JSONDecodeError:
                return JsonResponse({'status': 'Invalid data format'}, status=400)

        else:
            return JsonResponse({'status': 'Login to Add Cart'}, status=401)
    else:
        return JsonResponse({'status': 'Invalid Access'}, status=400)


def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Logged out Successfully!")
    return redirect('/')
def login_page(request):
    if request.user.is_authenticated:
            return redirect('/')
    if request.method=='POST': 
        name=request.POST.get('username')
        pwd=request.POST.get('password')
        user=authenticate(request,username=name,password=pwd)
        if user is not None:
            login(request,user)
            messages.success(request,"Login Successfully!")
            return redirect('/')
        else:
            messages.error(request,"Invalid Username or Password")
            return redirect('/login')
    return render(request, "shop/login.html")

def register(request):
    custom=customuserform()
    if request.method=='POST':
        custom=customuserform(request.POST)
        if custom.is_valid():
            custom.save()
            messages.success(request,"Registration Success You can Login Now..!")
            return redirect('/login')
    return render(request, "shop/register.html",{"custom":custom})

def collection(request):
    # Fetch all category objects from the database
    categories = category.objects.all()  # Fetch all categories (fixed variable name)
    return render(request, "shop/collection.html", {"categories": categories})  # Pass categories to the template
def collectionview(request,name):
    if (category.objects.filter(name=name,status=0)):
        products=product.objects.filter(category__name=name)
        return render(request,"shop/products/index.html",{"products":products,"category_name":name})

    else:
        messages.warning(request,"No Such Category Found!")
        return redirect('collection')
    
def collectionproduct(request,cname,pname):
    if(category.objects.filter(name=cname,status=0)):
        if(product.objects.filter(name=pname,status=0)):
            productsfirst=product.objects.filter(name=pname,status=0).first()
            return render(request,"shop/products/productdetails.html",{"productdetails":productsfirst})
        else: 
            messages.error("No Such Product Found!")
            return redirect('collection')
    else:
        messages.error("No Such Category Found!")
        return redirect('collection')
    
    