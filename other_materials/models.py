from django.db import models
from warehouses.models import Order
from django.db import transaction

class Category(models.Model):
    name = models.CharField(
        verbose_name="Kategori Adı",
        max_length=75,
        unique=True
    )

    class Meta:
        verbose_name = "Kategori"
        verbose_name_plural = "Kategoriler"

    def __str__(self):
        return self.name
    
class CategoryStock(models.Model):
    category = models.ForeignKey(
        Category,
        verbose_name="Kategori",
        on_delete=models.CASCADE,
        related_name="stocks"
    )

    material_name = models.CharField(
        verbose_name="Malzeme Adı",
        max_length=100
    )

    quantity = models.PositiveIntegerField(
        verbose_name="Miktar"
    )

    class Meta:
        verbose_name = "Kategori Stok"
        verbose_name_plural = "Kategori Stokları"

    def __str__(self):
        return f"{self.category.name} - {self.material_name}"
    
class CategoryStockOut(models.Model):
    order = models.ForeignKey(
        Order,
        verbose_name="Sipariş",
        on_delete=models.CASCADE,
        related_name="stock_outs"
    )
    stock = models.ForeignKey(
        'CategoryStock',
        verbose_name="Kategori Stok",
        on_delete=models.CASCADE,
        related_name="outs"
    )
    quantity = models.PositiveIntegerField(
        verbose_name="Çıkış Miktarı"
    )
    created_at = models.DateTimeField(
        verbose_name="Oluşturulma Tarihi",
        auto_now_add=True
    )

    class Meta:
        verbose_name = "Kategori Stok Çıkışı"
        verbose_name_plural = "Kategori Stok Çıkışları"

    def __str__(self):
        return f"{self.stock.material_name} - {self.quantity} adet"

    def save(self, *args, **kwargs):
        if not self.pk:  # sadece ilk oluşturulurken çalışsın
            if self.stock.quantity < self.quantity:
                raise ValueError("Stok miktarı yetersiz!")

            self.stock.quantity -= self.quantity
            self.stock.save()

        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        with transaction.atomic():
            # silinmeden önce stok geri eklensin
            self.stock.quantity += self.quantity
            self.stock.save()

            super().delete(*args, **kwargs)

