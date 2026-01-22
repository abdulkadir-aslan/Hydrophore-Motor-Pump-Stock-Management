import django_filters
from django.db.models import Q
from django import forms
from .models import Inventory,Engine,LOCATION,Pump,Order,Seconhand,WorkshopExitSlip

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

    engine = django_filters.CharFilter(
        method='filter_engine_serial',
        label='Motor Seri No',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Motor seri numarası'
        })
    )

    pump = django_filters.CharFilter(
        method='filter_pump_type_or_stage',
        label='Pompa Tipi / Kademe',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Pompa tipi veya kademe'
        })
    )

    class Meta:
        model = Inventory
        fields = ['well_number', 'engine', 'pump']

    def filter_engine_serial(self, queryset, name, value):
        return queryset.filter(
            engine__serialnumber__iexact=value
        )

    def filter_pump_type_or_stage(self, queryset, name, value):
        return queryset.filter(
            Q(pump__pump_type__iexact=value))

class EngineFilter(django_filters.FilterSet):

    serialnumber = django_filters.CharFilter(
        field_name='serialnumber',
        lookup_expr='iexact',
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

    class Meta:
        model = Engine
        fields = ['serialnumber', 'engine_power', 'location']
        
class PumpFilter(django_filters.FilterSet):

    pump_type = django_filters.CharFilter(
        field_name='pump_type',
        lookup_expr='iexact',
        label='Pompa Tipi',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Pompa tipi'
        })
    )

    class Meta:
        model = Pump
        fields = ['pump_type', ]

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
    
    # Çıkış Fişi Tarihi Başlangıç filtresi
    outlet_plug_date_start = django_filters.DateFilter(
        field_name='outlet_plug_date',
        lookup_expr='gte',
        label="Çıkış Fişi Başlangıç Tarihi",
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'placeholder': 'Başlangıç Tarihi'
        })
    )
    
    # Çıkış Fişi Tarihi Bitiş filtresi
    outlet_plug_date_end = django_filters.DateFilter(
        field_name='outlet_plug_date',
        lookup_expr='lte',
        label="Çıkış Fişi Bitiş Tarihi",
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'placeholder': 'Bitiş Tarihi'
        })
    )
    
    def filter_serial_number(self, queryset, name, value):
        if value:
            return queryset.filter(
                Q(mounted_engine__serialnumber__icontains=value) |
                Q(disassembled_engine__serialnumber__icontains=value)
            )
        return queryset

    class Meta:
        model = Order
        fields = ['well_number','serial_number', 'outlet_plug_date_start', 'outlet_plug_date_end']

class SeconhandFilter(django_filters.FilterSet):

    pump = django_filters.ModelChoiceFilter(
        field_name='pump',
        queryset=Pump.objects.none(),  # başlangıçta boş
        label='Pompa',
        widget=forms.Select(attrs={'class': 'form-select select2'})
    )

    engine = django_filters.ModelChoiceFilter(
        field_name='engine',
        queryset=Engine.objects.none(),  # başlangıçta boş
        label='Motor',
        widget=forms.Select(attrs={'class': 'form-select select2'})
    )

    row_identifier = django_filters.CharFilter(
        field_name='row_identifier',
        lookup_expr='icontains',
        label='Depo No',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Depo No'
        })
    )

    created_at = django_filters.DateFromToRangeFilter(
        label='Oluşturulma Tarihi',
        widget=django_filters.widgets.RangeWidget(attrs={
            'type': 'date',
            'class': 'form-control'
        })
    )

    class Meta:
        model = Seconhand
        fields = ['pump', 'engine', 'row_identifier', 'created_at']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Seconhand'te kullanılan pompalar
        self.filters['pump'].queryset = Pump.objects.filter(
            id__in=Seconhand.objects.filter(pump__isnull=False).values_list('pump', flat=True).distinct()
        )

        # Seconhand'te kullanılan motorlar
        self.filters['engine'].queryset = Engine.objects.filter(
            id__in=Seconhand.objects.filter(engine__isnull=False).values_list('engine', flat=True).distinct()
        )

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
        lookup_expr='icontains',
        label='Kuyu No',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Kuyu No'})
    )

    # Adres arama
    address = django_filters.CharFilter(
        field_name='address',
        lookup_expr='icontains',
        label='Adres',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Adres'})
    )

    class Meta:
        model = WorkshopExitSlip
        fields = ['slip_no', 'well_no', 'address']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # date_order widget attrs ekleme
        self.filters['date_order'].field.widget.attrs.update({'class': 'form-select select2'})
