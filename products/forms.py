from django import forms
from .models import Category, City, Product

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control custom-input', 
                'placeholder': 'Введіть назву категорії'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control custom-textarea', 
                'rows': 3,
                'placeholder': 'Короткий опис'
            }),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) < 3:
            raise forms.ValidationError("Назва категорії повинна мати хоча б 3 символи")
        return name

class CityForm(forms.ModelSerializer):
    class Meta:
        model = City
        fields = ['name', 'region']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Назва міста'}),
            'region': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Область'}),
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'