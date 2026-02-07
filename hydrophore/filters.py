import django_filters
from django.db.models import Q
from django import forms
from .models import Hydrophore,OutboundWorkOrder

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
        field_name='neighborhood',
        lookup_expr='icontains',
        label='Adres',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Adres'})
    )


    class Meta:
        model = Hydrophore
        fields = ['serial_number','district','neighborhood']

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

    neighborhood = django_filters.CharFilter(
        field_name='neighborhood',
        lookup_expr='icontains',
        label='Mahalle',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Mahalle'
        })
    )

    class Meta:
        model = Hydrophore
        fields = ['serial_number', 'district', 'neighborhood']

class OutboundWorkOrderFilter(django_filters.FilterSet):

    mounted_hydrophore = django_filters.CharFilter(
        field_name='mounted_hydrophore__serial_number',
        label="Hidrofor No",
        lookup_expr='iexact',  # veya 'icontains'
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Hidrofor No'
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
        lookup_expr='icontains',
        label="Mahalle",
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
        fields = ['mounted_hydrophore', 'district', 'neighborhood', 'district_personnel', 'dispatch_slip_number']

