import uuid
from decimal import Decimal

from django.db.models import Q, Sum
from django.utils import timezone
from rest_framework import serializers
from django.db import transaction

from .models import (
    Branch, Brand, CashRegisterShift, Category, Customer, CustomerLedger,
    Expense, LedgerEntryType, Payment, PaymentMethod, Product, ProductVariant,
    PurchaseItem, PurchaseOrder, RepairJob, Sale, SaleItem, SaleReturn,
    SaleReturnItem, Stock, StockItem, StockMovement, StockTransfer,
    StockTransferItem, Supplier, SupplierLedger, Warehouse,
)

ZERO = Decimal("0")
SERIALIZED = Product.TrackingType.SERIALIZED


def money(value):
    return Decimal(value).quantize(Decimal("0.01"))


def make_number(prefix):
    return f"{prefix}-{timezone.now():%Y%m%d}-{uuid.uuid4().hex[:6].upper()}"


def customer_balance(customer):
    t = customer.ledger.aggregate(d=Sum("debit"), c=Sum("credit"))
    return customer.opening_balance + (t["d"] or ZERO) - (t["c"] or ZERO)


def supplier_balance(supplier):
    t = supplier.ledger.aggregate(d=Sum("debit"), c=Sum("credit"))
    return supplier.opening_balance + (t["c"] or ZERO) - (t["d"] or ZERO)


def check_quantity(variant, qty):
    if variant.product.unit == Product.UnitChoices.PCS and qty != qty.to_integral_value():
        raise serializers.ValidationError("Quantity must be a whole number for pieces.")


def check_imeis(imei1, imei2, exclude_pk=None):
    if imei2 and imei1 == imei2:
        raise serializers.ValidationError("IMEI 1 and IMEI 2 must be different.")
    others = StockItem.objects.exclude(pk=exclude_pk)
    for imei in (imei1, imei2):
        if imei and others.filter(Q(imei1=imei) | Q(imei2=imei)).exists():
            raise serializers.ValidationError(f"IMEI {imei} already exists.")


def change_stock(variant, warehouse, delta, movement_type, ref_type, ref_id,user, stock_item=None, note=""):
    stock, _ = Stock.objects.select_for_update().get_or_create(
        variant=variant, warehouse=warehouse
    )
    if delta < 0 and stock.quantity - stock.reserved_quantity < -delta:
        raise serializers.ValidationError(f"Not enough stock for {variant}.")
    stock.quantity += delta
    stock.save(update_fields=["quantity", "updated_at"])
    StockMovement.objects.create(
        variant=variant, warehouse=warehouse, stock_item=stock_item,
        movement_type=movement_type, quantity=delta,
        reference_type=ref_type, reference_id=ref_id, note=note, created_by=user,
    )
    return stock


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = "__all__"
        extra_kwargs = {"fbr_token": {"write_only": True}}  # never sent back


class WarehouseSerializer(serializers.ModelSerializer):
    branch_name = serializers.CharField(source="branch.name", read_only=True)
    manager_name = serializers.SerializerMethodField()

    class Meta:
        model = Warehouse
        fields = "__all__"

    def get_manager_name(self, obj):
        return obj.manager.get_full_name() if obj.manager else None


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

    def validate_parent(self, parent):
        node = parent
        while node and self.instance:  
            if node.pk == self.instance.pk:
                raise serializers.ValidationError("A category cannot be its own ancestor.")
            node = node.parent
        return parent


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)
    brand_name = serializers.CharField(source="brand.name", read_only=True)

    class Meta:
        model = Product
        fields = "__all__"

    def validate(self, data):
        old = self.instance
        ptype = data.get("product_type", old.product_type if old else Product.ProductType.PHONE)
        tracking = data.get("tracking_type", old.tracking_type if old else SERIALIZED)
        if ptype == Product.ProductType.PHONE and tracking != SERIALIZED:
            raise serializers.ValidationError("Phones must be serialized (IMEI per unit).")
        return data


class ProductVariantSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)

    class Meta:
        model = ProductVariant
        fields = "__all__"
        extra_kwargs = {
            "cost_price": {"min_value": ZERO},
            "selling_price": {"min_value": ZERO},
            "minimum_stock": {"min_value": ZERO},
        }


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = "__all__"


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"


