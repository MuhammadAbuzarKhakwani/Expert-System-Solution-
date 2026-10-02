import uuid

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, RegexValidator
from django.db import models
from django.db.models import F, Q
from django.utils import timezone


phone_validator = RegexValidator(
    regex=r"^(\+92|0)\d{9,10}$",
    message="Enter a valid Pakistani number, e.g. 03001234567 or +923001234567.",
)

cnic_validator = RegexValidator(
    regex=r"^\d{13}$",
    message="CNIC must be 13 digits without dashes.",
)


def validate_imei(value):
    if not value.isdigit() or len(value) != 15:
        raise ValidationError("IMEI must be exactly 15 digits.")

    total = 0

    for index, digit in enumerate(reversed(value)):
        number = int(digit)

        if index % 2 == 1:
            number = number * 2

            if number > 9:
                number = number - 9

        total = total + number

    if total % 10 != 0:
        raise ValidationError("IMEI failed the Luhn check.")


class PaymentMethod(models.TextChoices):
    CASH = "CASH", "Cash"
    CARD = "CARD", "Card"
    BANK = "BANK", "Bank Transfer"
    JAZZCASH = "JAZZCASH", "JazzCash"
    EASYPAISA = "EASYPAISA", "Easypaisa"
    CREDIT = "CREDIT", "Credit (Udhaar)"


class PtaStatus(models.TextChoices):
    NOT_APPLICABLE = "NA", "Not applicable"
    APPROVED = "APPROVED", "PTA Approved"
    NON_PTA = "NON_PTA", "Non-PTA"
    JV = "JV", "JV / Locally assembled"


class LedgerEntryType(models.TextChoices):
    OPENING = "OPENING", "Opening balance"
    INVOICE = "INVOICE", "Invoice"
    PAYMENT = "PAYMENT", "Payment"
    RETURN = "RETURN", "Return"
    ADJUSTMENT = "ADJUSTMENT", "Adjustment"


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class AuditModel(TimeStampedModel):
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        editable=False,
    )

    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        editable=False,
    )

    class Meta:
        abstract = True


class Branch(TimeStampedModel):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    address = models.TextField()
    ntn = models.CharField("NTN", max_length=15, blank=True)
    strn = models.CharField("STRN", max_length=20, blank=True)
    fbr_pos_id = models.CharField(max_length=50, blank=True)
    fbr_token = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Warehouse(AuditModel):
    branch = models.ForeignKey(
        Branch,
        on_delete=models.PROTECT,
        related_name="warehouses",
    )

    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50, unique=True)
    address = models.TextField()

    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="managed_warehouses",
    )

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Category(TimeStampedModel):
    name = models.CharField(max_length=70, unique=True)
    description = models.TextField(blank=True)

    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="children",
    )

    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Brand(TimeStampedModel):
    name = models.CharField(max_length=70, unique=True)
    description = models.TextField(blank=True)

    logo = models.ImageField(
        upload_to="brands/",
        null=True,
        blank=True,
    )

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Product(AuditModel):
    class UnitChoices(models.TextChoices):
        PCS = "PCS", "Pieces"
        KG = "KG", "Kilogram"
        LITER = "LITER", "Liter"
        BOX = "BOX", "Box"

    class ProductType(models.TextChoices):
        PHONE = "PHONE", "Phone"
        ACCESSORY = "ACCESSORY", "Accessory"
        SERVICE = "SERVICE", "Service"

    class TrackingType(models.TextChoices):
        SERIALIZED = "SERIALIZED", "Serialized (IMEI per unit)"
        QUANTITY = "QUANTITY", "Quantity only"

    name = models.CharField(max_length=255)

    description = models.TextField(blank=True)

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products",
    )

    brand = models.ForeignKey(
        Brand,
        on_delete=models.PROTECT,
        related_name="products",
    )

    product_type = models.CharField(
        max_length=20,
        choices=ProductType.choices,
        default=ProductType.PHONE,
        db_index=True,
    )

    tracking_type = models.CharField(
        max_length=20,
        choices=TrackingType.choices,
        default=TrackingType.SERIALIZED,
    )

    unit = models.CharField(
        max_length=10,
        choices=UnitChoices.choices,
        default=UnitChoices.PCS,
    )

    warranty_months = models.PositiveSmallIntegerField(default=0)

    image = models.ImageField(
        upload_to="products/",
        null=True,
        blank=True,
    )

    is_active = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=(
                    ~Q(product_type="PHONE")
                    | Q(tracking_type="SERIALIZED")
                ),
                name="product_phone_must_be_serialized",
            ),
        ]

        indexes = [
            models.Index(fields=["name"]),
        ]

    def __str__(self):
        return self.name


