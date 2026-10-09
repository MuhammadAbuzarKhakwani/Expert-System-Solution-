from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    BranchViewSet, BrandViewSet, CashRegisterShiftViewSet, CategoryViewSet,
    CustomerLedgerViewSet, CustomerViewSet, ExpenseViewSet,
    ProductVariantViewSet, ProductViewSet, PurchaseOrderViewSet,
    RepairJobViewSet, SaleReturnViewSet, SaleViewSet, StockItemViewSet,
    StockMovementViewSet, StockTransferViewSet, StockViewSet,
    SupplierLedgerViewSet, SupplierViewSet, WarehouseViewSet,
)

router = DefaultRouter()

router.register("branches", BranchViewSet)
router.register("warehouses", WarehouseViewSet)
router.register("categories", CategoryViewSet)
router.register("brands", BrandViewSet)
router.register("products", ProductViewSet)
router.register("product-variants", ProductVariantViewSet)
router.register("suppliers", SupplierViewSet)
router.register("customers", CustomerViewSet)
router.register("stocks", StockViewSet)
router.register("stock-items", StockItemViewSet)
router.register("stock-movements", StockMovementViewSet)
router.register("purchase-orders", PurchaseOrderViewSet)
router.register("cash-register-shifts", CashRegisterShiftViewSet)
router.register("sales", SaleViewSet)
router.register("sale-returns", SaleReturnViewSet)
router.register("stock-transfers", StockTransferViewSet)
router.register("customer-ledgers", CustomerLedgerViewSet)
router.register("supplier-ledgers", SupplierLedgerViewSet)
router.register("expenses", ExpenseViewSet)
router.register("repair-jobs", RepairJobViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("auth/", include("rest_framework.urls")),  ###
]