from django import forms
from django.forms import ModelForm
from .models import *

class MarkForm(ModelForm):
    class Meta:
        model = Mark
        fields = ['engine_mark',]
        
        widgets = {
            'engine_mark': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Marka'}),
        }
    def clean_engine_mark(self):
        engine_mark = self.cleaned_data.get('engine_mark').upper()
        
        if Mark.objects.filter(engine_mark=engine_mark).exists():
            raise forms.ValidationError(f"*{engine_mark}* Bu Marka zaten mevcut.")
        
        return engine_mark

class PowerForm(ModelForm):
    class Meta:
        model = Power
        fields = ['engine_power',]
        widgets = {
            'engine_power': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Güç'}),
        }
    def clean_engine_power(self):
        engine_power = self.cleaned_data.get('engine_power')
        
        if Power.objects.filter(engine_power=engine_power).exists():
            raise forms.ValidationError(f"*{engine_power}* * Bu Güç değeri zaten mevcut.")
        
        return engine_power

class EngineForm(ModelForm):
    class Meta:
        model = Engine
        fields = ['engine_type', 'engine_power', 'engine_mark', 'serialnumber', 'comment']
        widgets = {
            'engine_type': forms.Select(attrs={'class': 'form-select select2', }),
            'engine_power': forms.Select(attrs={'class': 'form-select select2', }),
            'engine_mark': forms.Select(attrs={'class': 'form-select select2', }),
            'serialnumber': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Seri Numarası'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Açıklama', 'rows': '3'}),
        }

class PumpEditForm(ModelForm):
    class Meta:
        model = Pump
        fields = ['pump_type', 'pump_breed', 'number_stages', 'pump_mark', 'comment']
        widgets = {
            'pump_type': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Pompa Tipi', 
                'id': 'pump_type_id'
            }),
            'pump_breed': forms.Select(attrs={
                'class': 'form-select', 
                'id': 'pump_breed_id'
            }),
            'number_stages': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Kademe Sayısı', 
                'id': 'number_stages_id'
            }),
            'pump_mark': forms.Select(attrs={
                'class': 'form-select', 
                'id': 'pump_mark_id'
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'Açıklama', 
                'rows': 3,  
                'id': 'comment_id'
            }),
        }

