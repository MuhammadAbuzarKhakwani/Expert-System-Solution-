from rest_framework import serializers  
from .models import (
    Category,
    Brand,
    Product,
    Supplier,
    Customer,
    Warehouse,
    Stock,
)

class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = ['id','name','description','is_active','created_at','updated_at']

class BrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        fields = ['id','name','description','is_active','created_at','updated_at']

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id','sku','name','description','category','brand','barcode','cost_price','selling_price','minimum_stock','unit','is_active','created_at','updated_at'] 

class SupplierSerializer(serializers.ModelSerializer):

    class Meta:
        model = Supplier
        fields = ['id','name','company_name','email','phone','address','tax_number','is_active','created_at','updated_at']


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = ['id','name','email','phone','address','tax_number','is_active','created_at','updated_at']


class WarehouseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Warehouse
        fields = ['id','name','code','address','manager','is_active','created_at','updated_at']

class StockSerializer(serializers.ModelSerializer):

    class Meta:
        model = Stock
        fields = ['id','product','warehouse','quantity','update_at']