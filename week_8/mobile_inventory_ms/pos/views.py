from django.db import transaction
from django.db.models import F, Sum
from django.utils import timezone
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .models import (
    Branch, Brand, CashRegisterShift, Category, Customer, CustomerLedger,
    Expense, LedgerEntryType, Payment, PaymentMethod, Product, ProductVariant,
    PurchaseOrder, RepairJob, Sale, SaleReturn, Stock, StockItem, StockMovement,
    StockTransfer, Supplier, SupplierLedger, Warehouse,
)
from .serializers import (
    AmountSerializer, BranchSerializer, BrandSerializer,
    CashRegisterShiftSerializer, CategorySerializer, CustomerLedgerSerializer,
    CustomerSerializer, DeviceInputSerializer, ExpenseSerializer,
    ProductSerializer, ProductVariantSerializer, PurchaseOrderSerializer,
    RepairJobSerializer, SaleReturnSerializer, SaleSerializer,
    ShiftCloseSerializer, StockAdjustSerializer, StockItemSerializer,
    StockMovementSerializer, StockSerializer, StockTransferSerializer,
    SupplierLedgerSerializer, SupplierSerializer, WarehouseSerializer,
    ZERO, change_stock, customer_balance, supplier_balance,
)

SERIALIZED = Product.TrackingType.SERIALIZED


class ViewModelPermissions(DjangoModelPermissions):
    perms_map = {
        **DjangoModelPermissions.perms_map,
        "GET": ["%(app_label)s.view_%(model_name)s"],
        "HEAD": ["%(app_label)s.view_%(model_name)s"],
    }


class Pagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = "page_size"
    max_page_size = 200


class ApiMixin:
    permission_classes = [ViewModelPermissions]
    pagination_class = Pagination
    filter_backends = [SearchFilter, OrderingFilter]


class BaseViewSet(ApiMixin, ModelViewSet):
    http_method_names = ["get", "post", "put", "patch", "head", "options"]

    def perform_create(self, serializer):
        if hasattr(serializer.Meta.model, "created_by"):
            serializer.save(created_by=self.request.user, updated_by=self.request.user)
        else:
            serializer.save()

    def perform_update(self, serializer):
        if hasattr(serializer.Meta.model, "updated_by"):
            serializer.save(updated_by=self.request.user)
        else:
            serializer.save()

    def locked(self):
        self.get_object() 
        return self.queryset.model.objects.select_for_update().get(pk=self.kwargs["pk"])


class ReadOnlyViewSet(ApiMixin, ReadOnlyModelViewSet):
    pass


class BranchViewSet(BaseViewSet):
    queryset = Branch.objects.order_by("id")
    serializer_class = BranchSerializer
    search_fields = ["name", "code"]


class WarehouseViewSet(BaseViewSet):
    queryset = Warehouse.objects.select_related("branch", "manager").order_by("id")
    serializer_class = WarehouseSerializer
    search_fields = ["name", "code"]


class CategoryViewSet(BaseViewSet):
    queryset = Category.objects.order_by("id")
    serializer_class = CategorySerializer
    search_fields = ["name"]


class BrandViewSet(BaseViewSet):
    queryset = Brand.objects.order_by("id")
    serializer_class = BrandSerializer
    search_fields = ["name"]


class ProductViewSet(BaseViewSet):
    queryset = Product.objects.select_related("category", "brand").order_by("id")
    serializer_class = ProductSerializer
    search_fields = ["name", "brand__name", "category__name"]


class ProductVariantViewSet(BaseViewSet):
    queryset = ProductVariant.objects.select_related("product").order_by("id")
    serializer_class = ProductVariantSerializer
    search_fields = ["sku", "barcode", "product__name", "color"]


class SupplierViewSet(BaseViewSet):
    queryset = Supplier.objects.order_by("id")
    serializer_class = SupplierSerializer
    search_fields = ["name", "company_name", "phone"]

    @action(detail=True, methods=["get"])
    def balance(self, request, pk=None):
        """How much we owe this supplier."""
        return Response({"balance": supplier_balance(self.get_object())})


class CustomerViewSet(BaseViewSet):
    queryset = Customer.objects.order_by("id")
    serializer_class = CustomerSerializer
    search_fields = ["name", "phone", "cnic"]

    @action(detail=True, methods=["get"])
    def balance(self, request, pk=None):
        """How much this customer owes us."""
        return Response({"balance": customer_balance(self.get_object())})


