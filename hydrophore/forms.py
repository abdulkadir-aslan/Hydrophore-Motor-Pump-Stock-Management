from django import forms
from django.forms import ModelForm
from .models import RepairReturn,Power,PumpType,Hydrophore,OutboundWorkOrder,DistrictFieldPersonnel,WorkshopExit

class PumpTypeForm(ModelForm):
    class Meta:
        model = PumpType
        fields = ['type',]
        
        widgets = {
            'type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pompa Tipi'}),
        }
    def clean_type(self):
        type = self.cleaned_data.get('type').upper()
        
        if PumpType.objects.filter(type=type).exists():
            raise forms.ValidationError(f"*{type}* Bu Pompa Tipi zaten mevcut.")
        
        return type

class PowerForm(ModelForm):
    class Meta:
        model = Power
        fields = ['power',]
        widgets = {
            'power': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Güç'}),
        }
    def clean_engine_power(self):
        power = self.cleaned_data.get('power')
        
        if Power.objects.filter(power=power).exists():
            raise forms.ValidationError(f"*{power}* * Bu Güç değeri zaten mevcut.")
        
        return power

class HydrophoreForm(ModelForm):
    class Meta:
        model = Hydrophore
        fields = ['serial_number', 'engine_power', 'engine_brand', 'pump_type', 'district','neighborhood']
        widgets = {
            'serial_number': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Seri Numarası'}
            ),
            'engine_power': forms.Select(
                attrs={'class': 'form-select select2'}
            ),
            'engine_brand': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Motor Markası'}
            ),
            'pump_type': forms.Select(
                attrs={'class': 'form-select select2'}
            ),
            'district': forms.Select(
                attrs={'class': 'form-select'}
            ),
            'neighborhood': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Mahalle'}
            ),
        }
        
    def clean_serial_number(self):
        serial_number = self.cleaned_data.get('serial_number')
        qs = Hydrophore.objects.filter(serial_number=serial_number)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError(
                "Bu seri numarası zaten kayıtlı. Lütfen farklı bir seri numarası giriniz."
            )
        return serial_number

class DistrictFieldPersonnelForm(ModelForm):
    class Meta:
        model = DistrictFieldPersonnel
        fields = [
            'full_name',
            'phone_number',
            'district',
            'vehicle_plate',
            'is_active',
        ]

        widgets = {
            'full_name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Adı Soyadı'}
            ),
            'phone_number': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '05XXXXXXXXX veya +905XXXXXXXXX'
                }
            ),
            'district': forms.Select(
                attrs={'class': 'form-select'}
            ),
            'vehicle_plate': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': '34 ABC 123'}
            ),
            'is_active': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            ),
        }
        
class OutboundWorkOrderForm(ModelForm):
    class Meta:
        model = OutboundWorkOrder
        fields = [
            'disassembled_hydrophore',
            'disassembled_date',
            'district',
            'neighborhood',
            'dispatch_slip_number',
            'dispatch_date',
            'district_personnel', 
            'comment'
        ]
        
        widgets = {
            'disassembled_hydrophore': forms.TextInput(attrs={
                'id': 'disassembled_hydrophore_input',
                'class': 'form-control',
                'placeholder': 'Hidrofor Seri Numarası Giriniz'
            }),
            'disassembled_date': forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date'}
            ),
            'district': forms.Select(
                attrs={'class': 'form-select'}
            ),
            'neighborhood': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Mahalle'}
            ),
            'dispatch_slip_number': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Çıkış Fişi No'}
            ),
            'dispatch_date': forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date'},
                format='%Y-%m-%d'
            ),
            'district_personnel': forms.Select(
                attrs={'class': 'form-select select2'}
            ),
            'comment': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                    'placeholder': 'Açıklama'
                }
            ),
        }

    def clean_dispatch_slip_number(self):
        slip_number = self.cleaned_data.get('dispatch_slip_number')
        if slip_number:
            qs = OutboundWorkOrder.objects.filter(dispatch_slip_number=slip_number)
            # Güncellenen objeyi dahil etmemek için instance kontrolü
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError("Bu çıkış fişi numarası zaten kullanılıyor.")
        return slip_number

    def clean(self):
        cleaned_data = super().clean()
        disassembled_hydrophore = cleaned_data.get('disassembled_hydrophore')
        disassembled_date = cleaned_data.get('disassembled_date')

        if disassembled_hydrophore and not disassembled_date:
            self.add_error(
                'disassembled_date',
                'Demontaj Hidrofor Geldiği Tarih alanı zorunludur çünkü bir hidrofor seçtiniz.'
            )
        disassembled = cleaned_data.get('disassembled_hydrophore')
        mounted = cleaned_data.get('mounted_hydrophore')

        if disassembled and mounted and disassembled == mounted:
            raise forms.ValidationError(
                "Sökülen ve takılan hidrofor aynı olamaz."
            )

        return cleaned_data

class WorkshopExitForm(ModelForm):
    class Meta:
        model = WorkshopExit
        fields = [
            'workshop_dispatch_slip_number','workshop_dispatch_date'
        ]
        widgets = {
            'workshop_dispatch_slip_number': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Çıkış Fişi No',"required": "required",}
            ),
            'workshop_dispatch_date': forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date',"required": "required"},
                format='%Y-%m-%d'
            ),
        }
    def clean_workshop_dispatch_slip_number(self):
        slip_number = self.cleaned_data.get('workshop_dispatch_slip_number')
        if slip_number:
            qs = WorkshopExit.objects.filter(workshop_dispatch_slip_number=slip_number)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError("Bu çıkış fişi numarası zaten kullanılıyor.")
        return slip_number
    
class RepairReturnForm(ModelForm):
    class Meta:
        model = RepairReturn
        fields = [
            'repair_return_slip_number','repair_return_date'
        ]
        widgets = {
            'repair_return_slip_number': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Tamirden Gelen Fiş No',"required": "required",}
            ),
            'repair_return_date': forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date',"required": "required"},
                format='%Y-%m-%d'
            ),
        }
    def clean_repair_return_slip_number(self):
        slip_number = self.cleaned_data.get('repair_return_slip_number')
        if slip_number:
            qs = RepairReturn.objects.filter(repair_return_slip_number=slip_number)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError("Bu çıkış fişi numarası zaten kullanılıyor.")
        return slip_number
    