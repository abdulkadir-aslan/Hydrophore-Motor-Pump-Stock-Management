from django.contrib import admin
from .models import Hydrophore,PumpType,Power,OutboundWorkOrder,RepairReturn,WorkshopExit,DistrictFieldPersonnel

admin.site.register(Hydrophore)
admin.site.register(Power)
admin.site.register(PumpType)
admin.site.register(OutboundWorkOrder)
admin.site.register(RepairReturn)
admin.site.register(WorkshopExit)
admin.site.register(DistrictFieldPersonnel)