class ProductVariant(AuditModel):
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="variants",
    )

    sku = models.CharField(
        max_length=100,
        unique=True,
    )

    barcode = models.CharField(
        max_length=100,
        unique=True,
        null=True,
        blank=True,
    )

    color = models.CharField(
        max_length=40,
        blank=True,
    )

    ram_gb = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
    )

    storage_gb = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
    )

    pta_status = models.CharField(
        max_length=10,
        choices=PtaStatus.choices,
        default=PtaStatus.NOT_APPLICABLE,
    )

    hs_code = models.CharField(
        max_length=20,
        blank=True,
    )

    tax_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        validators=[MaxValueValidator(100)],
    )

    cost_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    selling_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    minimum_stock = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    is_active = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=Q(cost_price__gte=0),
                name="variant_cost_price_gte_0",
            ),
            models.CheckConstraint(
                condition=Q(selling_price__gte=0),
                name="variant_selling_price_gte_0",
            ),
            models.CheckConstraint(
                condition=Q(minimum_stock__gte=0),
                name="variant_min_stock_gte_0",
            ),
        ]

    def save(self, *args, **kwargs):
        if not self.barcode:
            self.barcode = None

        super().save(*args, **kwargs)

    def __str__(self):
        parts = [self.product.name]

        if self.ram_gb and self.storage_gb:
            parts.append(f"{self.ram_gb}/{self.storage_gb}GB")

        if self.color:
            parts.append(self.color)

        return " ".join(parts)


class Supplier(AuditModel):
    name = models.CharField(max_length=70)

    company_name = models.CharField(
        max_length=150,
    )

    email = models.EmailField(
        blank=True,
    )

    phone = models.CharField(
        max_length=15,
        validators=[phone_validator],
        db_index=True,
    )

    address = models.TextField()

    tax_number = models.CharField(
        max_length=50,
        blank=True,
    )

    opening_balance = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=0,
    )

    credit_days = models.PositiveSmallIntegerField(
        default=0,
    )

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.company_name


class Customer(AuditModel):
    class CustomerType(models.TextChoices):
        RETAIL = "RETAIL", "Retail"
        WHOLESALE = "WHOLESALE", "Wholesale"
        DEALER = "DEALER", "Dealer"

    name = models.CharField(max_length=100)

    email = models.EmailField(
        blank=True,
    )

    phone = models.CharField(
        max_length=15,
        validators=[phone_validator],
        db_index=True,
    )

    cnic = models.CharField(
        max_length=13,
        blank=True,
        validators=[cnic_validator],
    )

    address = models.TextField(
        blank=True,
    )

    tax_number = models.CharField(
        max_length=50,
        blank=True,
    )

    customer_type = models.CharField(
        max_length=10,
        choices=CustomerType.choices,
        default=CustomerType.RETAIL,
    )

    credit_limit = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    opening_balance = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=0,
    )

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Stock(TimeStampedModel):
    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.PROTECT,
        related_name="stocks",
    )

    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.PROTECT,
        related_name="stocks",
    )

    quantity = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    reserved_quantity = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["variant", "warehouse"],
                name="unique_variant_warehouse",
            ),
            models.CheckConstraint(
                condition=Q(quantity__gte=0),
                name="stock_quantity_gte_0",
            ),
            models.CheckConstraint(
                condition=Q(reserved_quantity__gte=0),
                name="stock_reserved_gte_0",
            ),
            models.CheckConstraint(
                condition=Q(
                    reserved_quantity__lte=F("quantity")
                ),
                name="stock_reserved_lte_quantity",
            ),
        ]

    @property
    def available(self):
        return self.quantity - self.reserved_quantity

    def __str__(self):
        return f"{self.variant} - {self.warehouse}: {self.quantity}"


