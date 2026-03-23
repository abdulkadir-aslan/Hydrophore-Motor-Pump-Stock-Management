from django import forms
from django.forms import ModelForm
from .models import *
from hydrophore.models import OutboundWorkOrder,WorkshopExit

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
    def clean_serialnumber(self):
        serialnumber = self.cleaned_data.get('serialnumber')
        if serialnumber:
            return serialnumber.replace(" ", "").upper()
        return serialnumber

class PumpEditForm(ModelForm):
    class Meta:
        model = Pump
        fields = ['pump_type', 'pump_breed', 'pump_mark', 'comment']
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
        fields = ['pump_type', 'pump_breed', 'pump_mark', 'comment']
        
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
        pump_mark = cleaned_data.get("pump_mark")
        
        if Pump.objects.filter(
            pump_type=pump_type,
            pump_breed=pump_breed,
            pump_mark=pump_mark
        ).exists():
            raise forms.ValidationError("Bu pompa kombinasyonu zaten mevcut!")
        
        return cleaned_data

class OperationForm(ModelForm):
    class Meta:
        model = Order
        fields = ['work_order_plug', 'comment', 'situation', 'operation_engine']
        widgets = {
            'work_order_plug':forms.NumberInput(attrs={
            "class": "form-control",
            "placeholder": "İş Emri No"
            }),
            'comment':forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'Açıklama', 
                'rows': 2,  
            }),
            'situation': forms.Select(attrs={
                'class': 'form-select',
                "required": "required", 
            }),
            'operation_engine':forms.Select(attrs={
                'class': 'form-select ', 
            }),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Sadece ilk 4 operation type göster
        # filtered_choices = [
        #     choice for choice in OPERATION_TYPE_CHOICES
        #     if choice[0] != "new_well"
        # ]

        # # Başına boş seçenek ekle
        # self.fields['situation'].choices = [("", "Seçiniz")] + filtered_choices

        # self.fields['situation'].required = True
        
        # Son kullanılan work_order_plug değerini bul
        last_order = Order.objects.order_by('-work_order_plug').first()
        if last_order and last_order.work_order_plug is not None:
            # Alan int olduğu için direkt +1
            next_value = last_order.work_order_plug + 1
        else:
            next_value = 1  # Eğer veri yoksa 1 ile başla

        # Form açıldığında default value olarak ata
        self.fields['work_order_plug'].initial = next_value

    def clean_work_order_plug(self):
        work_order_plug = self.cleaned_data.get('work_order_plug')

        # Aynı değer var mı kontrol et
        if Order.objects.filter(work_order_plug=work_order_plug).exists():
            raise forms.ValidationError("Bu İş Emri Numarası Daha Önce Kullanılmış!")

        return work_order_plug

class InventoryForm(ModelForm):

    class Meta:
        model = Inventory  
        fields = [
            "well_number", "district", "address",
            "disassembly_depth", "mounting_depth",
            "tank_info", "pipe_type", "cable",
            "flow", "comment",
        ]
        labels = {
            'district': 'İlçe',
        }
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
        

    def clean_well_number(self):
        well_number = self.cleaned_data.get('well_number')

        qs = Inventory.objects.filter(well_number=well_number)

        # edit modunda kendi kaydını hariç tut
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise forms.ValidationError("Bu Kuyu Numarası zaten mevcut.")

        return well_number

    def clean(self):
        cleaned_data = super().clean()
        d = cleaned_data.get("disassembly_depth")
        m = cleaned_data.get("mounting_depth")

        if d and m and d > m:
            raise forms.ValidationError(
                "Demontaj derinliği, montaj derinliğinden büyük olamaz."
            )
        return cleaned_data

class NewInventoryForm(ModelForm):
    class Meta:
        model = Inventory  
        fields = [
            "well_number", "district", "address",
            "disassembly_depth", "mounting_depth",
            "tank_info", "pipe_type", "cable",
            "flow", "comment",
        ]
        labels = {
            'district': 'İlçe',
        }
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
        
    def clean_well_number(self):
        well_number = self.cleaned_data.get('well_number')
        if Inventory.objects.filter(well_number=well_number).exists():
            raise forms.ValidationError("Bu Kuyu Numarası zaten mevcut.")
        return well_number
    
    def clean(self):
        cleaned_data = super().clean()
        d = cleaned_data.get("disassembly_depth")
        m = cleaned_data.get("mounting_depth")

        if d and m and d > m:
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

class AssemblyForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            "outlet_plug",
            "outlet_plug_date",
            "mounted_engine",
            "mounted_pump",
        ]

        widgets = {
            "outlet_plug": forms.NumberInput(attrs={
                "class": "form-control",
                "required":"required",
                "placeholder": "Çıkış fişi"
            }),
            "outlet_plug_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                    "required": "required",
                },
                format='%Y-%m-%d'
            ),
             "mounted_engine": forms.Select(attrs={
                "class": "form-select",
                "required": "required",
            }),
            "mounted_pump": forms.Select(attrs={
                "class": "form-select",
                "required": "required",
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Sadece ilk açılışta çalışsın (POST değilken)
        if not self.is_bound and not self.instance.pk:

            order_max = Order.objects.aggregate(
                max_val=Max("outlet_plug")
            )["max_val"] or 0

            outbound_max = OutboundWorkOrder.objects.aggregate(
                max_val=Max("dispatch_slip_number")
            )["max_val"] or 0

            next_number = max(order_max, outbound_max) + 1

            self.initial["outlet_plug"] = next_number
    
    def clean_outlet_plug(self):
        outlet_plug = self.cleaned_data.get("outlet_plug")

        if outlet_plug:
            # Order içinde kontrol
            qs = Order.objects.filter(outlet_plug=outlet_plug)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)

            if qs.exists():
                raise forms.ValidationError(
                    "Bu çıkış fişi daha önce kullanılmıştır."
                )

            # Hydrophore içinde kontrol
            if OutboundWorkOrder.objects.filter(dispatch_slip_number=outlet_plug).exists():
                raise forms.ValidationError(
                    "Bu çıkış numarası *HİDROFOR* işlemlerinde kullanılmıştır."
                )
        return outlet_plug

class DisassemblyForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['disassembly_plug',]
        widgets = {
            'disassembly_plug': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Demontaj Numarası', 'required': 'required'}),
        }
        
    def clean_disassembly_plug(self):
        disassembly_plug = self.cleaned_data.get("disassembly_plug")
        if disassembly_plug:
            qs = Order.objects.filter(disassembly_plug=disassembly_plug)

            # edit formu için (kendi kaydını hariç tut)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)

            if qs.exists():
                raise forms.ValidationError(f"*{disassembly_plug}* Bu Demontaj numarası daha önce kullanılmıştır.")

            return disassembly_plug

class MountingForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['assembly_plug',]
        widgets = {
            'assembly_plug': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Montaj Numarası', 'required': 'required'}),
        }
        
    def clean_assembly_plug(self):
        assembly_plug = self.cleaned_data.get("assembly_plug")
        if assembly_plug:
            qs = Order.objects.filter(assembly_plug=assembly_plug)

            # edit formu için (kendi kaydını hariç tut)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)

            if qs.exists():
                raise forms.ValidationError(f"*{assembly_plug}* Bu Montaj numarası daha önce kullanılmıştır.")

            return assembly_plug

class LenghtForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['outlet_plug','length','outlet_plug_date']
        widgets = {
            "outlet_plug": forms.NumberInput(attrs={
                "class": "form-control",
                "required":"required",
                "placeholder": "Çıkış fişi"
            }),
            "length": forms.NumberInput(attrs={
                "class": "form-control",
                "required":"required",
                "placeholder": "Boru Uzunluğu (mt)"
            }),
            "outlet_plug_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                    "required": "required",
                },
                format='%Y-%m-%d'
            ),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Sadece ilk açılışta çalışsın (POST değilken)
        if not self.is_bound and not self.instance.pk:

            order_max = Order.objects.aggregate(
                max_val=Max("outlet_plug")
            )["max_val"] or 0

            outbound_max = OutboundWorkOrder.objects.aggregate(
                max_val=Max("dispatch_slip_number")
            )["max_val"] or 0

            next_number = max(order_max, outbound_max) + 1

            self.initial["outlet_plug"] = next_number
    
    def clean_outlet_plug(self):
        outlet_plug = self.cleaned_data.get("outlet_plug")

        if outlet_plug:
            # Order içinde kontrol
            qs = Order.objects.filter(outlet_plug=outlet_plug)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)

            if qs.exists():
                raise forms.ValidationError(
                    "Bu çıkış fişi daha önce kullanılmıştır."
                )

            # Hydrophore içinde kontrol
            if OutboundWorkOrder.objects.filter(dispatch_slip_number=outlet_plug).exists():
                raise forms.ValidationError(
                    "Bu çıkış numarası *HİDROFOR* işlemlerinde kullanılmıştır."
                )
        return outlet_plug

class OrderEditForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['entrance_plug','entrance_plug_date']
        widgets = {
            'entrance_plug': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Atölyeden Giden Fiş','required': 'required' }),
            'entrance_plug_date': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Atölyeden Giden Fiş Tarihi', 'type': 'date', },format='%Y-%m-%d'),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Sadece ilk açılışta çalışsın (POST değilken)
        if not self.is_bound and not self.instance.pk:

            order_max = Order.objects.aggregate(
                max_val=Max("entrance_plug")
            )["max_val"] or 0

            outbound_max = WorkshopExit.objects.aggregate(
                max_val=Max("workshop_dispatch_slip_number")
            )["max_val"] or 0

            next_number = max(order_max, outbound_max) + 1
            self.initial["entrance_plug"] = next_number
    
    def clean_entrance_plug(self):
        entrance_plug = self.cleaned_data.get("entrance_plug")
        if entrance_plug:
            qs = Order.objects.filter(entrance_plug=entrance_plug)

            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)

            if qs.exists():
                raise forms.ValidationError(f"*{entrance_plug}* Bu atölye fişi daha önce kullanılmıştır.")

            if WorkshopExit.objects.filter(workshop_dispatch_slip_number=entrance_plug).exists():
                raise forms.ValidationError(
                    "Bu çıkış numarası *HİDROFOR* işlemlerinde kullanılmıştır."
                )
            return entrance_plug

class WorkshopExitSlipForm(forms.ModelForm):
    class Meta:
        model = WorkshopExitSlip
        fields = '__all__'
        labels = {
            'date': 'Tarih',
            'slip_no': 'Fiş No',
            'well_no': 'Kuyu No',
            'district': 'İlçe',
            'address': 'Adres',
            'motor_type': 'Motor Tipi',
            'hydrofor_no': 'Hidrofor No',
            'brand': 'Markası',
            'power': 'Gücü',
            'pump_type': 'Pompa Tipi',
            'pump_brand': 'Pompa Markası',
            'submersible': 'Dalgıç',
            'motor': 'Motor',
            'pump': 'Pompa',
            'hydrofor': 'Hidrofor',
            'main_pipe': 'Ö.Boru',
            'secondary_pipe': 'K.Boru',
            'maintenance_status': 'Bakım Durumu',
            'overall_status': 'Genel Durum',
        }
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Tarih', 'type': 'date','required': 'required'},format='%Y-%m-%d',),
            'slip_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Fiş No','required': 'required'}),
            'well_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Kuyu No'}),
            'district': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'İlçe'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Adres'}),
            'motor_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Motor Tipi'}),
            'hydrofor_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Hidrofor No'}),
            'brand': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Markası'}),
            'power': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Gücü'}),
            'pump_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pompa Tipi'}),
            'pump_brand': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pompa Markası'}),
            'submersible': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dalgıç'}),
            'motor': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Motor'}),
            'pump': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pompa'}),
            'hydrofor': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Hidrofor'}),
            'main_pipe': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ö.Boru'}),
            'secondary_pipe': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'K.Boru'}),
            'maintenance_status': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Bakım Durumu'}),
            'overall_status': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Genel Durum'}),
        }

