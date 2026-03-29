import django_filters
from django.db.models import Q
from django import forms
from .models import (Inventory,Unusable,NewWarehousePump,Engine,
    WORK_ORDER_CHOİCES,DISTRICT_CHOICES,LOCATION,ENGINE_TYPE,STATUS,
    Pump,Order,Seconhand,WorkshopExitSlip,DebtSituation)

def turkish_lower(text):
    return text.replace('i', 'İ')

class InventoryFilter(django_filters.FilterSet):
    well_number = django_filters.CharFilter(
        field_name='well_number',
        lookup_expr='iexact',
        label='Kuyu Numarası',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Kuyu numarası'
        })
    )

    # Motor Seri No Filter
    serialnumber = django_filters.CharFilter(
        field_name='engine__serialnumber',
        lookup_expr='icontains',
        label='Motor Seri No',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Motor Seri No'})
    )

    # Pompa Tipi Filter
    pump_type = django_filters.CharFilter(
        field_name='pump__pump_type',
        lookup_expr='icontains',
        label='Pompa Tipi',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pompa Tipi'})
    )

    # İlçe Filter
    district = django_filters.ChoiceFilter(
        field_name='district',
        choices=DISTRICT_CHOICES,
        label='İlçe',
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )

    # Adres Filter (icontains)
    address = django_filters.CharFilter(
        label="Adres",
        method="filter_adress",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Adres'
        })
    )

    # Kuyu Numarasına göre sıralama (A-Z veya Z-A)
    ordering = django_filters.OrderingFilter(
        fields=(('well_number', 'well_number'),),
        field_labels={'well_number': 'Kuyu No'},
        label="Sıralama",
        widget=forms.Select, 
        choices=(
            ('well_number', ' (A-Z)'),
            ('-well_number', '(Z-A)'),
        )
    )

    status = django_filters.ChoiceFilter(
        field_name='status',
        choices=STATUS,
        label='Durum',
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )

    class Meta:
        model = Inventory
        fields = ['district', 'well_number', 'serialnumber', 'pump_type', 'address', 'ordering','status']
    
    def filter_adress(self, queryset, name, value):
        if value:
            value = turkish_lower(value)
            value = value.upper()
            return queryset.filter(address__icontains=value)
        return queryset
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters['ordering'].field.widget.attrs.update({'class': 'form-select '})

class EngineFilter(django_filters.FilterSet):

    serialnumber = django_filters.CharFilter(
        field_name='serialnumber',
        lookup_expr='icontains',
        label='Seri Numarası',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Motor seri numarası'
        })
    )

    engine_power = django_filters.NumberFilter(
        field_name='engine_power__engine_power',
        lookup_expr='exact',
        label='Motor Gücü',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Motor gücü'
        })
    )

    location = django_filters.ChoiceFilter(
        field_name='location',
        choices=LOCATION,
        label='Lokasyon',
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    engine_type = django_filters.ChoiceFilter(
        field_name='engine_type',
        choices=ENGINE_TYPE,
        label='Motor Tipi',
        widget=forms.Select(attrs={'class': 'form-select select2'})
    )

    class Meta:
        model = Engine
        fields = ['serialnumber', 'engine_power', 'location','engine_type']

class GeneralEngineFilter(django_filters.FilterSet):
    serialnumber = django_filters.CharFilter(
        field_name='serialnumber',
        lookup_expr='icontains',
        label='Seri Numarası',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Motor seri numarası'
        })
    )

    engine_power = django_filters.NumberFilter(
        field_name='engine_power__engine_power',
        lookup_expr='exact',
        label='Motor Gücü',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Motor gücü'
        })
    )
    
    engine_mark = django_filters.CharFilter(
        field_name='engine_mark__engine_mark',
        lookup_expr='iexact',
        label='Marka',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Motor markası'
        })
    )

    engine_type = django_filters.ChoiceFilter(
        field_name='engine_type',
        choices=ENGINE_TYPE,
        label='Motor Tipi',
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )

    class Meta:
        model = Engine
        fields = ['serialnumber', 'engine_mark','engine_power', 'engine_type']