class StockItem(AuditModel):
    class Condition(models.TextChoices):
        NEW = "NEW", "New"
        USED = "USED", "Used"
        REFURBISHED = "REFURBISHED", "Refurbished"
        OPEN_BOX = "OPEN_BOX", "Open box"

    class Status(models.TextChoices):
        IN_STOCK = "IN_STOCK", "In stock"
        RESERVED = "RESERVED", "Reserved"
        SOLD = "SOLD", "Sold"
        IN_REPAIR = "IN_REPAIR", "In repair"
        DAMAGED = "DAMAGED", "Damaged"
        RETURNED_TO_SUPPLIER = (
            "RETURNED_TO_SUPPLIER",
            "Returned to supplier",
        )

    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.PROTECT,
        related_name="items",
    )

    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.PROTECT,
        related_name="items",
    )

    imei1 = models.CharField(
        max_length=15,
        unique=True,
        validators=[validate_imei],
    )

    imei2 = models.CharField(
        max_length=15,
        unique=True,
        null=True,
        blank=True,
        validators=[validate_imei],
    )

    condition = models.CharField(
        max_length=15,
        choices=Condition.choices,
        default=Condition.NEW,
    )

    pta_status = models.CharField(
        max_length=10,
        choices=PtaStatus.choices,
        default=PtaStatus.APPROVED,
    )

    purchase_cost = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    status = models.CharField(
        max_length=25,
        choices=Status.choices,
        default=Status.IN_STOCK,
        db_index=True,
    )

    supplier = models.ForeignKey(
        Supplier,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="+",
    )

    purchase_item = models.ForeignKey(
        "PurchaseItem",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="stock_items",
    )

    warranty_expiry = models.DateField(
        null=True,
        blank=True,
    )

    purchased_from_name = models.CharField(
        max_length=100,
        blank=True,
    )

    purchased_from_cnic = models.CharField(
        max_length=13,
        blank=True,
        validators=[cnic_validator],
    )

    purchased_from_phone = models.CharField(
        max_length=15,
        blank=True,
        validators=[phone_validator],
    )

    notes = models.TextField(
        blank=True,
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=~Q(imei1=F("imei2")),
                name="stockitem_imei1_ne_imei2",
            ),
            models.CheckConstraint(
                condition=Q(purchase_cost__gte=0),
                name="stockitem_cost_gte_0",
            ),
        ]

        indexes = [
            models.Index(
                fields=["variant", "warehouse", "status"]
            ),
        ]

    def save(self, *args, **kwargs):
        if not self.imei2:
            self.imei2 = None

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.variant} [{self.imei1}]"


