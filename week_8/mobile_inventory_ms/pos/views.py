from rest_framework.viewsets import ModelViewSet
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

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class SupplierViewSet(ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    
class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class WarehouseViewSet(ModelViewSet):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer
    
class StockViewSet(ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer

