from rest_framework import serializers
from .models import City, Category, Department

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'name', 'region']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class DepartmentSerializer(serializers.ModelSerializer):
    city_name = serializers.ReadOnlyField(source='city.name')
    class Meta:
        model = Department
        fields = ['id', 'number', 'address', 'city', 'city_name']