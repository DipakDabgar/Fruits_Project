"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('cart', views.cart, name='cart'),
    path('add_to_cart/<int:id>', views.add_to_cart, name='add_to_cart'),
    path('shop_add_to_card/<int:id>', views.shop_add_to_card, name='shop_add_to_card'),
    path('checkout', views.checkout, name='checkout'),
    path('contact', views.contact, name='contact'),
    path('error404', views.error404, name='error404'),
    path('shop_detail', views.shop_detail, name='shop_detail'),
    path('shop_detail1/<int:id>', views.shop_detail1, name='shop_detail1'),
    path('shop', views.shop, name='shop'),
    path('testimonial', views.testimonial, name='testimonial'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    
    path('forget', views.forget, name='forget'),
    path('confirm_password', views.confirm_password, name='confirm_password'),
    path('register', views.register, name='register'),
    path('cart_mines/<int:id>', views.cart_mines, name='cart_mines'),
    path('cart_plus/<int:id>', views.cart_plus, name='cart_plus'),
    path('delete1/<int:id>', views.delete1, name='delete1'),
    path('billing_view', views.billing_view, name='billing_view'),
    
    path('checkout', views.checkout, name='checkout'),
    path('show_orders', views.show_orders, name='show_orders'),
    
    
    path('order_delete/<int:id>', views.order_delete, name='order_delete'),
    path('apply_coupon', views.apply_coupon, name='apply_coupon'),
    path('filter_price', views.filter_price, name='filter_price'),
    path('price1', views.price1, name='price1'),
    path("Whishlist",views.Whishlist,name="Whishlist"),
    path("add_whishlist/<int:id>",views.add_whishlist,name="add_whishlist"),
    path("remove_whishlist/<int:id>",views.remove_whishlist,name="remove_whishlist"),   
    path('search', views.search, name='search'),
    # path('', views.login, name='index'),
]
