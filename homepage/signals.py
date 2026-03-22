from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from core.middleware import get_current_user

from .models import Notification
from warehouses.models import Order,Repair
from hydrophore.models import OutboundWorkOrder,WorkshopExit,RepairReturn
from other_materials.models import CategoryStockOut

@receiver(post_save, sender=CategoryStockOut)
def create_category_stock_out_notification(sender, instance, created, **kwargs):
    # Eğer yeni bir kayıt ise
    if created:
        # Verilen field'lara göre mesajı oluştur
        message = (
            f"3️⃣*{instance.outlet_plug}* iş emri no ile "
            f"{instance.get_district_display()} ilçesi {instance.address} mahallesine "
            f"({str(instance.stock)}) malzemesinden ({instance.quantity}) adet çıkış yapıldı."
        )
        
        user = get_current_user()  # Geçerli kullanıcı bilgisi
        if user.authorization == "2":
            Notification.objects.create(
                user=user,
                message=message
            )

#Hydrophore
@receiver(pre_save, sender=RepairReturn)
def repair_return_slip_dispatch(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_instance = RepairReturn.objects.get(pk=instance.pk)
            instance._old_repair_return_slip_number = old_instance.repair_return_slip_number
        except RepairReturn.DoesNotExist:
            instance._old_repair_return_slip_number = None
    else:
        instance._old_repair_return_slip_number = None

@receiver(post_save, sender=RepairReturn)
def repair_return_slip_notification(sender, instance, created, **kwargs):
    old_value = getattr(instance, "_old_repair_return_slip_number", None)

    # 🔥 kritik şart:
    # önce yoktu → şimdi var
    if old_value is None and instance.repair_return_slip_number:
        user = get_current_user()

        message = (
            f"2️⃣🛠️ ({str(instance.hydrophore)}) hidroforu tamirden geldi. "
            f"*{instance.hydrophore.get_location_display()}* depoya aktarıldı."
            f"* {str(instance.repair_return_slip_number)} * Tamirden gelen fişi oluşturuldu."
        )
        if user.authorization == "2":
            Notification.objects.create(
                user=user,
                message=message
            )

@receiver(pre_save, sender=WorkshopExit)
def store_old_workshop_dispatch(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_instance = WorkshopExit.objects.get(pk=instance.pk)
            instance._old_workshop_dispatch_slip_number = old_instance.workshop_dispatch_slip_number
        except WorkshopExit.DoesNotExist:
            instance._old_workshop_dispatch_slip_number = None
    else:
        instance._old_workshop_dispatch_slip_number = None

@receiver(post_save, sender=WorkshopExit)
def create_workshop_exit_notification(sender, instance, created, **kwargs):
    old_value = getattr(instance, "_old_dispatch_slip_number", None)

    # 🔥 kritik şart:
    # önce yoktu → şimdi var
    if old_value is None and instance.workshop_dispatch_slip_number:
        user = get_current_user()

        message = (
            f"2️⃣🛠️ ({str(instance.hydrophore)}) hidroforu tamire gönderildi "
            f"* {str(instance.workshop_dispatch_slip_number)} * Atölye çıkış fişi oluşturuldu."
        )
        if user.authorization == "2":
            Notification.objects.create(
                user=user,
                message=message
            )

@receiver(pre_save, sender=OutboundWorkOrder)
def store_old_dispatch_slip(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_instance = OutboundWorkOrder.objects.get(pk=instance.pk)
            instance._old_dispatch_slip_number = old_instance.dispatch_slip_number
        except OutboundWorkOrder.DoesNotExist:
            instance._old_dispatch_slip_number = None
    else:
        instance._old_dispatch_slip_number = None

@receiver(post_save, sender=OutboundWorkOrder)
def create_dispatch_notification(sender, instance, created, **kwargs):
    old_value = getattr(instance, "_old_dispatch_slip_number", None)

    # 🔥 kritik şart:
    # önce yoktu → şimdi var
    if old_value is None and instance.dispatch_slip_number:
        user = get_current_user()

        message = (
            f"2️⃣({str(instance.mounted_hydrophore)}) hidroforu "
            f"{instance.get_district_display()} ilçesi "
            f"{instance.neighborhood} mahallesine "
            f"* {str(instance.dispatch_slip_number)} * çıkış fişi oluşturuldu."
        )

        if user.authorization == "2":
            Notification.objects.create(
                user=user,
                message=message
            )

#warehouses
@receiver(pre_save, sender=Repair)
def store_old_status(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_instance = Repair.objects.get(pk=instance.pk)
            instance._old_status = old_instance.status
        except Repair.DoesNotExist:
            instance._old_status = None
    else:
        instance._old_status = None
        
@receiver(post_save, sender=Repair)
def create_passive_notification(sender, instance, created, **kwargs):
    old_status = getattr(instance, "_old_status", None)

    # active → passive geçişi
    if old_status != "passive" and instance.status == "passive":
        user = get_current_user()
        # mesaj oluştur
        message = f"1️⃣{str(instance.order.inventory)} kuyu numarası için *TG{str(instance.order.entrance_plug)}* fişi oluşturuldu."

        # motor kontrol (tercihine göre değiştirilebilir)
        if instance.engine:
            message += f" Motor ({instance.engine_info}) depoya aktarıldı."

        # pompa kontrol
        if instance.pump:
            message += f" Pompa ({instance.pump_info}) depoya aktarıldı."

        if user and user.authorization == "2":
            Notification.objects.create(
                user=user,
                message=message
            )

@receiver(post_save, sender=Order)
def create_order_notification(sender, instance, created, **kwargs):
    # Eğer yeni bir kayıt ise
    if created:
        # Verilen field'lara göre mesajı oluştur
        message = (
            f"1️⃣ {str(instance.inventory)} kuyu numarası için *E{instance.work_order_plug}* İş emri oluşturuldu. "
            f"({instance.get_situation_display()}) emri verildi. "
            f"({instance.get_operation_engine_display()}) işlem türü seçildi."
            )
        
        user = get_current_user()  # Geçerli kullanıcı bilgisi
        if user.authorization == "2":
            Notification.objects.create(
                user=user,
                message=message
            )

@receiver(pre_save, sender=Order)
def store_old_fields(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_instance = Order.objects.get(pk=instance.pk)
            instance._old_outlet_plug = old_instance.outlet_plug
            instance._old_entrance_plug = old_instance.entrance_plug
            instance._old_disassembly_plug = old_instance.disassembly_plug
            instance._old_assembly_plug = old_instance.assembly_plug
        except Order.DoesNotExist:
            instance._old_outlet_plug = None
            instance._old_entrance_plug = None
            instance._old_disassembly_plug = None
            instance._old_assembly_plug = None
    else:
        instance._old_outlet_plug = None
        instance._old_entrance_plug = None
        instance._old_disassembly_plug = None
        instance._old_assembly_plug = None

@receiver(post_save, sender=Order)
def create_disassembly_notification(sender, instance, created, **kwargs):
    old_value = getattr(instance, "_old_disassembly_plug", None)

    # önce yoktu → şimdi var
    if old_value is None and instance.disassembly_plug:
        user = get_current_user()

        message = f"1️⃣ {str(instance.inventory)} kuyu numarası için *D{str(instance.disassembly_plug)}* Demontaj numarası verildi. "

        user = get_current_user()
        if user.authorization == "2":
            Notification.objects.create(
                user=user,
                message=message
            )

@receiver(post_save, sender=Order)
def create_assembly_notification(sender, instance, created, **kwargs):
    old_value = getattr(instance, "_old_assembly_plug", None)

    # önce yoktu → şimdi var
    if old_value is None and instance.assembly_plug:
        user = get_current_user()

        message = f"1️⃣ {str(instance.inventory)} kuyu numarası için *M{str(instance.assembly_plug)}* Montaj numarası verildi. "

        user = get_current_user()
        if user.authorization == "2":
            Notification.objects.create(
                user=user,
                message=message
            )

@receiver(post_save, sender=Order)
def create_entrance_notification(sender, instance, created, **kwargs):
    old_value = getattr(instance, "_old_entrance_plug", None)

    # önce yoktu → şimdi var
    if old_value is None and instance.entrance_plug:
        user = get_current_user()

        message = f"1️⃣🛠️ {str(instance.inventory)} kuyu numarası için *AG{str(instance.entrance_plug)}* Atölye çıkış fişi oluşturuldu."

        # motor / pompa durumları
        if instance.disassembled_engine:
            message += f"({str(instance.disassembled_engine)}) Motor tamire gönderildi."
        if instance.disassembled_pump:
            message += f"({str(instance.disassembled_pump)}) Pompa tamire gönderildi."

        user = get_current_user()
        if user.authorization == "2":
            Notification.objects.create(
                user=user,
                message=message
            )

@receiver(post_save, sender=Order)
def create_outlet_notification(sender, instance, created, **kwargs):
    """
    outlet_plug sonradan oluştuğunda admin kullanıcılara notification oluşturur
    """

    old_value = getattr(instance, "_old_outlet_plug", None)

    # 🔥 kritik şart:
    # önce yoktu → şimdi var
    if old_value is None and instance.outlet_plug:

        # mesaj oluştur
        message = f"1️⃣{str(instance.inventory)} kuyu numarası için *C{str(instance.outlet_plug)}* Çıkış fişi oluşturuldu."

        # motor kontrol (tercihine göre değiştirilebilir)
        if instance.mounted_engine:
            if instance.engine_info:
                message += f" Motor ({instance.engine_info}- {str(instance.mounted_engine)}) depodan aktarıldı."
            else:
                message += f" Motor ({str(instance.mounted_engine)}) Sıfır depodan aktarıldı."

        # pompa kontrol
        if instance.mounted_pump:
            if instance.pump_info:
                message += f" Pompa ({instance.pump_info} - {str(instance.mounted_pump)}) depodan aktarıldı."
            else:
                message += f" Pompa ({str(instance.mounted_pump)}) Sıfır depodan aktarıldı."

        # admin kullanıcıları getir
        user = get_current_user()

        if user.authorization == "2":
            Notification.objects.create(
                user = user,
                message = message
            )