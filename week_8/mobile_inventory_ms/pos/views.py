from rest_framework import ModelViewSets
from .models import (
    Category,
    Brand,
    Product,
    Supplier,
    Customer,
    Warehouse,
    Stock,
)
from .serializer import (
    CategorySerializer,
    BrandSerializer,
    ProductSerializer,
    SupplierSerializer,
    CustomerSerializer,
    WarehouseSerializer,
    StockSerializer,
)

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class BrandViewSet(ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

class ProductViewSet(ModelSerializer):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

