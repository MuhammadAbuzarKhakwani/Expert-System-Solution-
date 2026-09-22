from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length = 70)
    description = models.TextField(max_length = 200)
    create_at = models.DateTimeField()
    is_active = models.BooleanField()
    update_at = models.DateTimeField()

class Brand(models.Model):
    name = models.CharField(max_length = 70)
    description	= models.TextField(max_length = 350)
    is_active = models.Boolean()
    created_at = models.DateTime()
    updated_at = models.DateTime()

class Product(models.Model):

    class UnitChoices(models.TextChoices):
        PCS = "PCS", "Pieces"
        KG = "KG", "Kilogram"
        LITER = "LITER", "Liter"
        BOX = "BOX", "Box"

    id = models.BigAutoField(primary_key=True)
    sku = models.CharField(max_length=100,unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey("Category",on_delete=models.PROTECT)
    brand = models.ForeignKey("Brand",on_delete=models.PROTECT)
    barcode = models.CharField(max_length=100)
    cost_price = models.DecimalField(max_digits=12,decimal_places=2)
    selling_price = models.DecimalField(max_digits=12,decimal_places=2)
    minimum_stock = models.PositiveIntegerField()
    unit = models.CharField(max_length=10,choices=UnitChoices.choices)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
        