import os
import uuid
import json
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.files.base import ContentFile
from PIL import Image
from io import BytesIO

from rest_framework import generics
from .serializers import CitySerializer, CategorySerializer, DepartmentSerializer
from .models import Product, ProductImage, Category, City, Department
from .forms import ProductForm, CategoryForm
class DepartmentListAPI(generics.ListAPIView):
    serializer_class = DepartmentSerializer
    def get_queryset(self):
        queryset = Department.objects.all()
        city_id = self.request.query_params.get('city_id')
        if city_id:
            queryset = queryset.filter(city_id=city_id)
        return queryset
# --- API ДЛЯ REACT (RTK QUERY) ---
class CityListCreateAPI(generics.ListCreateAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer

class CategoryUpdateAPI(generics.RetrieveUpdateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class DepartmentListAPI(generics.ListAPIView):
    serializer_class = DepartmentSerializer
    def get_queryset(self):
        queryset = Department.objects.all()
        city_id = self.request.query_params.get('city_id')
        if city_id:
            queryset = queryset.filter(city_id=city_id)
        return queryset

# --- КАТЕГОРІЇ ТА ПРОДУКТИ ---
def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('products:show_products') 
    else:
        form = CategoryForm()
    return render(request, "add_category.html", {"form": form})

def show_products(request):
    products = Product.objects.prefetch_related("images").all()
    return render(request, 'products.html', {'products': products})

def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        images_ids = request.POST.getlist('images')
        if form.is_valid():
            product = form.save()
            for idx, img_id in enumerate(images_ids):
                img = ProductImage.objects.get(id=img_id)
                img.product = product
                img.priority = idx
                img.save()
            return redirect("products:show_products")
    else:
        form = ProductForm()
    return render(request, "add_product.html", {"form": form})

# --- ЗАВАНТАЖЕННЯ З ОБРІЗКОЮ (CROP) ---
@csrf_exempt
def upload_temp_image(request):
    if request.method == "POST":
        file_key = list(request.FILES.keys())[0]
        image_file = request.FILES[file_key]
        
        img_image = Image.open(image_file)
        
        # Центрична обрізка до квадрата
        width, height = img_image.size
        min_side = min(width, height)
        left = (width - min_side) / 2
        top = (height - min_side) / 2
        right = (width + min_side) / 2
        bottom = (height + min_side) / 2
        img_image = img_image.crop((left, top, right, bottom))
        img_image = img_image.resize((800, 800), Image.LANCZOS)

        if img_image.mode in ("RGBA", "P"):
            img_image = img_image.convert("RGB")

        filename = f"{uuid.uuid4().hex}.webp"
        buffer = BytesIO()
        img_image.save(buffer, format="WEBP", quality=85)
        buffer.seek(0)
        
        img = ProductImage()
        img.image.save(filename, ContentFile(buffer.read()), save=True)
        return JsonResponse({"file_id": img.id})

@csrf_exempt
def delete_temp_image(request):
    if request.method == "DELETE":
        data = json.loads(request.body)
        file_id = data.get("file_id")
        if file_id:
            img = ProductImage.objects.get(id=file_id, product__isnull=True)
            if img.image and os.path.isfile(img.image.path):
                os.remove(img.image.path)
            img.delete()
            return JsonResponse({"status": "ok"})
    return JsonResponse({"error": "Invalid request"}, status=400)