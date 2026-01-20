from django.db import models
from django.db.models import Max, IntegerField
from django.db.models.functions import Substr, Cast
from django.db import models, transaction
from django.utils import timezone

ENGINE_TYPE = (
    ("1", "3′"),
    ("2", "4′"),
    ("3", "5′"),
    ("4", "6′"),
    ("5", "7′"),
    ("6", "8′"),
    ("7", "9′"),
    ("8", "10′"),
    ("9", "11′"),
    ("10", "ASENKRON"),
    ("11", "-"),
)

class Mark(models.Model):
    engine_mark = models.CharField(verbose_name="Marka", unique=True, max_length=50)
    def save(self, *args, **kwargs):
        self.engine_mark = self.engine_mark.strip().upper()
        super(Mark, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.engine_mark
    
    class Meta:
        verbose_name = "Marka"
        verbose_name_plural = "Markalar"

class Power(models.Model):
    engine_power = models.FloatField(verbose_name="Motor Gücü", unique=True)
    def __str__(self):
        return str(self.engine_power)
    class Meta:
        verbose_name = "Güç"
        verbose_name_plural = "Güçler"

LOCATION = (
    ("1", "Kuyuda"),
    ("2", "Tamir Depo"),
    ("3", "2.El Depo"),
    ("4", "Pert Depo"),
    ("5", "Sıfır Depo"),
    ("6", "Mütahit Depo"),
)

class Engine(models.Model):
    engine_type = models.CharField(verbose_name="Motor Tipi", choices=ENGINE_TYPE, max_length=4)
    engine_power = models.ForeignKey(Power, verbose_name="Motor Gücü", on_delete=models.PROTECT, null=True)
    engine_mark = models.ForeignKey(Mark, verbose_name="Marka", on_delete=models.PROTECT, null=True)
    serialnumber = models.CharField(verbose_name="Seri Numarası", unique=True, max_length=100)
    location = models.CharField(verbose_name="Lokasyon", choices=LOCATION, max_length=10, default="5", null=True)
    storeno = models.IntegerField(verbose_name="Depono", null=True, blank=True)
    comment = models.TextField(verbose_name="Açıklama", blank=True, null=True)

    def __str__(self):
        return f"{self.get_engine_type_display()} - {self.engine_power} HP - {self.engine_mark} - {self.serialnumber}"

    class Meta:
        verbose_name = "Motor"
        verbose_name_plural = "Motorlar"
        ordering = ("engine_power__engine_power",)

BREED = (
    ("1","KROM"),
    ("2","NORİL"),
    ("3","DÖKÜM"),
    ("4","PİK"),
    ("5","-"),
)

class Pump(models.Model):
    pump_type = models.CharField(verbose_name="Tipi", max_length=25, null=False, blank=False)
    pump_breed = models.CharField(verbose_name="Cinsi", choices=BREED, max_length=5, null=False, blank=False)
    number_stages = models.PositiveIntegerField(verbose_name="Kademe Sayısı", default=0, null=False, blank=False)
    pump_mark = models.ForeignKey(Mark, verbose_name="Pompa Markası", on_delete=models.PROTECT, null=True)
    comment = models.TextField(verbose_name="Açıklama", blank=True)

    def __str__(self):
        return self.pump_type + "/" + str(self.number_stages) + " - " +self.pump_mark.engine_mark 
    
    class Meta:
        verbose_name = "Pompa"
        verbose_name_plural = "Pompalar"
        ordering = ("pump_type",)
        constraints = [
            models.UniqueConstraint(
                fields=['pump_type', 'pump_breed', 'number_stages', 'pump_mark'], 
                name='unique_pump_combination'
            )
        ]

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

class Inventory(models.Model):
    well_number = models.CharField(verbose_name="Kuyu Numarası", max_length=100, unique=True, blank=False)
    district = models.CharField(verbose_name="İlçe", null=False, choices=DISTRICT_CHOICES, max_length=50, blank=False)
    address = models.CharField(verbose_name="Adres", max_length=50, null=False, blank=False)
    disassembly_depth = models.PositiveIntegerField(verbose_name="Demontaj Derinliği", blank=False, null=False)
    mounting_depth = models.PositiveIntegerField(verbose_name="Montaj Derinliği", blank=False, null=False)
    tank_info = models.CharField(verbose_name="Depo Bilgisi", max_length=50, null=False, blank=False)
    pipe_type = models.CharField(verbose_name="Boru Tipi", max_length=50, null=False, blank=False)
    cable = models.CharField(verbose_name="Kablo", max_length=15, null=False, blank=False)
    engine = models.ForeignKey(Engine, verbose_name="Motor", on_delete=models.PROTECT, null=True)
    pump = models.ForeignKey(Pump, verbose_name="Pompa", on_delete=models.PROTECT, null=True)
    created_at = models.DateTimeField(auto_now_add=True)  # 'create_at' -> 'created_at'
    updated_at = models.DateTimeField(auto_now=True)  # 'update_at' -> 'updated_at'
    flow = models.CharField(verbose_name="Debi", max_length=50, null=True, blank=True)
    comment = models.TextField(verbose_name="Açıklama", blank=True)

    def save(self, *args, **kwargs):
        self.address = self.address.upper()  # 'adress' -> 'address'
        super(Inventory, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.well_number)

    class Meta:
        verbose_name = "Kuyu"
        verbose_name_plural = "Kuyular"
        constraints = [
            models.UniqueConstraint(fields=['engine'], name='unique_engine_for_inventory')
        ]
        ordering = ("well_number",)

class Seconhand(models.Model):
    pump = models.ForeignKey(Pump, on_delete=models.SET_NULL,null=True, blank=True)
    engine = models.ForeignKey(Engine, on_delete=models.SET_NULL,null=True, blank=True)
    row_identifier = models.CharField( max_length=4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now=True) 
    
    def save(self, *args, **kwargs):
        if not self.pk:
            with transaction.atomic():
                max_value = (
                    Seconhand.objects
                    .annotate(
                        num=Cast(
                            Substr('row_identifier', 2),
                            IntegerField()
                        )
                    )
                    .aggregate(max_num=Max('num'))
                )

                next_number = (max_value['max_num'] or 0) + 1
                self.row_identifier = f"D{next_number:03d}"

        super().save(*args, **kwargs)
    def __str__(self):
        return self.row_identifier
    class Meta:
        verbose_name = "2.El Depo"
        verbose_name_plural = "2.El Depolar"

class Repair(models.Model):
    well_number = models.ForeignKey(Inventory, on_delete=models.CASCADE,null=True, blank=True)
    pump = models.ForeignKey(Pump, on_delete=models.CASCADE,null=True, blank=True)
    engine = models.ForeignKey(Engine, on_delete=models.CASCADE,null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True) 
    
    def __str__(self):
        return self.well_number.well_number 
    class Meta:
        verbose_name = "Tamir Depo"
        verbose_name_plural = "Tamir Depolar"

class Unusable(models.Model):
    well_number = models.ForeignKey(Inventory, on_delete=models.CASCADE,null=True, blank=True)
    pump = models.ForeignKey(Pump, on_delete=models.CASCADE,null=True, blank=True)
    engine = models.ForeignKey(Engine, on_delete=models.CASCADE,null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True) 
    
    def __str__(self):
        return self.well_number 
    class Meta:
        verbose_name = "Pert Depo"
        verbose_name_plural = "Pert Depolar"

class NewWarehousePump(models.Model):
    pump = models.ForeignKey(Pump, on_delete=models.CASCADE,null=False, blank=True)
    quantity = models.PositiveIntegerField(default=0) 
    created_at = models.DateTimeField(auto_now=True)  

    def __str__(self):
        return f"{self.pump} - {self.quantity}"
    
    def decrease_quantity(self, quantity=1):
        """
        Bu fonksiyon, pompa stoğundan belirtilen miktarı düşürür.
        """
        if self.quantity < quantity:
            raise ValueError(f"Yeterli stok yok. Stokta {self.quantity} adet bulunuyor.")
        
        # Stok azaltma
        self.quantity -= quantity
        self.save()

        return self.quantity

STATUS= (
    ('active','Aktif'),
    ('passive','Pasif'),
)

class Order(models.Model):
    inventory = models.ForeignKey(
        Inventory, verbose_name="Kuyu Bilgisi",on_delete=models.CASCADE, null=False, blank=True
    )

    outlet_plug = models.CharField(
        verbose_name="Çıkış Fişi",
        unique=True,null=True,
        max_length=10
    )

    entrance_plug = models.CharField(
        verbose_name="Atölyeden Giden Fiş",
        unique=True,null=True,blank=True,
        max_length=10
    )

    mounted_engine = models.ForeignKey(
        Engine, verbose_name="Montaj Edilen Motor", on_delete=models.CASCADE,
        related_name="mounted_engine_orders",
        null=True, blank=True
    )

    mounted_pump = models.ForeignKey(
        Pump,verbose_name="Montaj Edilen Pompa", on_delete=models.CASCADE,
        related_name="mounted_pump_orders",
        null=True, blank=True
    )

    disassembled_engine = models.ForeignKey(
        Engine,verbose_name="Demontaj Edilen Motor", on_delete=models.CASCADE,
        null=True, blank=True
    )

    disassembled_pump = models.ForeignKey(
        Pump,verbose_name="Demontaj Edilen Pompa", on_delete=models.CASCADE,
        null=True, blank=True
    )

    outlet_plug_date = models.DateField(
        default=timezone.now, verbose_name="Çıkış Fişi Tarihi", blank=True, null=True
    )

    entrance_plug_date = models.DateField(
        verbose_name="Atölyeden Giden Fiş Tarihi", blank=True, null=True
    )

    status = models.CharField(
        verbose_name="Durum",
        choices=STATUS,
        default="active",
        max_length=7
    )

    engine_info = models.CharField(
        verbose_name="Motor Durumu",
        max_length=50,
        blank=True, null=True
    )

    pump_info = models.CharField(
        verbose_name="Pompa Durumu",
        max_length=50,
        blank=True, null=True
    )
    
    comment = models.TextField(verbose_name="Açıklama", blank=True, null=True)
    
    def __str__(self):
        return f"{self.inventory}"
    
    def delete(self, *args, **kwargs):
        with transaction.atomic():
            if self.mounted_engine:
                engine = self.mounted_engine

                if self.engine_info:
                    seconhand = Seconhand.objects.get(
                        row_identifier=self.engine_info
                    )

                    if seconhand:
                        seconhand.engine = engine
                        seconhand.save()

                    engine.location = "3"
                else:
                    engine.location = "5"

                engine.save()
                
            if self.mounted_pump:
                pump = self.mounted_pump

                if self.pump_info:
                    seconhand = Seconhand.objects.get(
                        row_identifier=self.pump_info
                    )

                    if seconhand:
                        seconhand.pump = pump
                        seconhand.save()
                else:
                    warehouse_pump = NewWarehousePump.objects.get(
                        pump=pump
                    )
                    warehouse_pump.quantity += 1
                    warehouse_pump.save()

            super().delete(*args, **kwargs)
    
    class Meta:
        verbose_name = "İş Emri"
        verbose_name_plural = "İş Emirleri"

class WorkshopExitSlip(models.Model):
    date = models.DateField(verbose_name="Tarih")
    slip_no = models.CharField(max_length=100, verbose_name="Fiş No")
    well_no = models.CharField(max_length=100,blank=True, null=True, verbose_name="Kuyu No")
    district = models.CharField(max_length=100,blank=True, null=True, verbose_name="İlçe")
    address = models.CharField(max_length=100, blank=True, null=True,verbose_name="Adres")

    motor_type = models.CharField(max_length=100,blank=True, null=True, verbose_name="Motor Tipi")
    hydrofor_no = models.CharField(max_length=100,blank=True, null=True, verbose_name="Hidrofor No")
    brand = models.CharField(max_length=100, blank=True, null=True,verbose_name="Markası")
    power = models.CharField(max_length=100,blank=True, null=True, verbose_name="Gücü")

    pump_type = models.CharField(max_length=100, blank=True, null=True,verbose_name="Pompa Tipi")
    pump_brand = models.CharField(max_length=100, blank=True, null=True,verbose_name="Pompa Markası")

    submersible = models.CharField(max_length=100,blank=True, null=True, verbose_name="Dalgıç")
    motor = models.CharField(max_length=100, blank=True, null=True,verbose_name="Motor")
    pump = models.CharField(max_length=100,blank=True, null=True, verbose_name="Pompa")
    hydrofor = models.CharField(max_length=100,blank=True, null=True, verbose_name="Hidrofor")

    main_pipe = models.CharField(max_length=100,blank=True, null=True, verbose_name="Ö.Boru")
    secondary_pipe = models.CharField(max_length=100,blank=True, null=True, verbose_name="K.Boru")

    maintenance_status = models.CharField(max_length=100,blank=True, null=True, verbose_name="Bakım Durumu")
    overall_status = models.CharField(max_length=100, blank=True, null=True,verbose_name="Genel Durum")

    class Meta:
        verbose_name = "Tüm Atölye Çıkış Fişi"
        verbose_name_plural = "Tüm Atölye Çıkış Fişleri"
        ordering = ("date",)

    def __str__(self):
        return f"{self.slip_no} - {self.well_no}"
