"""
URL configuration for Onlineshop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from os import name
from urllib import request
from django.contrib import admin
from django.urls import path
from store_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('order_complete', views.order_complete, name='order_complete'),
    path('place_order', views.place_order, name='bplace_orderase'),
    path('<slug:category_slug>/<slug:product_slug>', views.product_detail, name='product_detail'),
    path('store/<slug:category_slug>/', views.store, name='store'),
    path('store/', views.store, name='store'),
    path('search_result', views.search_result, name='search_result'),
    path('home', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('admin_index/', views.admin_index, name="admin_index"),
    path('admin_index/update/', views.update_applications, name='update_applications'),
    path('adminastor', views.a, name='a'),
    path('add-news/', views.add_news, name='add_news'),
    path('news/', views.news, name='news'),
    path('turul/', views.admin_category, name='category'),
    path('user/', views.admin_user, name='user'),
    path('zar/', views.admin_zar, name='zar'),
    path('about/', views.about, name='about'),
    path('request/', views.admin_request, name='request')
    ]
