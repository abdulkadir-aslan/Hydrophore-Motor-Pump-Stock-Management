from django.urls import path
from .views import *

urlpatterns = [
    path('',index,name='home'),
    path('veri_yükleme',data_load,name='data_load'),
    
    #Fişler
    path("order/<int:pk>/cikis-fisi-pdf/",order_cikis_pdf, name="order_cikis_pdf"),
]