class NewPumpFilter(django_filters.FilterSet):

    pump_type = django_filters.CharFilter(
        field_name='pump__pump_type',
        lookup_expr='icontains',
        label='Pompa Tipi',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Pompa tipi'
        })
    )

    class Meta:
        model = NewWarehousePump
        fields = ['pump_type', ]
        
class PumpFilter(django_filters.FilterSet):

    pump_type = django_filters.CharFilter(
        field_name='pump_type',
        lookup_expr='icontains',
        label='Pompa Tipi',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Pompa tipi'
        })
    )

    class Meta:
        model = Pump
        fields = ['pump_type', ]

class UnusableFilter(django_filters.FilterSet):

    well_number = django_filters.CharFilter(
        field_name='well_number__well_number',
        lookup_expr='icontains',
        label='Kuyu No',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Kuyu numarası giriniz'
        })
    )

    # Motor Seri No Filter
    serialnumber = django_filters.CharFilter(
        field_name='engine__serialnumber',
        lookup_expr='icontains',
        label='Motor Seri No',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Motor Seri No'})
    )

    # Pompa Tipi Filter
    pump_type = django_filters.CharFilter(
        field_name='pump__pump_type',
        lookup_expr='icontains',
        label='Pompa Tipi',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pompa Tipi'})
    )

    class Meta:
        model = Unusable
        fields = ['well_number', 'serialnumber', 'pump_type',]

USER_CHOICES = (
    ('ugur', 'UĞUR'),
    ('huseyin', 'HÜSEYİN'),
    ('tumu', 'TÜMÜ'),
)

class OrderFilter(django_filters.FilterSet):
    well_number = django_filters.CharFilter(
        field_name='inventory__well_number',
        lookup_expr='iexact',
        label='Kuyu Numarası',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Kuyu numarası'
        })
    )
    
    # Tek bir giriş alanı ile her iki motoru filtreleyecek
    serial_number = django_filters.CharFilter(
        method='filter_serial_number',
        label='Motor Seri Numarası',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Motor Seri Numarası (montaj ve demontaj için)'
        })
    )
    
    # Yeni user_choice filtresi (Uğur veya Hüseyin seçeneği)
    user = django_filters.ChoiceFilter(
        label="Sorumlu",
        choices=USER_CHOICES,
        method="filter_user",
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    
    district = django_filters.ChoiceFilter(
        field_name='inventory__district',
        choices=DISTRICT_CHOICES,
        label='İlçe',
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    
    operation_type = django_filters.MultipleChoiceFilter(
        field_name='operation_type',
        choices=WORK_ORDER_CHOİCES,
        label='İşlem Türü',
        widget=forms.SelectMultiple(attrs={
            'class': 'form-select select2',
            'data-placeholder': 'İşlem Türü Seçiniz'
        })
    )

    # Adres Filter (icontains)
    address = django_filters.CharFilter(
        label="Adres",
        method="filter_adres",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Adres'
        })
    )

    class Meta:
        model = Order
        fields = ['well_number','operation_type','serial_number','district','address' ]
    
    def filter_adres(self, queryset, name, value):
        if value:
            value = turkish_lower(value)
            value = value.upper()
            return queryset.filter(inventory__address__icontains=value)
        return queryset
    
    def filter_serial_number(self, queryset, name, value):
        if value:
            return queryset.filter(
                Q(mounted_engine__serialnumber__icontains=value) |
                Q(disassembled_engine__serialnumber__icontains=value)
            )
        return queryset
    
     # Override to filter district and operation_type based on user_choice
    def filter_user(self, queryset, name, value):

        # Her ikisinde de ortak filtrelenecek operation_type'lar
        allowed_operations = ['1', '5', '6', '8', '9']

        if value == 'tumu':
            return queryset.filter(
                inventory__district__in=[
                    'siverek', 'bozova', 'hilvan',
                    'birecik', 'halfeti', 'suruç',
                    'karaköprü', 'haliliye', 'eyyübiye',
                    'ceylanpınar', 'viranşehir',
                    'akçakale', 'harran'
                ],
                operation_type__in=allowed_operations
            )
            
        elif value == 'ugur':
            return queryset.filter(
                inventory__district__in=[
                    'siverek', 'bozova', 'hilvan',
                    'birecik', 'halfeti', 'suruç'
                ],
                operation_type__in=allowed_operations
            )

        elif value == 'huseyin':
            return queryset.filter(
                inventory__district__in=[
                    'karaköprü', 'haliliye', 'eyyübiye',
                    'ceylanpınar', 'viranşehir',
                    'akçakale', 'harran'
                ],
                operation_type__in=allowed_operations
            )

        return queryset
    
