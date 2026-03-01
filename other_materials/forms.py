from django import forms
from django.forms import ModelForm
from .models import CategoryStock,Category,CategoryStockOut
from django.db import transaction
from django.db.models import F

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['name',]
        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Kategori'}),
        }
    def clean_name(self):
        name = self.cleaned_data.get('name').upper()
        
        if Category.objects.filter(name=name).exists():
            raise forms.ValidationError(f"*{name}* Bu Kategori zaten mevcut.")
        
        return name

class CategoryStockForm(forms.ModelForm):
    class Meta:
        model = CategoryStock
        fields = ["category", "material_name", "quantity"]
        labels = {
            "category": "Kategori",
            "material_name": "Malzeme Adı",
            "quantity": "Miktar",
        }
        widgets = {
            "category": forms.Select(attrs={"class": "form-select select2"}),
            "material_name": forms.TextInput(attrs={"class": "form-control"}),
            "quantity": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
        }

    def clean_material_name(self):
        # boşlukları kaldır ve büyük harfe çevir
        return self.cleaned_data["material_name"].upper()

    def save(self, commit=True):
        """
        Aynı kategori + malzeme varsa miktarı toplar,
        yoksa yeni kayıt oluşturur.
        """
        category = self.cleaned_data['category']
        material_name = self.cleaned_data['material_name']
        quantity_to_add = self.cleaned_data['quantity']

        with transaction.atomic():
            stock = CategoryStock.objects.select_for_update().filter(
                category=category,
                material_name=material_name
            ).first()

            if stock:
                stock.quantity = F('quantity') + quantity_to_add
                if commit:
                    stock.save()
                return stock
            else:
                stock = super().save(commit=commit)
                return stock

class CategoryStockOutForm(forms.ModelForm):
    class Meta:
        model = CategoryStockOut
        fields = [ 'stock', 'quantity']
        widgets = {
            'stock': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        stock = cleaned_data.get("stock")
        quantity = cleaned_data.get("quantity")

        if stock and quantity:
            if stock.quantity < quantity:
                raise forms.ValidationError("Yetersiz stok miktarı! ")

        return cleaned_data