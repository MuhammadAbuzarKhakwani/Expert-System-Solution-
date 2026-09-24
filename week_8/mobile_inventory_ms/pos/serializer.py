from rest_framework import serializer 
from . import models 

class CategorySerializer(serializer.ModelSerializer):
    
    class Meta:
        model = Category
        Field = ['id','name','description','is_active','created_at','updated_at']

class BrandSerializer(serializer.ModelSerializer):

    class Meta:
        model = Brand
        Field = ['id','name','description','is_active','created_at','updated_at']

class ProductSerializer(serializer.ModelSerializer):

    class Meta:
        model = Product
        Field = ['sku','name','description','category','brand','barcode','cost_price','selling_price','minimum_stock','unit','is_active','created_at','updated_at'] 

class SupplierSerializer(serializer.ModelSerializer):

    class Meta:
        model = Supplier
        Field = ['name','company_name','email','phone','address','tax_number','is_active','created_at','updated_at']