class PumpForm(ModelForm):
    class Meta:
        model = Pump
        fields = ['pump_type', 'pump_breed', 'number_stages', 'pump_mark', 'comment']
        
        widgets = {
            'pump_type': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Pompa Tipi', 
                'id': 'pump_type_id'
            }),
            'pump_breed': forms.Select(attrs={
                'class': 'form-select select2', 
                'id': 'pump_breed_id'
            }),
            'number_stages': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Kademe Sayısı', 
                'id': 'number_stages_id'
            }),
            'pump_mark': forms.Select(attrs={
                'class': 'form-select select2', 
                'id': 'pump_mark_id'
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'Açıklama', 
                'rows': 3,  
                'id': 'comment_id'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        pump_type = cleaned_data.get("pump_type")
        pump_breed = cleaned_data.get("pump_breed")
        number_stages = cleaned_data.get("number_stages")
        pump_mark = cleaned_data.get("pump_mark")
        
        if Pump.objects.filter(
            pump_type=pump_type,
            pump_breed=pump_breed,
            number_stages=number_stages,
            pump_mark=pump_mark
        ).exists():
            raise forms.ValidationError("Bu pompa kombinasyonu zaten mevcut!")
        
        return cleaned_data

class InventoryEditForm(ModelForm):
    engine = forms.ModelChoiceField(
        queryset=Engine.objects.none(),
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'select-engine',
            'data-show-subtext': 'true',
            'data-live-search': 'true',
            'disabled': 'disabled'
        })
    )
    pump = forms.ModelChoiceField(
        queryset=Pump.objects.none(),
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'select-pump',
            'disabled': 'disabled'
        })
    )

    class Meta:
        model = Inventory  
        fields = ["well_number", "district", "address", "disassembly_depth",
                  "mounting_depth", "tank_info", "pipe_type", "cable",
                  "engine", "pump", "flow", "comment"]
        widgets = {
            "well_number": forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Kuyu Numarası'}),
            "district": forms.Select(attrs={'class': 'form-select','id': 'select-district'}),
            "address": forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Adres', 'rows': "2"}),
            "disassembly_depth": forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Demontaj Derinliği'}),
            "mounting_depth": forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Montaj Derinliği'}),
            "tank_info": forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Depo Bilgisi'}),
            "pipe_type": forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Boru Tipi'}),
            "cable": forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Kablo'}),
            "flow": forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Debi'}),
            'comment': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Açıklama', 'rows': '3'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            if self.instance.engine:
                self.fields['engine'].queryset = Engine.objects.filter(pk=self.instance.engine.pk)
                self.fields['engine'].initial = self.instance.engine
            if self.instance.pump:
                self.fields['pump'].queryset = Pump.objects.filter(pk=self.instance.pump.pk)
                self.fields['pump'].initial = self.instance.pump

class EngineChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        # obj = Engine instance
        seconhand = obj.seconhand_set.first()
        if seconhand:
            return f"{seconhand.row_identifier} - {obj}"
        return str(obj)

class PumpChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        seconhand = obj.seconhand_set.first()
        if seconhand:
            return f"{seconhand.row_identifier} - {obj}"
        return str(obj)

class InventoryForm(ModelForm):
    engine = EngineChoiceField(
        queryset=Engine.objects.none(),
        widget=forms.Select(attrs={
            'class': 'form-select select2',
            'id': 'select-engine'
        })
    )

    pump = PumpChoiceField(
        queryset=Pump.objects.none(),
        widget=forms.Select(attrs={
            'class': 'form-select select2',
            'id': 'select-pump'
        })
    )
    class Meta:
        model = Inventory  
        fields = ["well_number", "district", "address", "disassembly_depth",
                  "mounting_depth", "tank_info", "pipe_type", "cable",
                  "engine", "pump", "flow", "comment"]
        widgets = {
            "well_number": forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Kuyu Numarası'}),
            "district": forms.Select(attrs={'class': 'form-select','id': 'select-district'}),
            "address": forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Adres', 'rows': "2"}),
            "disassembly_depth": forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Demontaj Derinliği'}),
            "mounting_depth": forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Montaj Derinliği'}),
            "tank_info": forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Depo Bilgisi'}),
            "pipe_type": forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Boru Tipi'}),
            "cable": forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Kablo'}),
            "engine": forms.Select(attrs={'class': 'form-select select2','id': 'select-engine', 'data-show-subtext': 'true', 'data-live-search': 'true'}),
            "pump": forms.Select(attrs={'class': 'form-select select2','id': 'select-pump'}),
            "flow": forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Debi'}),
            'comment': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Açıklama', 'rows': '3'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Seconhand tablosunda dolu engine kayıtlarını al
        engine_ids = Seconhand.objects.exclude(engine__isnull=True).values_list('engine', flat=True).distinct()
        self.fields['engine'].queryset = Engine.objects.filter(id__in=engine_ids)
        
        # Seconhand tablosunda dolu pump kayıtlarını al
        pump_ids = Seconhand.objects.exclude(pump__isnull=True).values_list('pump', flat=True).distinct()
        self.fields['pump'].queryset = Pump.objects.filter(id__in=pump_ids)
        
    def clean_well_number(self):
        well_number = self.cleaned_data.get('well_number')
        if Inventory.objects.filter(well_number=well_number).exists():
            raise forms.ValidationError("Bu Kuyu Numarası zaten mevcut.")
        return well_number

    def clean_engine(self):
        engine = self.cleaned_data.get('engine')
        if Inventory.objects.filter(engine=engine).exists():
            raise forms.ValidationError("Bu motor daha önce kullanılmış.")
        return engine

    def clean(self):
        cleaned_data = super().clean()
        disassembly_depth = cleaned_data.get("disassembly_depth")
        mounting_depth = cleaned_data.get("mounting_depth")

        if disassembly_depth and mounting_depth:
            if disassembly_depth > mounting_depth:
                raise forms.ValidationError(
                    "Demontaj derinliği, montaj derinliğinden büyük olamaz."
                )
        return cleaned_data

class WarehousePumpForm(ModelForm):
    class Meta:
        model = NewWarehousePump
        fields = ['pump', 'quantity']
        widgets = {
            'pump': forms.Select(attrs={'class': 'form-select select2'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Miktar'}),
        }

    def save(self, commit=True):
        pump = self.cleaned_data['pump']
        quantity_to_add = self.cleaned_data['quantity']

        # Mevcut pump varsa quantity ekle, yoksa yeni oluştur
        warehouse_pump, created = NewWarehousePump.objects.get_or_create(pump=pump)
        if not created:
            warehouse_pump.quantity += quantity_to_add
        else:
            warehouse_pump.quantity = quantity_to_add

        if commit:
            warehouse_pump.save()
        return warehouse_pump

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            "inventory",
            "outlet_plug",
            "outlet_plug_date",
            "entrance_plug",
            "entrance_plug_date",
            "mounted_engine",
            "mounted_pump",
            "comment",
        ]

        widgets = {
            "inventory": forms.Select(attrs={
                "class": "form-select"
            }),
            "outlet_plug": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Çıkış fişi"
            }),
            "outlet_plug_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                    "required": "required",
                },
                format='%Y-%m-%d',
            ),
            "entrance_plug": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Atölyeden Giden Fiş"
            }),
            "entrance_plug_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                },
                format='%Y-%m-%d',
            ),
            "mounted_engine": forms.Select(attrs={
                "class": "form-select",
                "required": "required",
            }),
            "mounted_pump": forms.Select(attrs={
                "class": "form-select",
                "required": "required",
            }),
            'comment': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Açıklama', 'rows': '3'}),

        }
    def clean_outlet_plug(self):
        outlet_plug = self.cleaned_data.get("outlet_plug")
        if outlet_plug:
            qs = Order.objects.filter(outlet_plug=outlet_plug)

            # edit formu için (kendi kaydını hariç tut)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)

            if qs.exists():
                raise forms.ValidationError("Bu çıkış fişi daha önce kullanılmıştır.")

            return outlet_plug

    def clean_entrance_plug(self):
        entrance_plug = self.cleaned_data.get("entrance_plug")
        if entrance_plug:
            qs = Order.objects.filter(entrance_plug=entrance_plug)

            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)

            if qs.exists():
                raise forms.ValidationError("Bu atölye fişi daha önce kullanılmıştır.")

            return entrance_plug
        
class OrderEditForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['outlet_plug', 'entrance_plug', 'outlet_plug_date', 'entrance_plug_date','comment']
        widgets = {
            'outlet_plug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Çıkış Fişi', 'required': 'required'}),
            'entrance_plug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Atölyeden Giden Fiş', }),
            'outlet_plug_date': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Çıkış Fişi Tarihi', 'type': 'date', 'required': 'required'},format='%Y-%m-%d'),
            'entrance_plug_date': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Atölyeden Giden Fiş Tarihi', 'type': 'date', },format='%Y-%m-%d'),
            'comment': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Açıklama', 'rows': '3'}),
        }
    def clean_outlet_plug(self):
        outlet_plug = self.cleaned_data.get("outlet_plug")
        if outlet_plug:
            qs = Order.objects.filter(outlet_plug=outlet_plug)

            # edit formu için (kendi kaydını hariç tut)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)

            if qs.exists():
                raise forms.ValidationError("Bu çıkış fişi daha önce kullanılmıştır.")

            return outlet_plug

    def clean_entrance_plug(self):
        entrance_plug = self.cleaned_data.get("entrance_plug")
        if entrance_plug:
            qs = Order.objects.filter(entrance_plug=entrance_plug)

            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)

            if qs.exists():
                raise forms.ValidationError("Bu atölye fişi daha önce kullanılmıştır.")

            return entrance_plug
        