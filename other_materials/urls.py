from django.urls import path
from .views import *

urlpatterns = [
    # Kategori
    path("kategori/", category, name="category"),
    path("malzeme_listesi/", category_stock, name="category_stock"),
    path("kategori_sil/<int:id>/", delete_category, name="delete_category"),
    path("malzeme_sil/<int:id>/", delete_category_stock, name="delete_category_stock"),
    path("malzeme_cikis_islemleri/", category_stock_out, name="category_stock_out"),
    path("malzeme_cikis_islemler/", new_category_stock_out, name="new_category_stock_out"),
    path("malzeme_cikis_sil/<int:id>/", delete_category_stock_out, name="delete_category_stock_out"),
    path("malzeme_cikis_düzenle/<int:id>/", edit_category_stock_out, name="edit_category_stock_out"),

]