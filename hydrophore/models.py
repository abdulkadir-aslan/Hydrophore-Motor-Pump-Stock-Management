from django.db import models,transaction
from django.utils import timezone

class PumpType(models.Model):
    type = models.CharField(verbose_name="Pompa Tipi", unique=True, max_length=50)
    def save(self, *args, **kwargs):
        self.type = self.type.strip().upper()
        super(PumpType, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.type
    class Meta:
        verbose_name = "Pompa Tipi"
        verbose_name_plural = "Pompa Tipleri"

class Power(models.Model):
    power = models.FloatField(verbose_name="Güç", unique=True)
    def __str__(self):
        return str(self.power)
    class Meta:
        verbose_name = "Güç"
        verbose_name_plural = "Güçler"

class Hydrophore(models.Model):
    DISTRICT_CHOICES = (
    ('akçakale','AKÇAKALE'),
    ('eyyübiye','EYYÜBİYE'),
    ('birecik','BİRECİK'),
    ('bozova','BOZOVA'),
    ('ceylanpınar','CEYLANPINAR'),
    ('halfeti','HALFETİ'),
    ('haliliye','HALİLİYE'),
    ('harran','HARRAN'),
    ('hilvan','HİLVAN'),
    ('karaköprü','KARAKÖPRÜ'),
    ('siverek','SİVEREK'),
    ('suruç','SURUÇ'),
    ('viranşehir','VİRANŞEHİR'),
    )
    LOCATION = (
    ("1", "Atölyede"),
    ("2", "Atölyede Tamir Bekliyor"),
    ("3", "Elektrikçide"),
    ("4", "Kuyuda"),
    ("5", "Tamirde"),
    ("6", "Sıfır Depo"),
    ("7", "Pert Depo"),
    )
    serial_number = models.CharField(verbose_name="Hidrofor Seri Numarası", max_length=100, unique=True, blank=False)
    engine_power = models.ForeignKey(Power, verbose_name="Motor Gücü", on_delete=models.PROTECT, null=True)
    engine_brand = models.CharField(max_length=100, verbose_name="Motor Markası")
    pump_type = models.ForeignKey(PumpType, verbose_name="Pompa Tipi", on_delete=models.PROTECT, null=True)
    location = models.CharField(max_length=50, choices=LOCATION, verbose_name="Lokasyon",default="1")
    district = models.CharField(max_length=100, choices=DISTRICT_CHOICES, null=True, blank=True, verbose_name="İlçe")
    neighborhood = models.CharField(max_length=100, verbose_name="Mahalle" ,null=True, blank=True,)

    def save(self, *args, **kwargs):
        self.serial_number = self.serial_number.strip().upper()
        super(Hydrophore, self).save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.serial_number} - {self.engine_power}KW - {self.pump_type}"

    class Meta:
        verbose_name = "Hidrofor"
        verbose_name_plural = "Hidroforlar"

class DistrictFieldPersonnel(models.Model):
    full_name = models.CharField(
        max_length=150,
        verbose_name='Adı Soyadı'
    )

    phone_number = models.CharField(
        max_length=20,
        verbose_name='Telefon'
    )

    district = models.CharField(
        max_length=100,
        choices=Hydrophore.DISTRICT_CHOICES,
        verbose_name='İlçe'
    )

    vehicle_plate = models.CharField(
        max_length=15,
        verbose_name='Plaka'
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name='Aktif'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Oluşturulma Tarihi'
    )

    def __str__(self):
        return f"{self.full_name}"

    class Meta:
        verbose_name = "İlçe Saha Personeli"
        verbose_name_plural = "İlçe Saha Personelleri"
        ordering = ['full_name']

STATUS_CHOICES = (
    ('active', 'Aktif'),
    ('passive', 'Pasif'),
)