# ----------------------------------------------------------------------------
# Stock
# ----------------------------------------------------------------------------
class StockViewSet(ReadOnlyViewSet):
    queryset = Stock.objects.select_related("variant__product", "warehouse").order_by("id")
    serializer_class = StockSerializer
    search_fields = ["variant__sku", "variant__product__name"]

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.query_params.get("low"):  # /stocks/?low=1
            qs = qs.filter(quantity__lte=F("variant__minimum_stock"))
        return qs

    @action(detail=False, methods=["post"])
    @transaction.atomic
    def adjust(self, request):
        """Manual correction for non-serialized items (+ or -)."""
        data = StockAdjustSerializer(data=request.data)
        data.is_valid(raise_exception=True)
        d = data.validated_data
        if d["variant"].product.tracking_type == SERIALIZED:
            raise ValidationError("Phones are managed per IMEI in /stock-items/.")
        stock = change_stock(d["variant"], d["warehouse"], d["quantity"],
                             StockMovement.MovementType.ADJUSTMENT, "ADJUSTMENT", 0,
                             request.user, note=d["note"])
        return Response(StockSerializer(stock).data)


class StockMovementViewSet(ReadOnlyViewSet):
    queryset = StockMovement.objects.select_related("variant__product", "warehouse").order_by("-id")
    serializer_class = StockMovementSerializer
    search_fields = ["variant__sku", "reference_type", "stock_item__imei1"]


class StockItemViewSet(BaseViewSet):
    queryset = StockItem.objects.select_related("variant__product", "warehouse").order_by("id")
    serializer_class = StockItemSerializer
    http_method_names = ["get", "post", "patch", "head", "options"]
    search_fields = ["imei1", "imei2", "variant__product__name", "variant__sku"]

    @transaction.atomic
    def perform_create(self, serializer):
        user = self.request.user
        item = serializer.save(created_by=user, updated_by=user)
        change_stock(item.variant, item.warehouse, 1, StockMovement.MovementType.OPENING,
                     "STOCK_ITEM", item.id, user, item)


class PurchaseOrderViewSet(BaseViewSet):
    queryset = PurchaseOrder.objects.select_related("supplier", "warehouse").prefetch_related("items").order_by("id")
    serializer_class = PurchaseOrderSerializer
    http_method_names = ["get", "post", "head", "options"]  # create + actions only
    search_fields = ["po_number", "supplier__company_name"]

    @action(detail=True, methods=["post"])
    @transaction.atomic
    def place(self, request, pk=None):
        po = self.locked()
        if po.status != PurchaseOrder.Status.DRAFT:
            raise ValidationError("Only draft orders can be placed.")
        po.status = PurchaseOrder.Status.ORDERED
        po.save(update_fields=["status", "updated_at"])
        return Response(self.get_serializer(po).data)

    @action(detail=True, methods=["post"])
    @transaction.atomic
    def receive(self, request, pk=None):
        po = self.locked()
        if po.status not in (PurchaseOrder.Status.DRAFT, PurchaseOrder.Status.ORDERED):
            raise ValidationError("This order cannot be received.")

        devices = DeviceInputSerializer(data=request.data.get("devices", []), many=True)
        devices.is_valid(raise_exception=True)
        by_item = {}
        for d in devices.validated_data:
            by_item.setdefault(d["purchase_item"].id, []).append(d)

        items = list(po.items.select_related("variant__product"))
        if set(by_item) - {i.id for i in items}:
            raise ValidationError("A device points to an item from another order.")
        imeis = [i for d in devices.validated_data for i in (d["imei1"], d.get("imei2")) if i]
        if len(imeis) != len(set(imeis)):
            raise ValidationError("Duplicate IMEI in the request.")

        for item in items:
            variant = item.variant
            if variant.product.tracking_type == SERIALIZED:
                given = by_item.get(item.id, [])
                if len(given) != item.quantity:
                    raise ValidationError(f"{variant}: send exactly {item.quantity} device(s) with IMEI.")
                for d in given:
                    unit = StockItem.objects.create(
                        variant=variant, warehouse=po.warehouse, supplier=po.supplier,
                        purchase_cost=item.unit_cost, created_by=request.user,
                        updated_by=request.user, **d)
                    change_stock(variant, po.warehouse, 1, StockMovement.MovementType.PURCHASE,
                                 "PO", po.id, request.user, unit)
            else:
                change_stock(variant, po.warehouse, item.quantity,
                             StockMovement.MovementType.PURCHASE, "PO", po.id, request.user)
            ProductVariant.objects.filter(pk=variant.pk).update(cost_price=item.unit_cost)

        po.status = PurchaseOrder.Status.RECEIVED
        po.save(update_fields=["status", "updated_at"])
        SupplierLedger.objects.create(
            supplier=po.supplier, entry_type=LedgerEntryType.INVOICE, credit=po.grand_total,
            reference_type="PO", reference_id=po.id, note=po.po_number, created_by=request.user)
        return Response(self.get_serializer(po).data)

    @action(detail=True, methods=["post"])
    @transaction.atomic
    def pay(self, request, pk=None):
        po = self.locked()
        data = AmountSerializer(data=request.data)
        data.is_valid(raise_exception=True)
        amount = data.validated_data["amount"]
        if po.status != PurchaseOrder.Status.RECEIVED:
            raise ValidationError("Receive the order before paying.")
        if po.paid_amount + amount > po.grand_total:
            raise ValidationError("Payment is more than the order total.")
        po.paid_amount += amount
        po.save(update_fields=["paid_amount", "updated_at"])
        SupplierLedger.objects.create(
            supplier=po.supplier, entry_type=LedgerEntryType.PAYMENT, debit=amount,
            reference_type="PO", reference_id=po.id, note=po.po_number, created_by=request.user)
        return Response(self.get_serializer(po).data)

    @action(detail=True, methods=["post"])
    @transaction.atomic
    def cancel(self, request, pk=None):
        po = self.locked()
        if po.status not in (PurchaseOrder.Status.DRAFT, PurchaseOrder.Status.ORDERED):
            raise ValidationError("Only draft or ordered orders can be cancelled.")
        po.status = PurchaseOrder.Status.CANCELLED
        po.save(update_fields=["status", "updated_at"])
        return Response(self.get_serializer(po).data)


