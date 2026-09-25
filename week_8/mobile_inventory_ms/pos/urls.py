from django.urls import path,include
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet,
    BrandViewSet,
    ProductViewSet,
    SupplierViewSet,
    CustomerViewSet,
    WarehouseViewSet,
    StockViewSet,
)

router = DefaultRouter()

router.register("categories",CategoryViewSet)
router.register("brands",BrandViewSet)
router.register("products",ProductViewSet)
router.register("suppliers",SupplierViewSet)
router.register("customers", CustomerViewSet)
router.register("warehouses",WarehouseViewSet)
router.register("stocks",StockViewSet)

urlpatterns = [
    path("", include(router.urls)),
]