class OutboundWorkOrder(models.Model):
    disassembled_hydrophore = models.ForeignKey(
        Hydrophore,
        null=True, blank=True,
        on_delete=models.PROTECT,
        related_name='disassembled_work_orders',
        verbose_name='Sökülen Hidrofor'
    )

    mounted_hydrophore = models.ForeignKey(
        Hydrophore,
        on_delete=models.PROTECT,
        related_name='mounted_work_orders',
        verbose_name='Takılan Hidrofor'
    )
    
    disassembled_date = models.DateField(
        null=True, blank=True,
        verbose_name='Demontaj Hidrofor Geldiği Tarih'
    )
    
    district = models.CharField(
        max_length=100,
        choices=Hydrophore.DISTRICT_CHOICES,
        verbose_name='İlçe'
    )

    neighborhood = models.CharField(
        max_length=100,
        verbose_name='Mahalle'
    )

    dispatch_slip_number = models.CharField(
        max_length=100,
        verbose_name='Çıkış Fişi No'
    )

    dispatch_date = models.DateField(
        default=timezone.now,
        verbose_name='Çıkış Fişi Tarihi'
    )

    district_personnel = models.ForeignKey(
        'DistrictFieldPersonnel',
        on_delete=models.PROTECT,
        verbose_name='Saha Personeli'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Oluşturulma Tarihi'
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='active',
        verbose_name='Durum'
    )

    comment = models.TextField(verbose_name="Açıklama", blank=True, null=True)

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Güncellenme Tarihi'
    )

    def delete(self, using=None, keep_parents=False):
        with transaction.atomic():
            # Takılan hidroforu araziye al
            if self.mounted_hydrophore:
                self.mounted_hydrophore.location = "1"  # Atölyede
                self.mounted_hydrophore.save()

            super().delete(using=using, keep_parents=keep_parents)
            
    def __str__(self):
        return f"{self.dispatch_slip_number} - {self.mounted_hydrophore.serial_number}"

    class Meta:
        verbose_name = "Çıkış İş Emri"
        verbose_name_plural = "Çıkış İş Emirleri"
        ordering = ['-created_at']

class WorkshopExit(models.Model):
    hydrophore = models.ForeignKey(
        Hydrophore,
        on_delete=models.PROTECT,
        related_name='workshop_exits',
        verbose_name='Hidrofor'
    )

    outbound_work_order = models.ForeignKey(
        OutboundWorkOrder,
        on_delete=models.PROTECT,
        related_name='workshop_exits',
        verbose_name='Çıkış İş Emri'
    )

    workshop_dispatch_slip_number = models.CharField(
        max_length=100,
        null=True, blank=True,
        verbose_name='Atölyeden Giden Fiş No'
    )

    workshop_dispatch_date = models.DateField(
        default=timezone.now,
        null=True, blank=True,
        verbose_name='Fiş Tarihi'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Oluşturulma Tarihi'
    )
    
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='active',
        verbose_name='Durum'
    )

    def delete(self, using=None, keep_parents=False):
        order = self.outbound_work_order

        with transaction.atomic():
            # Sökülen hidrofor varsa
            if order.disassembled_hydrophore:
                dhydrophore = order.disassembled_hydrophore
                dhydrophore.location = "4"  # Kuyuda
                dhydrophore.save()

            # Takılan hidrofor
            mhydrophore = order.mounted_hydrophore
            mhydrophore.location = "3"  # Elektrikçide
            mhydrophore.save()

            # İş emrini geri al
            order.disassembled_hydrophore = None
            order.disassembled_date = None
            order.status = "active"
            order.save()

            # Asıl silme işlemi
            super().delete(using=using, keep_parents=keep_parents)

    def __str__(self):
        return f"{self.workshop_dispatch_slip_number}"

    class Meta:
        verbose_name = "Atölye Çıkışı"
        verbose_name_plural = "Atölye Çıkışları"
        ordering = ['-workshop_dispatch_date']

class RepairReturn(models.Model):
    hydrophore = models.ForeignKey(
        Hydrophore,
        on_delete=models.PROTECT,
        related_name='repair_returns',
        verbose_name='Hidrofor'
    )

    workshop_exit = models.ForeignKey(
        WorkshopExit,
        on_delete=models.PROTECT,
        related_name='repair_returns',
        verbose_name='Atölye Çıkışı'
    )

    repair_return_slip_number = models.CharField(
        max_length=100,
        null=True, blank=True,
        verbose_name='Tamirden Gelen Fiş No'
    )

    repair_return_date = models.DateField(
        null=True, blank=True,
        default=timezone.now,
        verbose_name='Fiş Tarihi'
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='active',
        verbose_name='Durum'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Kayıt Tarihi'
    )

    def delete(self, using=None, keep_parents=False):
        order = self.workshop_exit

        with transaction.atomic():
            # Takılan hidrofor
            hydrophore = self.hydrophore
            hydrophore.location = "2"  # Atölyede Tamir Bekliyor.
            hydrophore.save()

            # İş emrini geri al
            order.workshop_dispatch_slip_number = None
            order.workshop_dispatch_date = None
            order.status = "active"
            order.save()

            # Asıl silme işlemi
            super().delete(using=using, keep_parents=keep_parents)

    def __str__(self):
        return f"{self.repair_return_slip_number} - {self.hydrophore.serial_number}"

    class Meta:
        verbose_name = "Tamirden Geri Geliş"
        verbose_name_plural = "Tamirden Geri Gelişler"
        ordering = ['-repair_return_date']
