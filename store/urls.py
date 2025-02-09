from django.urls import path
from . import views

urlpatterns = [

    path('', views.store, name='store'),

    path('products/', views.products, name='products'),

    path('about/', views.about, name='about'),

    path('contact/', views.contact, name='contact'),

    path('product/<slug:product_slug>/', views.product_info, name='product-info'),

    path('search/<slug:category_slug>/', views.list_category, name='list-category'),


]