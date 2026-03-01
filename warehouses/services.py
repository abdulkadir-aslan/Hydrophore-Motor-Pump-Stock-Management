from django.db import transaction
from .models import Seconhand, Unusable, Repair,WorkshopExitSlip
from .views import engine_locations_update

def workshop_exit_delete(slip_no):
    item = WorkshopExitSlip.objects.filter(slip_no=slip_no).first()
    if item:
        item.delete()
        
def workshop_exit_delete_id(slip_no):
    item = WorkshopExitSlip.objects.filter(modal_id=slip_no).first()
    if item:
        item.delete()

def activate_repair_transfer(order):
    obj = Repair.objects.filter(order=order).first()
    if not obj:
        return False, "Tamir kaydı bulunamadı."

    # if obj.status != "active" :
    #     return False, "Tamir durumu PASİF."

    engine = (obj.engine_info or "").split("|")
    pump = (obj.pump_info or "").split("|")

    engine_loc = engine[0].strip() if len(engine) > 0 else ""
    pump_loc = pump[0].strip() if len(pump) > 0 else ""

    engine_item = None
    pump_item = None
    unusable_engine = None
    unusable_pump = None

    with transaction.atomic():

        # ---------------- ENGINE ----------------
        if order.operation_engine in ["engine", "engine_pump"]:

            if engine_loc == "Pert Depo":
                unusable_engine = Unusable.objects.filter(
                    well_number=order.inventory,
                    engine=obj.engine
                ).first()

            elif engine_loc == "2.El Depo" and len(engine) > 1:
                engine_item = Seconhand.objects.filter(
                    row_identifier=engine[1].strip(),
                    engine=obj.engine
                ).first()

                if not engine_item:
                    return False, f"{engine[1]} sırasında {obj.engine.serialnumber} motoru bulunamadı. İş emri bu aşamada geri alınamaz."

            elif engine_loc == "Mütahit Depo" and len(engine) > 2:
                engine_item = Seconhand.objects.filter(
                    row_identifier=engine[2].strip(),
                    engine__serialnumber=engine[1].strip()
                ).first()

                if not engine_item:
                    return False, f"{engine[2]} sırasında {engine[1]} motoru bulunamadı. İş emri bu aşamada geri alınamaz."

        # ---------------- PUMP ----------------
        if order.operation_engine in ["pump", "engine_pump"]:

            if pump_loc == "Pert Depo":
                unusable_pump = Unusable.objects.filter(
                    well_number=order.inventory,
                    pump=obj.pump
                ).first()

            elif pump_loc == "2.El Depo" and len(pump) > 1:
                pump_item = Seconhand.objects.filter(
                    row_identifier=pump[1].strip(),
                    pump=obj.pump
                ).first()

                if not pump_item:
                    return False, f"{pump[1]} sırasında {obj.pump} pompa bulunamadı. İş emri bu aşamada geri alınamaz."

        # ---------------- DELETE PERT ----------------
        if unusable_pump:
            unusable_pump.delete()

        if unusable_engine:
            unusable_engine.delete()

        # ---------------- SECONHAND GÜNCELLEME ----------------
        # Aynı kayıt gelirse tek save yap
        if engine_item and pump_item and engine_item.id == pump_item.id:
            if order.operation_engine in ["engine", "engine_pump"]:
                if engine_loc == "Mütahit Depo" and engine_item.engine:
                    engine_locations_update(engine_item.engine.id, "6")
                engine_item.engine = None

            if order.operation_engine in ["pump", "engine_pump"]:
                engine_item.pump = None

            engine_item.save()

        else:
            if pump_item:
                pump_item.pump = None
                pump_item.save()

            if engine_item:
                if engine_loc == "Mütahit Depo" and engine_item.engine:
                    engine_locations_update(engine_item.engine.id, "6")                
                engine_item.engine = None
                engine_item.save()

        # ---------------- ENGINE LOCATION UPDATE ----------------
        if obj.engine:
            engine_locations_update(obj.engine.id, "2")

        # ---------------- STATUS UPDATE ----------------
        obj.status = "active"
        obj.save()
        if order.situation == "installation":
            order.status = "active"
        elif order.situation == "well_cancellation":
            order.status = "active"
            inv = order.inventory
            inv.engine = obj.engine
            inv.pump = obj.pump
            inv.status = "active"
            inv.save()
            
        order.operation_type = "4"

    return True, "İşlem başarıyla tamamlandı."