class SaleViewSet(BaseViewSet):
    """POST creates and completes the sale (stock, payments, ledger) in one step."""
    queryset = (Sale.objects.select_related("customer", "warehouse", "branch", "cashier")
                .prefetch_related("items", "payments").order_by("-id"))
    serializer_class = SaleSerializer
    http_method_names = ["get", "post", "head", "options"]
    search_fields = ["invoice_no", "customer__name", "customer__phone", "items__stock_item__imei1"]

    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_staff:  # cashiers only see their own sales
            qs = qs.filter(cashier=self.request.user)
        return qs


class SaleReturnViewSet(BaseViewSet):
    queryset = (SaleReturn.objects.select_related("sale").prefetch_related("items").order_by("-id"))
    serializer_class = SaleReturnSerializer
    http_method_names = ["get", "post", "head", "options"]
    search_fields = ["return_no", "sale__invoice_no"]


class CashRegisterShiftViewSet(BaseViewSet):
    queryset = CashRegisterShift.objects.select_related("branch", "cashier").order_by("-id")
    serializer_class = CashRegisterShiftSerializer
    http_method_names = ["get", "post", "head", "options"]

    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_staff:
            qs = qs.filter(cashier=self.request.user)
        return qs

    def perform_create(self, serializer): 
        serializer.save(cashier=self.request.user)

    @action(detail=True, methods=["post"])
    @transaction.atomic
    def close(self, request, pk=None):
        """Body: {"counted_cash": "15000.00", "notes": ""}"""
        shift = self.locked()
        if shift.status != CashRegisterShift.Status.OPEN:
            raise ValidationError("This shift is already closed.")
        data = ShiftCloseSerializer(data=request.data)
        data.is_valid(raise_exception=True)

        window = {"created_by": shift.cashier, "created_at__gte": shift.opened_at}
        cash_in = Payment.objects.filter(sale__shift=shift, method=PaymentMethod.CASH
                                         ).aggregate(t=Sum("amount"))["t"] or ZERO
        refunds = SaleReturn.objects.filter(refund_method=PaymentMethod.CASH, **window
                                            ).aggregate(t=Sum("refund_amount"))["t"] or ZERO
        expenses = Expense.objects.filter(paid_via=PaymentMethod.CASH, branch=shift.branch, **window
                                          ).aggregate(t=Sum("amount"))["t"] or ZERO

        shift.expected_cash = shift.opening_cash + cash_in - refunds - expenses
        shift.counted_cash = data.validated_data["counted_cash"]
        shift.difference = shift.counted_cash - shift.expected_cash
        shift.notes = data.validated_data.get("notes", shift.notes)
        shift.status = CashRegisterShift.Status.CLOSED
        shift.closed_at = timezone.now()
        shift.save()
        return Response(self.get_serializer(shift).data)