class StockMovement(models.Model):
    class MovementType(models.TextChoices):
        OPENING = "OPENING", "Opening stock"
        PURCHASE = "PURCHASE", "Purchase"
        PURCHASE_RETURN = "PURCHASE_RETURN", "Purchase return"
        SALE = "SALE", "Sale"
        SALE_RETURN = "SALE_RETURN", "Sale return"
        TRANSFER_IN = "TRANSFER_IN", "Transfer in"
        TRANSFER_OUT = "TRANSFER_OUT", "Transfer out"
        ADJUSTMENT = "ADJUSTMENT", "Adjustment"

    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.PROTECT,
        related_name="movements",
    )

    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.PROTECT,
        related_name="movements",
    )

    stock_item = models.ForeignKey(
        StockItem,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="movements",
    )

    movement_type = models.CharField(
        max_length=20,
        choices=MovementType.choices,
        db_index=True,
    )

    quantity = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    reference_type = models.CharField(
        max_length=30,
    )

    reference_id = models.PositiveBigIntegerField()

    note = models.CharField(
        max_length=255,
        blank=True,
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=~Q(quantity=0),
                name="stockmovement_quantity_ne_0",
            ),
        ]

        indexes = [
            models.Index(
                fields=["reference_type", "reference_id"]
            ),
            models.Index(
                fields=["variant", "warehouse", "created_at"]
            ),
        ]

    def save(self, *args, **kwargs):
        if self.pk:
            raise ValidationError(
                "StockMovement rows are immutable."
            )

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise ValidationError(
            "StockMovement rows cannot be deleted."
        )


class PurchaseOrder(AuditModel):
    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Draft"
        ORDERED = "ORDERED", "Ordered"
        RECEIVED = "RECEIVED", "Received"
        CANCELLED = "CANCELLED", "Cancelled"

    po_number = models.CharField(
        max_length=30,
        unique=True,
    )

    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.PROTECT,
        related_name="purchase_orders",
    )

    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.PROTECT,
        related_name="purchase_orders",
    )

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.DRAFT,
        db_index=True,
    )

    order_date = models.DateField(
        default=timezone.localdate,
    )

    subtotal = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=0,
    )

    tax_total = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=0,
    )

    grand_total = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=0,
    )

    paid_amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=0,
    )

    notes = models.TextField(
        blank=True,
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=Q(
                    subtotal__gte=0,
                    tax_total__gte=0,
                    grand_total__gte=0,
                    paid_amount__gte=0,
                ),
                name="po_amounts_gte_0",
            ),
        ]

    def __str__(self):
        return self.po_number


class PurchaseItem(models.Model):
    purchase_order = models.ForeignKey(
        PurchaseOrder,
        on_delete=models.CASCADE,
        related_name="items",
    )

    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.PROTECT,
        related_name="+",
    )

    quantity = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    unit_cost = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    line_total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=Q(quantity__gt=0),
                name="purchaseitem_qty_gt_0",
            ),
            models.CheckConstraint(
                condition=Q(unit_cost__gte=0),
                name="purchaseitem_cost_gte_0",
            ),
        ]


class CashRegisterShift(TimeStampedModel):
    class Status(models.TextChoices):
        OPEN = "OPEN", "Open"
        CLOSED = "CLOSED", "Closed"

    branch = models.ForeignKey(
        Branch,
        on_delete=models.PROTECT,
        related_name="shifts",
    )

    cashier = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="shifts",
    )

    status = models.CharField(
        max_length=6,
        choices=Status.choices,
        default=Status.OPEN,
    )

    opened_at = models.DateTimeField(
        default=timezone.now,
    )

    closed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    opening_cash = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    expected_cash = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
    )

    counted_cash = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
    )

    difference = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
    )

    notes = models.TextField(
        blank=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["cashier"],
                condition=Q(status="OPEN"),
                name="one_open_shift_per_cashier",
            ),
        ]