class StockSerializer(serializers.ModelSerializer):
    variant_name = serializers.CharField(source="variant.__str__", read_only=True)
    warehouse_name = serializers.CharField(source="warehouse.name", read_only=True)
    available = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = Stock
        fields = "__all__"


class StockAdjustSerializer(serializers.Serializer):
    variant = serializers.PrimaryKeyRelatedField(queryset=ProductVariant.objects.all())
    warehouse = serializers.PrimaryKeyRelatedField(queryset=Warehouse.objects.all())
    quantity = serializers.DecimalField(max_digits=12, decimal_places=2,
                                        help_text="Use a negative number to reduce stock.")
    note = serializers.CharField(max_length=255)

    def validate_quantity(self, value):
        if value == 0:
            raise serializers.ValidationError("Quantity cannot be 0.")
        return value


class StockMovementSerializer(serializers.ModelSerializer):
    variant_name = serializers.CharField(source="variant.__str__", read_only=True)
    warehouse_name = serializers.CharField(source="warehouse.name", read_only=True)

    class Meta:
        model = StockMovement
        fields = "__all__"


class StockItemSerializer(serializers.ModelSerializer):
    variant_name = serializers.CharField(source="variant.__str__", read_only=True)
    warehouse_name = serializers.CharField(source="warehouse.name", read_only=True)

    class Meta:
        model = StockItem
        fields = "__all__"
        read_only_fields = ["status", "purchase_item"] 

    def validate(self, data):
        item = self.instance
        variant = data.get("variant") or (item.variant if item else None)
        if variant and variant.product.tracking_type != SERIALIZED:
            raise serializers.ValidationError("This product is not serialized.")
        if item:
            for field in ("variant", "warehouse"):
                if field in data and data[field] != getattr(item, field):
                    raise serializers.ValidationError(f"{field} cannot be changed. Use a stock transfer.")
        check_imeis(
            data.get("imei1", item.imei1 if item else None),
            data.get("imei2", item.imei2 if item else None),
            item.pk if item else None,
        )
        return data


class DeviceInputSerializer(serializers.ModelSerializer):

    class Meta:
        model = StockItem
        fields = ["purchase_item", "imei1", "imei2", "condition", "pta_status"]
        extra_kwargs = {"purchase_item": {"required": True, "allow_null": False}}

    def validate(self, data):
        check_imeis(data["imei1"], data.get("imei2"))
        return data


class PurchaseItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseItem
        fields = ["id", "variant", "quantity", "unit_cost", "line_total"]
        read_only_fields = ["line_total"]
        extra_kwargs = {
            "quantity": {"min_value": Decimal("0.01")},
            "unit_cost": {"min_value": ZERO},
        }

    def validate(self, data):
        check_quantity(data["variant"], data["quantity"])
        return data


class PurchaseOrderSerializer(serializers.ModelSerializer):
    items = PurchaseItemSerializer(many=True)
    supplier_name = serializers.CharField(source="supplier.company_name", read_only=True)

    class Meta:
        model = PurchaseOrder
        fields = "__all__"
        read_only_fields = ["po_number", "status", "subtotal", "tax_total",
                            "grand_total", "paid_amount"]

    def validate_items(self, items):
        if not items:
            raise serializers.ValidationError("Add at least one item.")
        return items

    @transaction.atomic
    def create(self, validated_data):
        items = validated_data.pop("items")
        order = PurchaseOrder.objects.create(po_number=make_number("PO"), **validated_data)
        subtotal = tax_total = ZERO
        for item in items:
            line = money(item["quantity"] * item["unit_cost"])
            tax_total += money(line * item["variant"].tax_rate / 100)
            subtotal += line
            PurchaseItem.objects.create(purchase_order=order, line_total=line, **item)
        order.subtotal, order.tax_total = subtotal, tax_total
        order.grand_total = subtotal + tax_total
        order.save()
        return order


class AmountSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=14, decimal_places=2,
                                      min_value=Decimal("0.01"))


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ["id", "method", "amount", "reference"]
        extra_kwargs = {"amount": {"min_value": Decimal("0.01")}}


