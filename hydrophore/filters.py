import django_filters
from django.db.models import Q
from django import forms
from .models import Hydrophore,OutboundWorkOrder,WorkshopExit,RepairReturn

class HydrophoreFilter(django_filters.FilterSet):

    serial_number = django_filters.CharFilter(
        field_name='serial_number',
        lookup_expr='iexact',
        label='Hidrofor No',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Hidrofor numarası'
        })
    )
    
    district = django_filters.ChoiceFilter(
        field_name='district',
        choices=Hydrophore.DISTRICT_CHOICES,
        label='İlçe',
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )

    # Adres Filter (icontains)
    neighborhood = django_filters.CharFilter(
        label="Mahalle",
        method="filter_neighborhood",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Mahalle'
        })
    )

    pump_type = django_filters.CharFilter(
    field_name='pump_type__type',  # PumpType modelinde name alanı varsa
    lookup_expr='icontains',
    label='Pompa Tipi',
    widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Pompa tipi'
        })
    )

    class Meta:
        model = Hydrophore
        fields = ['serial_number','district','neighborhood', 'pump_type']

    def filter_neighborhood(self, queryset, name, value):
        if value:
            value = value.upper()
            return queryset.filter(neighborhood__icontains=value)
        return queryset
    
class HydrophoreAllFilter(django_filters.FilterSet):

    serial_number = django_filters.CharFilter(
        field_name='serial_number',
        lookup_expr='iexact',
        label='Hidrofor No',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Hidrofor numarası'
        })
    )

    district = django_filters.ChoiceFilter(
        field_name='district',
        choices=Hydrophore.DISTRICT_CHOICES,
        label='İlçe',
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    
    location = django_filters.ChoiceFilter(
        field_name='location',
        choices=Hydrophore.LOCATION,
        label='Lokasyon',
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )

    neighborhood = django_filters.CharFilter(
        label="Mahalle",
        method="filter_neighborhood",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Mahalle'
        })
    )

    class Meta:
        model = Hydrophore
        fields = ['serial_number', 'district', 'neighborhood','location']

    def filter_neighborhood(self, queryset, name, value):
        if value:
            value = value.upper()
            return queryset.filter(neighborhood__icontains=value)
        return queryset

class OutboundWorkOrderFilter(django_filters.FilterSet):

    serial_number = django_filters.CharFilter(
        method='filter_serial_number',
        label='Hidrofor Numarası',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Hidrofor Seri Numarası (montaj ve demontaj için)'
        })
    )

    district = django_filters.ChoiceFilter(
        choices=Hydrophore.DISTRICT_CHOICES,
        label="İlçe",
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )

    neighborhood = django_filters.CharFilter(
        label="Mahalle",
        method="filter_neighborhood",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Mahalle'
        })
    )

    district_personnel = django_filters.CharFilter(
        field_name='district_personnel__full_name',
        label="Personel:",
        lookup_expr='icontains',  
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Personel'
        })
    )

    dispatch_slip_number = django_filters.CharFilter(
        lookup_expr='iexact',
        label="Çıkış Fişi No",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Çıkış Fişi No'
        })
    )

    class Meta:
        model = OutboundWorkOrder
        fields = ['serial_number', 'district', 'neighborhood', 'district_personnel', 'dispatch_slip_number']

    def filter_serial_number(self, queryset, name, value):
        if value:
            return queryset.filter(
                Q(mounted_hydrophore__serial_number__icontains=value) |
                Q(disassembled_hydrophore__serial_number__icontains=value)
            )
        return queryset
    
    def filter_neighborhood(self, queryset, name, value):
        if value:
            value = value.upper()
            return queryset.filter(neighborhood__icontains=value)
        return queryset
    
class WorkshopExitFilter(django_filters.FilterSet):
    hydrophore = django_filters.CharFilter(
        field_name='hydrophore__serial_number',
        label="Hidrofor No",
        lookup_expr='iexact',  # veya 'icontains'
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Hidrofor No'
        })
    )
    workshop_dispatch_slip_number = django_filters.CharFilter(
        lookup_expr='iexact',
        label="Atölyeden Giden Fiş No",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Atölyeden Giden Fiş No'
        })
    )
    class Meta:
        model = WorkshopExit
        fields = ['hydrophore', 'workshop_dispatch_slip_number',]
        
class RepairReturnFilter(django_filters.FilterSet):
    hydrophore = django_filters.CharFilter(
        field_name='hydrophore__serial_number',
        label="Hidrofor No",
        lookup_expr='iexact',  # veya 'icontains'
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Hidrofor No'
        })
    )
    repair_return_slip_number = django_filters.CharFilter(
        lookup_expr='iexact',
        label="Tamirden Gelen Fiş No",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Tamirden Gelen Fiş No'
        })
    )
    class Meta:
        model = RepairReturn
        fields = ['hydrophore', 'repair_return_slip_number',]
        