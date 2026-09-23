from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=70)
    description = models.TextField(max_length=200)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['-created_at']

    def __str__(self):
        return self.name


# class Brand(models.Model):
#     name = models.CharField(max_length=70)
#     description = models.TextField(max_length=350)
#     is_active = models.BooleanField(default=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         ordering = ['-created_at']

#     def __str__(self):
#         return self.name


class Product(models.Model):
    
    class UnitChoices(models.TextChoices):
        PCS = "PCS", "Pieces"
        KG = "KG", "Kilogram"
        LITER = "LITER", "Liter"
        BOX = "BOX", "Box"

    sku = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT)
    barcode = models.CharField(max_length=100)
    cost_price = models.DecimalField(max_digits=12, decimal_places=2)
    selling_price = models.DecimalField(max_digits=12, decimal_places=2)
    minimum_stock = models.PositiveIntegerField()
    unit = models.CharField(max_length=10, choices=UnitChoices.choices)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['sku']),
            models.Index(fields=['category']),
            models.Index(fields=['brand']),
        ]

    def __str__(self):
        return self.name


class Supplier(models.Model):
    name = models.CharField(max_length=70)
    company_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    tax_number = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.company_name


class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    tax_number = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class Warehouse(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50, unique=True)
    address = models.TextField()
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class Stock(models.Model):

    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT)
    quantity = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('product', 'warehouse')
        indexes = [
            models.Index(fields=['product', 'warehouse']),
        ]

    def __str__(self):
        return f"{self.product.name} - {self.warehouse.name}: {self.quantity}"