class SaleItemSerializer(serializers.ModelSerializer):
    imei = serializers.CharField(write_only=True, required=False,
                                 help_text="Scan the IMEI instead of sending stock_item.")

    class Meta:
        model = SaleItem
        fields = ["id", "variant", "stock_item", "imei", "item_name", "hs_code",
                  "quantity", "unit_price", "unit_cost", "discount",
                  "tax_rate", "tax_amount", "line_total"]
       
        read_only_fields = ["item_name", "hs_code", "unit_price", "unit_cost",
                            "tax_rate", "tax_amount", "line_total"]
        extra_kwargs = {
            "quantity": {"min_value": Decimal("0.01")},
            "discount": {"min_value": ZERO},
        }

    def validate(self, data):
        if not data["variant"].is_active:
            raise serializers.ValidationError("This variant is inactive.")
        check_quantity(data["variant"], data["quantity"])
        return data


class SaleSerializer(serializers.ModelSerializer):
    items = SaleItemSerializer(many=True)
    payments = PaymentSerializer(many=True, required=False)

    class Meta:
        model = Sale
        fields = "__all__"
        read_only_fields = [
            "invoice_no", "branch", "cashier", "shift", "status", "subtotal",
            "discount_total", "tax_total", "grand_total", "paid_amount",
            "fbr_status", "fbr_invoice_number", "fbr_qr_payload",
            "fbr_synced_at", "fbr_response",
        ]
        extra_kwargs = {"idempotency_key": {"required": True}} 

    def validate_items(self, items):
        if not items:
            raise serializers.ValidationError("Add at least one item.")
        return items

    @transaction.atomic
    def create(self, validated_data):
        user = self.context["request"].user
        items = validated_data.pop("items")
        payments = validated_data.pop("payments", [])
        warehouse = validated_data["warehouse"]

        shift = CashRegisterShift.objects.filter(
            cashier=user, status=CashRegisterShift.Status.OPEN, branch=warehouse.branch
        ).first()
        if not shift:
            raise serializers.ValidationError("Open a cash register shift for this branch first.")

        sale = Sale.objects.create(
            invoice_no=make_number("INV"), branch=warehouse.branch, cashier=user,
            shift=shift, status=Sale.Status.COMPLETED, **validated_data,
        )

        subtotal = discount_total = tax_total = ZERO
        for line in items:
            variant = line["variant"]
            qty = line["quantity"]
            stock_item = line.get("stock_item")
            imei = line.get("imei")
            product = variant.product
            cost = variant.cost_price

            if product.tracking_type == SERIALIZED:
                if qty != 1:
                    raise serializers.ValidationError(f"{variant}: sell phones one per line.")
                if imei:
                    stock_item = StockItem.objects.select_for_update().filter(
                        Q(imei1=imei) | Q(imei2=imei)).first()
                elif stock_item:
                    stock_item = StockItem.objects.select_for_update().get(pk=stock_item.pk)
                if not stock_item:
                    raise serializers.ValidationError(f"{variant}: IMEI is required.")
                if (stock_item.variant_id != variant.id
                        or stock_item.warehouse_id != warehouse.id
                        or stock_item.status != StockItem.Status.IN_STOCK):
                    raise serializers.ValidationError(
                        f"IMEI {stock_item.imei1} is not available for {variant} in this warehouse.")
                cost = stock_item.purchase_cost
                stock_item.status = StockItem.Status.SOLD
                stock_item.save(update_fields=["status", "updated_at"])
            else:
                stock_item = None

            if product.product_type != Product.ProductType.SERVICE:
                change_stock(variant, warehouse, -qty, StockMovement.MovementType.SALE,
                             "SALE", sale.id, user, stock_item)

            price = variant.selling_price
            discount = line.get("discount", ZERO)
            gross = money(price * qty)
            if discount > gross:
                raise serializers.ValidationError(f"{variant}: discount is more than the price.")
            tax = money((gross - discount) * variant.tax_rate / 100)
            SaleItem.objects.create(
                sale=sale, variant=variant, stock_item=stock_item, item_name=str(variant),
                hs_code=variant.hs_code, quantity=qty, unit_price=price, unit_cost=cost,
                discount=discount, tax_rate=variant.tax_rate, tax_amount=tax,
                line_total=gross - discount + tax,
            )
            subtotal += gross
            discount_total += discount
            tax_total += tax

        grand_total = subtotal - discount_total + tax_total

        paid = ZERO
        for pay in payments:
            if pay["method"] == PaymentMethod.CREDIT:
                raise serializers.ValidationError("Do not send a CREDIT payment; the unpaid rest becomes udhaar.")
            Payment.objects.create(sale=sale, received_by=user, **pay)
            paid += pay["amount"]
        if paid > grand_total:
            raise serializers.ValidationError("Paid amount is more than the invoice total.")

        customer = sale.customer
        due = grand_total - paid
        if due > 0:
            if not customer:
                raise serializers.ValidationError("Select a customer for credit (udhaar) sales.")
            if customer_balance(customer) + due > customer.credit_limit:
                raise serializers.ValidationError("Customer credit limit exceeded.")

        sale.subtotal, sale.discount_total = subtotal, discount_total
        sale.tax_total, sale.grand_total, sale.paid_amount = tax_total, grand_total, paid
        sale.save()

        if customer:
            CustomerLedger.objects.create(
                customer=customer, entry_type=LedgerEntryType.INVOICE, debit=grand_total,
                reference_type="SALE", reference_id=sale.id, note=sale.invoice_no, created_by=user)
            if paid:
                CustomerLedger.objects.create(
                    customer=customer, entry_type=LedgerEntryType.PAYMENT, credit=paid,
                    reference_type="SALE", reference_id=sale.id, note=sale.invoice_no, created_by=user)
        return sale


class SaleReturnItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleReturnItem
        fields = ["id", "sale_item", "quantity", "restock", "stock_item", "refund_amount"]
        read_only_fields = ["stock_item", "refund_amount"]
        extra_kwargs = {"quantity": {"min_value": Decimal("0.01")}}


class SaleReturnSerializer(serializers.ModelSerializer):
    items = SaleReturnItemSerializer(many=True)

    class Meta:
        model = SaleReturn
        fields = "__all__"
        read_only_fields = ["return_no", "refund_amount"]

    def validate_items(self, items):
        if not items:
            raise serializers.ValidationError("Add at least one item.")
        return items

    def validate(self, data):
        if data.get("refund_method") == PaymentMethod.CREDIT and not data["sale"].customer:
            raise serializers.ValidationError("A credit note needs a customer on the sale.")
        return data

    @transaction.atomic
    def create(self, validated_data):
        user = self.context["request"].user
        items = validated_data.pop("items")
        sale = Sale.objects.select_for_update().get(pk=validated_data["sale"].pk)
        if sale.status not in (Sale.Status.COMPLETED, Sale.Status.PARTIALLY_RETURNED):
            raise serializers.ValidationError("This sale cannot be returned.")

        ret = SaleReturn.objects.create(return_no=make_number("RET"), **validated_data)
        total = ZERO
        for line in items:
            sale_item, qty = line["sale_item"], line["quantity"]
            if sale_item.sale_id != sale.id:
                raise serializers.ValidationError("Item does not belong to this sale.")
            already = sale_item.returns.aggregate(q=Sum("quantity"))["q"] or ZERO
            if already + qty > sale_item.quantity:
                raise serializers.ValidationError(f"{sale_item.item_name}: returning more than was sold.")

            value = money(sale_item.line_total / sale_item.quantity * qty)
            SaleReturnItem.objects.create(
                sale_return=ret, sale_item=sale_item, quantity=qty, restock=line["restock"],
                stock_item=sale_item.stock_item, refund_amount=value)
            total += value

            product = sale_item.variant.product
            stock_item = sale_item.stock_item
            if stock_item:
                stock_item = StockItem.objects.select_for_update().get(pk=stock_item.pk)
                stock_item.status = StockItem.Status.IN_STOCK if line["restock"] else StockItem.Status.DAMAGED
                stock_item.warehouse = sale.warehouse
                stock_item.save(update_fields=["status", "warehouse", "updated_at"])
            if line["restock"] and product.product_type != Product.ProductType.SERVICE:
                change_stock(sale_item.variant, sale.warehouse, qty,
                             StockMovement.MovementType.SALE_RETURN, "RETURN", ret.id, user, stock_item)

        
        cash_refund = ZERO
        if ret.refund_method != PaymentMethod.CREDIT:
            before = sale.returns.exclude(pk=ret.pk).aggregate(t=Sum("refund_amount"))["t"] or ZERO
            cash_refund = max(min(total, sale.paid_amount - before), ZERO)
        ret.refund_amount = cash_refund
        ret.save()

        if sale.customer:
            CustomerLedger.objects.create(
                customer=sale.customer, entry_type=LedgerEntryType.RETURN, credit=total,
                reference_type="RETURN", reference_id=ret.id, note=ret.return_no, created_by=user)
            if cash_refund:
                CustomerLedger.objects.create(
                    customer=sale.customer, entry_type=LedgerEntryType.RETURN, debit=cash_refund,
                    reference_type="RETURN", reference_id=ret.id, note="Refund paid", created_by=user)

        fully = all((si.returns.aggregate(q=Sum("quantity"))["q"] or ZERO) >= si.quantity
                    for si in sale.items.all())
        sale.status = Sale.Status.RETURNED if fully else Sale.Status.PARTIALLY_RETURNED
        sale.save(update_fields=["status", "updated_at"])
        return ret


class CashRegisterShiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashRegisterShift
        fields = "__all__"
        read_only_fields = ["cashier", "status", "opened_at", "closed_at",
                            "expected_cash", "counted_cash", "difference"]
        extra_kwargs = {"opening_cash": {"min_value": ZERO}}

    def validate(self, data):
        user = self.context["request"].user
        if CashRegisterShift.objects.filter(cashier=user, status=CashRegisterShift.Status.OPEN).exists():
            raise serializers.ValidationError("You already have an open shift.")
        return data


class ShiftCloseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashRegisterShift
        fields = ["counted_cash", "notes"]
        extra_kwargs = {"counted_cash": {"required": True, "allow_null": False, "min_value": ZERO}}


class StockTransferItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockTransferItem
        fields = ["id", "variant", "stock_item", "quantity"]
        extra_kwargs = {"quantity": {"min_value": Decimal("0.01")}}

    def validate(self, data):
        variant, stock_item, qty = data["variant"], data.get("stock_item"), data["quantity"]
        check_quantity(variant, qty)
        if variant.product.tracking_type == SERIALIZED:
            if not stock_item or qty != 1:
                raise serializers.ValidationError("Phones need a stock_item (IMEI) and quantity 1.")
            if stock_item.variant_id != variant.id:
                raise serializers.ValidationError("IMEI does not belong to this variant.")
        return data


class StockTransferSerializer(serializers.ModelSerializer):
    items = StockTransferItemSerializer(many=True)

    class Meta:
        model = StockTransfer
        fields = "__all__"
        read_only_fields = ["transfer_no", "status"]

    def validate(self, data):
        if data["from_warehouse"] == data["to_warehouse"]:
            raise serializers.ValidationError("Choose two different warehouses.")
        if not data.get("items"):
            raise serializers.ValidationError("Add at least one item.")
        return data

    @transaction.atomic
    def create(self, validated_data):
        items = validated_data.pop("items")
        transfer = StockTransfer.objects.create(transfer_no=make_number("TRF"), **validated_data)
        for item in items:
            StockTransferItem.objects.create(transfer=transfer, **item)
        return transfer

class CustomerLedgerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerLedger
        fields = "__all__"


class SupplierLedgerSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplierLedger
        fields = "__all__"


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = "__all__"
        extra_kwargs = {"amount": {"min_value": Decimal("0.01")}}


class RepairJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepairJob
        fields = "__all__"
        read_only_fields = ["job_no", "delivered_at"]

    def create(self, validated_data):
        validated_data["job_no"] = make_number("JOB")
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if validated_data.get("status") == RepairJob.Status.DELIVERED and not instance.delivered_at:
            validated_data["delivered_at"] = timezone.now()
        return super().update(instance, validated_data)