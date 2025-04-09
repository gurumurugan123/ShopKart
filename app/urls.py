from django.urls import path
from . import views

urlpatterns = [ 
    path('', views.home, name="home"),
    path('login/', views.login_page, name="login"),
    path('logout/', views.logout_page, name="logout"),
    path('cart/', views.cart_page, name="cartpage"),

    path('register/',views.register, name="register"),
    path('collection/',views.collection, name="collection"),  # Changed name to "collection"
    path('collection/<str:name>',views.collectionview, name="collectionview"),
    path('collection/<str:cname>/<str:pname>',views.collectionproduct, name="collectionproduct"),
    path('addtocart/',views.add_to_cart,name="addtocart")
]
