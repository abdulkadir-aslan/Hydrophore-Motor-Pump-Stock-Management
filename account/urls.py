from django.urls import  path
from . import views

urlpatterns = [
    path("giris/", views.login_request, name="login"),
    path("cikis/", views.logout_request, name="logout"),
    path("kayit/", views.register_request, name="register"),
    path("kullanicilar_anasayfa/", views.users_home, name="users_home"),
    path("kullanici_sil/", views.userDelete, name="user_delete"),
    path("kullanici_guncelle/<int:myid>/", views.updateUser, name="update_user"),
    path("kayit_duzenle/<int:myid>/", views.userEdit, name="register_edit"),
    path("sifre_guncelle/<str:myid>/", views.update_password, name="update_password"),
]

