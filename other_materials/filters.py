import django_filters
from django import forms
from .models import CategoryStock,CategoryStockOut,DISTRICT_CHOICES

class CategoryStockFilter(django_filters.FilterSet):

    category = django_filters.CharFilter(
        field_name='category__name',
        lookup_expr='icontains',
        label="Kategori",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Kategori ara...'
        })
    )

    material_name = django_filters.CharFilter(
        lookup_expr='icontains',
        label="Malzeme Adı",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Malzeme ara...'
        })
    )

    min_quantity = django_filters.NumberFilter(
        field_name="quantity",
        lookup_expr='gte',
        label="Minimum Miktar",
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    max_quantity = django_filters.NumberFilter(
        field_name="quantity",
        lookup_expr='lte',
        label="Maximum Miktar",
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = CategoryStock
        fields = ['category', 'material_name']

class CategoryStockOutFilter(django_filters.FilterSet):

    well_number = django_filters.CharFilter(
        lookup_expr='icontains',
        label="Kuyu No",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Kuyu numarası ara...'
        })
    )

    # ✅ SELECT OLDU
    district = django_filters.ChoiceFilter(
        choices=DISTRICT_CHOICES,
        label="İlçe",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    address = django_filters.CharFilter(
        lookup_expr='icontains',
        label="Adres",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Adres ara...'
        })
    )

    material_name = django_filters.CharFilter(
        field_name='stock__material_name',
        lookup_expr='icontains',
        label="Malzeme",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Malzeme ara...'
        })
    )

    category = django_filters.CharFilter(
        field_name='stock__category__name',
        lookup_expr='icontains',
        label="Kategori",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Kategori ara...'
        })
    )

    class Meta:
        model = CategoryStockOut
        fields = []