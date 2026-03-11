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
        return self.cleaned_data["material_name"].strip().upper()

    def save(self, commit=True):
        material_name = self.cleaned_data["material_name"]
        category = self.cleaned_data["category"]
        quantity = self.cleaned_data["quantity"]

        if self.instance.pk:
            # Düzenleme durumunda sadece quantity güncellenir
            self.instance.quantity = quantity
            if commit:
                self.instance.save()
            return self.instance
        else:
            # Yeni ekleme durumunda daha önce var mı kontrol et
            existing = CategoryStock.objects.filter(
                category=category,
                material_name=material_name
            ).first()
            
            if existing:
                # Mevcut kayıt varsa quantity ekle
                existing.quantity = F('quantity') + quantity
                if commit:
                    existing.save()
                    # F() kullanımı sonrası güncel değeri almak için refresh
                    existing.refresh_from_db()
                return existing
            else:
                # Yoksa yeni kayıt oluştur
                return super().save(commit=commit)
            
class CategoryStockOutForm(forms.ModelForm):
    class Meta:
        model = CategoryStockOut
        fields = [
            'outlet_plug',
            'well_number',
            'district',
            'address',
            'stock',
            'quantity'
        ]
        widgets = {
            'outlet_plug': forms.NumberInput(attrs={'class': 'form-control'}),
            'well_number': forms.TextInput(attrs={'class': 'form-control'}),
            'district': forms.Select(attrs={'class': 'form-select'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'stock': forms.Select(attrs={'class': 'form-select select2'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        stock = cleaned_data.get("stock")
        quantity = cleaned_data.get("quantity")

        if not stock or not quantity:
            return cleaned_data

        # Düzenleme durumunda eski quantity'i hesaba kat
        if self.instance and self.instance.pk:
            old_quantity = self.instance.quantity or 0
            available_stock = stock.quantity + old_quantity
        else:
            available_stock = stock.quantity

        if quantity > available_stock:
            raise forms.ValidationError("Yetersiz stok miktarı!")

        return cleaned_data

class CategoryStockOut2Form(forms.ModelForm):
    class Meta:
        model = CategoryStockOut
        fields = [
            'stock',
            'quantity'
        ]
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