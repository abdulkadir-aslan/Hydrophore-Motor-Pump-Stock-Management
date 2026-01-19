from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

STATUS= (
    ('active','Aktif'),
    ('passive','Pasif'),
)

DEFAULT_STATUS = 'passive'

AUTHORİZATİON = (
    ('1','Yönetici'),
    ('2','Kullanıcı'),
    ('3','Tamir'),
)
DEFAULT_AUTHORİZATİON = '2'



class User(AbstractUser):
    status = models.CharField(verbose_name="Durum",choices=STATUS,default=DEFAULT_STATUS,max_length=7,blank=False)
    authorization = models.CharField(verbose_name="Yetki",null=False,choices=AUTHORİZATİON,default=DEFAULT_AUTHORİZATİON,max_length=11,blank=False)
    profileimage = models.ImageField(verbose_name="Profil Fotoğrafı",null=False,blank=False,upload_to="profile",default="7.png")


