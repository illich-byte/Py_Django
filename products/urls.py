from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.show_products, name='show_products'),
    path('add/', views.add_product, name='add_product'),
    path('edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete/<int:product_id>/', views.delete_product, name='delete_product'),
    
    # Зображення
    path("upload_temp_image/", views.upload_temp_image, name="upload_temp_image"),
    path("delete_temp_image/", views.delete_temp_image, name="delete_temp_image"),
    
    # Категорії
    path('category/add/', views.add_category, name='add_category'),
    
    # API Міст
    path('api/cities/', views.CityListCreateAPI.as_view(), name='city_api'),
]