class SeconhandFilter(django_filters.FilterSet):

    # Motor Gücü Filter (Exact match)
    engine_power = django_filters.NumberFilter(
        field_name='engine__engine_power__engine_power',
        lookup_expr='exact',
        label='Motor Gücü',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Motor gücü'
        })
    )

    # Motor Tipi Filter
    engine_type = django_filters.ChoiceFilter(
        field_name='engine__engine_type',
        choices=ENGINE_TYPE,
        label='Motor Tipi',
        widget=forms.Select(attrs={'class': 'form-select '})
    )

    # Motor Seri No Filter
    serialnumber = django_filters.CharFilter(
        field_name='engine__serialnumber',
        lookup_expr='icontains',
        label='Motor Seri No',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Motor Seri No'})
    )

    # Pompa Tipi Filter
    pump_type = django_filters.CharFilter(
        field_name='pump__pump_type',
        lookup_expr='icontains',
        label='Pompa Tipi',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pompa Tipi'})
    )

    # Depo No Filter
    row_identifier = django_filters.CharFilter(
        field_name='row_identifier',
        lookup_expr='icontains',
        label='Depo No',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Depo No'})
    )

    class Meta:
        model = Seconhand
        fields = ['engine_power', 'engine_type', 'serialnumber', 'pump_type', 'row_identifier']

class WorkshopExitSlipFilter(django_filters.FilterSet):
    # Tarih sıralaması
    date_order = django_filters.OrderingFilter(
        fields=(('date', 'date'),),
        field_labels={'date': 'Tarih'},
        label='Sırala',
        widget=forms.Select, 
        choices=(
            ('date', 'Eskiden Yeniye'),
            ('-date', 'Yeniden Eskiye'),
        )
    )

    # Fiş No arama
    slip_no = django_filters.CharFilter(
        field_name='slip_no',
        lookup_expr='icontains',
        label='Fiş No',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Fiş No'})
    )

    # Kuyu No arama
    well_no = django_filters.CharFilter(
        field_name='well_no',
        lookup_expr='exact',
        label='Kuyu No',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Kuyu No'})
    )

    # Adres arama
    address = django_filters.CharFilter(
        label="Adres",
        method="filter_address",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Adres'
        })
    )

    class Meta:
        model = WorkshopExitSlip
        fields = ['slip_no', 'well_no', 'address']
    
    def filter_address(self, queryset, name, value):
        if value:
            value = turkish_lower(value)
            value = value.upper()
            return queryset.filter(address__icontains=value)
        return queryset

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # date_order widget attrs ekleme
        self.filters['date_order'].field.widget.attrs.update({'class': 'form-select select2'})

class DebtSituationFilter(django_filters.FilterSet):
    well_number = django_filters.CharFilter(
        field_name='inventory__well_number',
        lookup_expr='iexact',
        label='Kuyu Numarası',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Kuyu numarası'
        })
    )

    district = django_filters.ChoiceFilter(
        field_name='inventory__district',
        choices=DISTRICT_CHOICES,
        label='İlçe',
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    
    # Adres Filter (icontains)
    address = django_filters.CharFilter(
        label="Adres",
        method="filter_adres",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Adres'
        })
    )

    class Meta:
        model = Order
        fields = ['well_number','district','address' ]
    
    def filter_adres(self, queryset, name, value):
        if value:
            value = turkish_lower(value)
            value = value.upper()
            return queryset.filter(inventory__address__icontains=value)
        return queryset
    