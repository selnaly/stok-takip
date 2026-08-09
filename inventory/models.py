from django.db import models


class Product(models.Model):

    CATEGORY_CHOICES = [
        ('HAMMADDE', 'Hammadde'),
        ('YARI_MAMUL', 'Yarı Mamul'),
        ('MAMUL', 'Mamul'),
        ('DIGER', 'Diğer'),
    ]

    UNIT_CHOICES = [
        ('ADET', 'Adet'),
        ('LEVHA', 'Levha'),
        ('METRE', 'Metre'),
        ('KG', 'Kilogram'),
        ('PAKET', 'Paket'),
    ]

    name = models.CharField(
        max_length=100
    )

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES
    )

    quantity = models.PositiveIntegerField(
        default=0
    )

    unit = models.CharField(
        max_length=20,
        choices=UNIT_CHOICES
    )

    minimum_stock = models.PositiveIntegerField(
        default=5
    )

    def __str__(self):
        return self.name


class StockMovement(models.Model):

    MOVEMENT_TYPES = [
        ('GIRIS', 'Stok Girişi'),
        ('CIKIS', 'Stok Çıkışı'),
    ]

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='movements'
    )

    movement_type = models.CharField(
        max_length=5,
        choices=MOVEMENT_TYPES
    )

    quantity = models.PositiveIntegerField()

    description = models.CharField(
        max_length=250,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.product.name} - {self.get_movement_type_display()}"