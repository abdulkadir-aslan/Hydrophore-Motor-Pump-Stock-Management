from django.urls import path
from .views import *

urlpatterns = [
    path('',index,name='home'),
    path('veri_yükleme',data_load,name='data_load'),
    #Bildirimler
    path('bildirimler/sil/<int:notification_id>/', delete_notification, name='delete_notification'),
    path('bildirimler/', notifications_view, name='notifications'),
    #Fişler
    path("hidrofor/<int:pk>/atölye-cikis-fisi-pdf/",hydrophore_workshop_exit_pdf, name="hydrophore_workshop_exit_pdf"),
    path("hidrofor/atölye-exit-check/<int:pk>/", hydrophore_workshop_exit_check, name="hydrophore_workshop_exit_check"),

    path("hidrofor/<int:pk>/cikis-fisi-pdf/",hydrophore_exit_pdf, name="hydrophore_exit_pdf"),
    path("hidrofor/exit-check/<int:pk>/", hydrophore_exit_check, name="hydrophore_exit_check"),

    path("atölye/<int:pk>/cikis-fisi-pdf/",workshop_exit_pdf, name="workshop_exit_pdf"),
    path("atölye/workshop-exit-check/<int:pk>/", workshop_exit_check, name="workshop_exit_check"),
    
    path("order/cikis-check/<int:pk>/", order_cikis_check, name="order_cikis_check"),
    path("order/<int:pk>/cikis-fisi-pdf/",order_cikis_pdf, name="order_cikis_pdf"),

    path('stock-out-check/<str:number>/', stock_out_check, name='stock_out_check'),
    path('stock-out-pdf/<str:number>/', stock_out_pdf, name='stock_out_pdf'),
]

