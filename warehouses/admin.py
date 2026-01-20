from django.contrib import admin
from .models import Pump,Inventory,WorkshopExitSlip, Engine,Seconhand,Repair,Unusable,NewWarehousePump,Order

class SeconhandAdmin(admin.ModelAdmin):
    list_display = ('row_identifier', 'pump',  'engine', 'created_at')
    list_filter = ('pump', 'engine')
    search_fields = ('row_identifier', 'created_at')

class RepairAdmin(admin.ModelAdmin):
    list_display = ( 'pump','engine', 'created_at')
    list_filter = ('pump', 'engine')
    search_fields = ( 'created_at',)
    
class UnusableAdmin(admin.ModelAdmin):
    list_display = ( 'pump',  'engine', 'created_at')
    list_filter = ('pump', 'engine')
    search_fields = ( 'created_at',)
    
class EngineAdmin(admin.ModelAdmin):
    list_display = ( 'engine_type','engine_power','engine_mark','serialnumber','location')
    list_filter = ('engine_power', 'engine_type','location')
    search_fields = ( 'serialnumber',)
    
admin.site.register(Pump)
admin.site.register(Inventory)
admin.site.register(Engine,EngineAdmin)
admin.site.register(Seconhand, SeconhandAdmin)
admin.site.register(Repair, RepairAdmin)
admin.site.register(Unusable, UnusableAdmin)
admin.site.register(NewWarehousePump)
admin.site.register(Order)
admin.site.register(WorkshopExitSlip)