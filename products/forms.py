from django import forms
from .models import Category

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control custom-input', 
                'placeholder': 'Ведіть назву категорії'
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
            raise forms.ValidationError("Назва категорії повинна мати хочаб 3 символи")
        return name