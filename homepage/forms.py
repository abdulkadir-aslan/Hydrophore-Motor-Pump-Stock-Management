from django import forms
from .models import PumpCatalog
import json


class PumpSelectionForm(forms.Form):
    debi = forms.FloatField(label="Debi (L/s)")
    yukseklik = forms.FloatField(label="Basma Yüksekliği (m)")
    
class PumpExcelUploadForm(forms.Form):
    file = forms.FileField()

class PumpCatalogForm(forms.ModelForm):

    q_values_lps = forms.CharField(
        label="Q Listesi (L/s) - virgülle",
        help_text="Örn: 1.5,2,2.5,3,3.5"
    )

    h_values = forms.CharField(
        label="H Listesi (m) - virgülle",
        help_text="Örn: 140,138,130,125,120"
    )

    class Meta:
        model = PumpCatalog
        fields = [
            "pump_model",
            "kademe",
            "power_kw",
            "q_values_lps",
            "h_values",
            "status",
            "comment",
        ]

    def clean_q_values_lps(self):
        data = self.cleaned_data["q_values_lps"]
        return [float(x.strip()) for x in data.split(",")]

    def clean_h_values(self):
        data = self.cleaned_data["h_values"]
        return [float(x.strip()) for x in data.split(",")]