def run_transfer(transfer, user, warehouse, sign, movement_type, item_status):
    """Move every line of a transfer in or out of `warehouse` (sign = -1 out, +1 in)."""
    for line in transfer.items.select_related("variant__product"):
        stock_item = None
        if line.stock_item_id:
            stock_item = StockItem.objects.select_for_update().get(pk=line.stock_item_id)
            if sign < 0 and (stock_item.status != StockItem.Status.IN_STOCK
                             or stock_item.warehouse_id != warehouse.id):
                raise ValidationError(f"IMEI {stock_item.imei1} is not in stock at {warehouse}.")
            stock_item.status = item_status
            stock_item.warehouse = warehouse
            stock_item.save(update_fields=["status", "warehouse", "updated_at"])
        change_stock(line.variant, warehouse, sign * line.quantity, movement_type,
                     "TRANSFER", transfer.id, user, stock_item)


class StockTransferViewSet(BaseViewSet):
    queryset = (StockTransfer.objects.select_related("from_warehouse", "to_warehouse")
                .prefetch_related("items").order_by("-id"))
    serializer_class = StockTransferSerializer
    http_method_names = ["get", "post", "head", "options"]
    search_fields = ["transfer_no"]

    @action(detail=True, methods=["post"])
    @transaction.atomic
    def send(self, request, pk=None):
        t = self.locked()
        if t.status != StockTransfer.Status.DRAFT:
            raise ValidationError("Only draft transfers can be sent.")
        run_transfer(t, request.user, t.from_warehouse, -1,
                     StockMovement.MovementType.TRANSFER_OUT, StockItem.Status.RESERVED)
        t.status = StockTransfer.Status.IN_TRANSIT
        t.save(update_fields=["status", "updated_at"])
        return Response(self.get_serializer(t).data)

    @action(detail=True, methods=["post"])
    @transaction.atomic
    def receive(self, request, pk=None):
        t = self.locked()
        if t.status != StockTransfer.Status.IN_TRANSIT:
            raise ValidationError("Only transfers in transit can be received.")
        run_transfer(t, request.user, t.to_warehouse, +1,
                     StockMovement.MovementType.TRANSFER_IN, StockItem.Status.IN_STOCK)
        t.status = StockTransfer.Status.RECEIVED
        t.save(update_fields=["status", "updated_at"])
        return Response(self.get_serializer(t).data)

    @action(detail=True, methods=["post"])
    @transaction.atomic
    def cancel(self, request, pk=None):
        t = self.locked()
        if t.status == StockTransfer.Status.IN_TRANSIT:  
            run_transfer(t, request.user, t.from_warehouse, +1,
                         StockMovement.MovementType.TRANSFER_IN, StockItem.Status.IN_STOCK)
        elif t.status != StockTransfer.Status.DRAFT:
            raise ValidationError("This transfer cannot be cancelled.")
        t.status = StockTransfer.Status.CANCELLED
        t.save(update_fields=["status", "updated_at"])
        return Response(self.get_serializer(t).data)

class CustomerLedgerViewSet(ReadOnlyViewSet):
    queryset = CustomerLedger.objects.select_related("customer").order_by("-id")
    serializer_class = CustomerLedgerSerializer

    def get_queryset(self): 
        qs = super().get_queryset()
        customer = self.request.query_params.get("customer")
        return qs.filter(customer=customer) if customer else qs


class SupplierLedgerViewSet(ReadOnlyViewSet):
    queryset = SupplierLedger.objects.select_related("supplier").order_by("-id")
    serializer_class = SupplierLedgerSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        supplier = self.request.query_params.get("supplier")
        return qs.filter(supplier=supplier) if supplier else qs


class ExpenseViewSet(BaseViewSet):
    queryset = Expense.objects.select_related("branch").order_by("-id")
    serializer_class = ExpenseSerializer
    http_method_names = ["get", "post", "head", "options"]  
    search_fields = ["category", "note"]


class RepairJobViewSet(BaseViewSet):
    queryset = RepairJob.objects.select_related("customer", "technician").order_by("-id")
    serializer_class = RepairJobSerializer
    search_fields = ["job_no", "device_model", "device_imei", "customer__name", "customer__phone"]