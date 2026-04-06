from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.show_products, name='show_products'),
    path('add/', views.add_product, name='add_product'),
    
    # Зображення
    path("upload_temp_image/", views.upload_temp_image, name="upload_temp_image"),
    path("delete_temp_image/", views.delete_temp_image, name="delete_temp_image"),
    
    # Категорії
    path('category/add/', views.add_category, name='add_category'),
    
    # API для React RTK Query
    path('api/cities/', views.CityListCreateAPI.as_view(), name='city_api'),
    path('api/category/<int:pk>/', views.CategoryUpdateAPI.as_view(), name='category_update_api'),
    path('api/departments/', views.DepartmentListAPI.as_view(), name='department_api'),