class Sale(AuditModel):
    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Draft"
        COMPLETED = "COMPLETED", "Completed"
        CANCELLED = "CANCELLED", "Cancelled"
        PARTIALLY_RETURNED = (
            "PARTIALLY_RETURNED",
            "Partially returned",
        )
        RETURNED = "RETURNED", "Returned"

    class FbrStatus(models.TextChoices):
        NOT_REQUIRED = "NOT_REQUIRED", "Not required"
        PENDING = "PENDING", "Pending"
        SYNCED = "SYNCED", "Synced"
        FAILED = "FAILED", "Failed"

    invoice_no = models.CharField(
        max_length=30,
        unique=True,
    )

    idempotency_key = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
    )

    branch = models.ForeignKey(
        Branch,
        on_delete=models.PROTECT,
        related_name="sales",
    )

    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.PROTECT,
        related_name="sales",
    )

    customer = models.ForeignKey(
        Customer,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="sales",
    )

    cashier = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="sales",
    )

    shift = models.ForeignKey(
        CashRegisterShift,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="sales",
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
        db_index=True,
    )

    subtotal = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=0,
    )

    discount_total = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=0,
    )

    tax_total = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=0,
    )

    grand_total = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=0,
    )

    paid_amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=0,
    )

    fbr_status = models.CharField(
        max_length=12,
        choices=FbrStatus.choices,
        default=FbrStatus.NOT_REQUIRED,
        db_index=True,
    )

    fbr_invoice_number = models.CharField(
        max_length=40,
        null=True,
        blank=True,
    )

    fbr_qr_payload = models.TextField(
        blank=True,
    )

    fbr_synced_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    fbr_response = models.JSONField(
        null=True,
        blank=True,
    )

    notes = models.TextField(
        blank=True,
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=Q(
                    subtotal__gte=0,
                    discount_total__gte=0,
                    tax_total__gte=0,
                    grand_total__gte=0,
                    paid_amount__gte=0,
                ),
                name="sale_amounts_gte_0",
            ),
        ]

        indexes = [
            models.Index(fields=["created_at"]),
        ]

    @property
    def balance_due(self):
        return self.grand_total - self.paid_amount

    def __str__(self):
        return self.invoice_no


class SaleItem(models.Model):
    sale = models.ForeignKey(
        Sale,
        on_delete=models.CASCADE,
        related_name="items",
    )

    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.PROTECT,
        related_name="+",
    )

    stock_item = models.ForeignKey(
        StockItem,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="sale_items",
    )

    item_name = models.CharField(
        max_length=255,
    )

    hs_code = models.CharField(
        max_length=20,
        blank=True,
    )

    quantity = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    unit_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    unit_cost = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    discount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    tax_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
    )

    tax_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    line_total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=Q(quantity__gt=0),
                name="saleitem_qty_gt_0",
            ),
            models.CheckConstraint(
                condition=Q(unit_price__gte=0),
                name="saleitem_price_gte_0",
            ),
            models.CheckConstraint(
                condition=Q(discount__gte=0),
                name="saleitem_discount_gte_0",
            ),
        ]


class Payment(models.Model):
    sale = models.ForeignKey(
        Sale,
        on_delete=models.PROTECT,
        related_name="payments",
    )

    method = models.CharField(
        max_length=10,
        choices=PaymentMethod.choices,
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    reference = models.CharField(
        max_length=100,
        blank=True,
    )

    received_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=Q(amount__gt=0),
                name="payment_amount_gt_0",
            ),
        ]


class SaleReturn(AuditModel):
    return_no = models.CharField(
        max_length=30,
        unique=True,
    )

    sale = models.ForeignKey(
        Sale,
        on_delete=models.PROTECT,
        related_name="returns",
    )

    reason = models.TextField()

    refund_method = models.CharField(
        max_length=10,
        choices=PaymentMethod.choices,
        default=PaymentMethod.CASH,
    )

    refund_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=Q(refund_amount__gte=0),
                name="salereturn_refund_gte_0",
            ),
        ]

    def __str__(self):
        return self.return_no


class SaleReturnItem(models.Model):
    sale_return = models.ForeignKey(
        SaleReturn,
        on_delete=models.CASCADE,
        related_name="items",
    )

    sale_item = models.ForeignKey(
        SaleItem,
        on_delete=models.PROTECT,
        related_name="returns",
    )

    stock_item = models.ForeignKey(
        StockItem,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="+",
    )

    quantity = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    restock = models.BooleanField(
        default=True,
    )

    refund_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=Q(quantity__gt=0),
                name="returnitem_qty_gt_0",
            ),
        ]


