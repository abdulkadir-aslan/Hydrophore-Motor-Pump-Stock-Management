import django_filters
from django import forms
from .models import CategoryStock,CategoryStockOut,DISTRICT_CHOICES

class CategoryStockFilter(django_filters.FilterSet):

    category = django_filters.CharFilter(
        label="Kategori",
        method="filter_category",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Kategori'
        })
    )

    material_name = django_filters.CharFilter(
        label="Malzeme Adi",
        method="filter_material_name",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Malzeme ara..'
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

    def filter_category(self, queryset, name, value):
        if value:
            value = value.upper()
            return queryset.filter(category__name__icontains=value)
        return queryset

    def filter_material_name(self, queryset, name, value):
        if value:
            value = value.upper()
            return queryset.filter(material_name__icontains=value)
        return queryset
    
class CategoryStockOutFilter(django_filters.FilterSet):

    outlet_plug = django_filters.CharFilter(
        lookup_expr='iexact',
        label="Çıkış Fişi",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Çıkış Fişi ara...'
        })
    )
    
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
        label="Adres",
        method="filter_address",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'adres ara..'
        })
    )

    category = django_filters.CharFilter(
        label="Kategori",
        method="filter_category",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Kategori'
        })
    )

    material_name = django_filters.CharFilter(
        label="Malzeme Adi",
        method="filter_material_name",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Malzeme ara..'
        })
    )

    class Meta:
        model = CategoryStockOut
        fields = []
        
    def filter_address(self, queryset, name, value):
        if value:
            value = value.upper()
            return queryset.filter(address__icontains=value)
        return queryset
    
    def filter_category(self, queryset, name, value):
        if value:
            value = value.upper()
            return queryset.filter(stock__category__name__icontains=value)
        return queryset

    def filter_material_name(self, queryset, name, value):
        if value:
            value = value.upper()
            return queryset.filter(stock__material_name__icontains=value)
        return queryset
    