from django.contrib import admin
from .models import Hydrophore,PumpType,Power,OutboundWorkOrder,RepairReturn,WorkshopExit,DistrictFieldPersonnel

class HydrophoreAdmin(admin.ModelAdmin):
    list_display = ( 'serial_number','engine_power','engine_brand','pump_type','location','district','neighborhood')
    list_filter = ( 'location',)
    search_fields = ( 'serial_number',)

class WorkshopExitAdmin(admin.ModelAdmin):
    list_display = ('hydrophore','district','neighborhood','outbound_work_order','workshop_dispatch_slip_number','workshop_dispatch_date','created_at','status')
    list_filter = ( 'status',)
    search_fields = ( 'outbound_work_order','workshop_dispatch_slip_number')
    
class RepairReturnAdmin(admin.ModelAdmin):
    list_display = ('hydrophore','workshop_exit','repair_return_slip_number','repair_return_date','status','created_at')
    list_filter = ( 'status',)
    search_fields = ( 'hydrophore','repair_return_slip_number')
    
class OutboundWorkOrderAdmin(admin.ModelAdmin):
    list_display = ('disassembled_hydrophore','mounted_hydrophore','disassembled_date','district','neighborhood','dispatch_slip_number','dispatch_date','district_personnel','created_at','status','updated_at')
    list_filter = ( 'status',)
    search_fields = ( 'disassembled_hydrophore','mounted_hydrophore','dispatch_slip_number')

admin.site.register(Hydrophore,HydrophoreAdmin)
admin.site.register(Power)
admin.site.register(PumpType)
admin.site.register(OutboundWorkOrder,OutboundWorkOrderAdmin)
admin.site.register(RepairReturn,RepairReturnAdmin)
admin.site.register(WorkshopExit,WorkshopExitAdmin)
admin.site.register(DistrictFieldPersonnel)