class StockTransfer(AuditModel):
    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Draft"
        IN_TRANSIT = "IN_TRANSIT", "In transit"
        RECEIVED = "RECEIVED", "Received"
        CANCELLED = "CANCELLED", "Cancelled"

    transfer_no = models.CharField(
        max_length=30,
        unique=True,
    )

    from_warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.PROTECT,
        related_name="transfers_out",
    )

    to_warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.PROTECT,
        related_name="transfers_in",
    )

    status = models.CharField(
        max_length=12,
        choices=Status.choices,
        default=Status.DRAFT,
    )

    notes = models.TextField(
        blank=True,
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=~Q(
                    from_warehouse=F("to_warehouse")
                ),
                name="transfer_different_warehouses",
            ),
        ]


class StockTransferItem(models.Model):
    transfer = models.ForeignKey(
        StockTransfer,
        on_delete=models.CASCADE,
        related_name="items",
    )

    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.PROTECT,
        related_name="+",
    )

    stock_item = models.ForeignKey(
        StockItem,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="+",
    )

    quantity = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=Q(quantity__gt=0),
                name="transferitem_qty_gt_0",
            ),
        ]


class LedgerEntry(models.Model):
    entry_type = models.CharField(
        max_length=12,
        choices=LedgerEntryType.choices,
    )

    debit = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=0,
    )

    credit = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=0,
    )

    reference_type = models.CharField(
        max_length=30,
        blank=True,
    )

    reference_id = models.PositiveBigIntegerField(
        null=True,
        blank=True,
    )

    note = models.CharField(
        max_length=255,
        blank=True,
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        abstract = True


class CustomerLedger(LedgerEntry):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.PROTECT,
        related_name="ledger",
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=Q(
                    debit__gte=0,
                    credit__gte=0,
                ),
                name="custledger_amounts_gte_0",
            ),
        ]

        indexes = [
            models.Index(
                fields=["customer", "created_at"]
            ),
        ]


class SupplierLedger(LedgerEntry):
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.PROTECT,
        related_name="ledger",
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=Q(
                    debit__gte=0,
                    credit__gte=0,
                ),
                name="suppledger_amounts_gte_0",
            ),
        ]

        indexes = [
            models.Index(
                fields=["supplier", "created_at"]
            ),
        ]


class Expense(AuditModel):
    branch = models.ForeignKey(
        Branch,
        on_delete=models.PROTECT,
        related_name="expenses",
    )

    category = models.CharField(
        max_length=50,
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    paid_via = models.CharField(
        max_length=10,
        choices=PaymentMethod.choices,
        default=PaymentMethod.CASH,
    )

    note = models.CharField(
        max_length=255,
        blank=True,
    )

    date = models.DateField(
        default=timezone.localdate,
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=Q(amount__gt=0),
                name="expense_amount_gt_0",
            ),
        ]


class RepairJob(AuditModel):
    class Status(models.TextChoices):
        RECEIVED = "RECEIVED", "Received"
        DIAGNOSING = "DIAGNOSING", "Diagnosing"
        IN_REPAIR = "IN_REPAIR", "In repair"
        READY = "READY", "Ready"
        DELIVERED = "DELIVERED", "Delivered"
        CANCELLED = "CANCELLED", "Cancelled"

    job_no = models.CharField(
        max_length=30,
        unique=True,
    )

    customer = models.ForeignKey(
        Customer,
        on_delete=models.PROTECT,
        related_name="repairs",
    )

    device_model = models.CharField(
        max_length=100,
    )

    device_imei = models.CharField(
        max_length=15,
        blank=True,
        validators=[validate_imei],
    )

    issue = models.TextField()

    status = models.CharField(
        max_length=12,
        choices=Status.choices,
        default=Status.RECEIVED,
        db_index=True,
    )

    estimated_cost = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    final_cost = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
    )

    technician = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="repairs",
    )

    received_at = models.DateTimeField(
        default=timezone.now,
    )

    delivered_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.job_no
