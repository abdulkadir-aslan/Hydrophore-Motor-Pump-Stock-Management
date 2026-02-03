from django.urls import path
from .views import*

urlpatterns = [
    # Markalar
    path("marka_ekle/", newMark, name="add_mark"),
    path("marka_sil/<int:myid>/", markDelete, name="mark_delete"),

    # Güçler
    path("guc_ekle/", newPower, name="add_power"),
    path("guc_sil/<int:myid>/", powerDelete, name="power_delete"),

    # Motorlar
    path("motor_sil/<int:myid>/", engineDelete, name="engine_delete"),
    path("motor_duzenle/<int:pk>/", engine_edit, name="engine_edit"),
    path("motorlar/", engine_homepage, name="engine_homepage"),

    # Pompalar
    path("pompa_ekle/", newPump, name="add_pump"),
    path("pompa_sil/<int:myid>/", pumpDelete, name="pump_delete"),
    path("pompa_duzenle/<int:pk>/", pump_edit, name="pump_edit"),
    path("pompalar/", pump_homepage, name="pump_homepage"),

    # Envanter
    path("envanter/", inventory_homepage, name="inventory"),
    path("envanter_duzenle/<int:pk>/", inventory_edit, name="inventory_edit"),
    path("envanter_ekle/", add_inventory, name="add_inventory"),
    path("envanter_sil/<int:id>/", delete_inventory, name="delete_inventory"),
    
    # İkinci el
    path("ikinci_el/", seconhand, name="seconhand"),

    # Tamir
    path("tamir_depo/", warehouses_repair, name="warehouses_repair"),
    path("tamir/", repair, name="engine_repair"),
    path("tamir_iş_emri_sil/<int:id>/", repair_delete, name="repair_delete"),
    path("kapanan_tamir_emirleri/", all_repair, name="engine_all_repair"),
    path("tamir_duzenle/<int:id>/", repair_edit, name="repair_edit"),

    # Müteahhit Deposu
    path("müteahhit_deposu/", contractor_warehouse, name="contractor_warehouse"),

    # Kullanılamaz
    path("pert_depo/", unusable, name="unusable"),

    # Yeni Depo Sayfası
    path("yeni_depo_motor/", new_warehouse_engine, name="new_warehouse_engine"),
    path("depo_aktarma/", transfer_warehouse, name="transfer_warehouse"),
    path("yeni_depo_pompa_sil/<int:id>/", new_warehouse_pump_delete, name="new_warehouse_pump_delete"),
    path("yeni_depo_pompa/", new_warehouse_pump, name="new_warehouse_pump"),

    # İş Emirleri
    path("kapanan_tum_is_emirleri/", workshop_exit_slip, name="workshop_exit_slip"),
    path("kapanan_tum_is_emiri_ekle/", new_workshop_exit_slip, name="new_workshop_exit_slip"),
    path("kapanan_tum_is_emiri_düzenle/<int:id>/", workshop_exit_slip_edit, name="workshop_exit_slip_edit"),
    path("kapanan_tum_is_emiri_sil/<int:id>/", workshop_exit_slip_delete, name="workshop_exit_slip_delete"),
    path("tum_is_emirleri/", all_order_page, name="all_order_page"),
    path("is_emirleri/", order_page, name="order_page"),
    path("is_emiri_duzenle/<int:id>/", order_edit, name="order_edit"),
    path("yeni_is_emiri/<int:id>/", new_order, name="new_order"),
    path("is_emiri_sil/<int:id>/", order_delete, name="order_delete"),
]
