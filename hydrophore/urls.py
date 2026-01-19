from django.urls import path
from .views import *

urlpatterns = [
    # Pompa Tipi
    path("pompa_tipi/", pump_type, name="pump_type"),
    path("pompa_tipi_sil/<int:id>/", pump_type_delete, name="pump_type_delete"),

    # Güçler
    path("gucler/", new_power, name="new_power"),
    path("guc_sil/<int:id>/", hydrophore_power_delete, name="hydrophore_power_delete"),

    # Hidrofor
    path("hidroforlar/", hydrophore_homepage, name="hydrophore_homepage"),
    path("hidrofor_sil/<int:id>/", hydrophore_delete, name="hydrophore_delete"),
    path("hidrofor_duzenle/<int:pk>/", hydrophore_edit, name="hydrophore_edit"),
    
    # Saha Personelleri
    path('ajax/search_hydrophore/', search_hydrophore, name='search_hydrophore'),
    path('ajax/personel_getir/', get_personnel_by_district, name='get_personnel_by_district'),
    path("saha_personeli/", district_field_personnel, name="district_field_personnel"),
    path("saha_personeli/<int:id>/", district_field_personnel, name="district_field_personnel_edit"),  # edit
    path("saha_personeli_sil/<int:id>/", district_field_personnel_delete, name="district_field_personnel_delete"),

    # Çıkış İş Emri
    path("tum_cikis_is_emirleri/", all_outbound_work_order, name="all_outbound_work_order"),
    path("cikis_is_emri/", outbound_work_order, name="outbound_work_order"),
    path("yeni_cikis_is_emri/<int:id>/", new_outbound_work_order, name="new_outbound_work_order"),
    path("cikis_is_emri_sil/<int:id>/", outbound_work_order_delete, name="outbound_work_order_delete"),
    path("cikis_is_emri_duzenle/<int:pk>/", outbound_work_order_edit, name="outbound_work_order_edit"),

    # Tamirden Gelen İş Emri
    path("tamir_cikis/", workshop_exit, name="workshop_exit"),
    path("tamir_cikis_sil/<int:id>/", workshop_exit_delete, name="workshop_exit_delete"),
    path("tamir_cikis_duzenle/<int:pk>/", workshop_exit_edit, name="workshop_exit_edit"),
    path("tum_tamir_cikis/", all_workshop_exit, name="all_workshop_exit"),

    # Atölye Tamir Çıkış İş Emri
    path("tamir_gelen/", repair_return, name="repair_return"),
    path("tamir_gelen_sil/<int:id>/", repair_return_delete, name="repair_return_delete"),
    path("tamir_gelen_duzenle/<int:pk>/", repair_return_edit, name="repair_return_edit"),
    path("tum_tamir_gelen/", all_repair_return, name="all_repair_return"),

    # Depolar
    path("atolye_depo/", workshop_stock, name="workshop_stock"),
    path("tamir_depo/", repair_stock, name="repair_stock"),
    path("tamir_listesi/", repair_list, name="repair_list"),
    path("arazi_depo/", field_stock, name="field_stock"),
    path("elektrik_depo/", electrical_stock, name="electrical_stock"),
    path("yeni_depo/", new_stock, name="new_stock"),
    path("hurda_depo/", scrap_stock, name="scrap_stock"),
]
