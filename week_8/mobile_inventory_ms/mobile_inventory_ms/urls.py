"""
URL configuration for mobile_inventory_ms project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import json
from decimal import Decimal

from django.contrib import admin
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F
from django.urls import path, include
from django.views.decorators.http import require_POST
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from pos.models import (
    Branch,
    Brand,
    CashRegisterShift,
    Category,
    Customer,
    CustomerLedger,
    LedgerEntryType,
    Payment,
    Product,
    ProductVariant,
    Sale,
    SaleItem,
    Stock,
    Supplier,
    Warehouse,
)

GROUP_MANAGER = 'manager'
GROUP_CUSTOMER = 'customer'


def user_in_group(user, *group_names):
    if not user or not user.is_authenticated:
        return False
    return user.groups.filter(name__in=group_names).exists()


def role_context(request, extra_context=None):
    context = extra_context or {}
    is_manager = user_in_group(request.user, GROUP_MANAGER)
    is_customer = user_in_group(request.user, GROUP_CUSTOMER)
    context.update({
        'is_manager': is_manager,
        'is_customer': is_customer,
        'can_view_dashboard': True,
        'can_view_products': is_manager,
        'can_view_sales': is_manager,
        'can_view_stock': is_manager,
        'can_view_customers': is_manager or is_customer,
        'can_view_suppliers': is_manager,
        'can_add_products': is_manager,
        'can_add_sales': is_manager,
        'can_adjust_stock': is_manager,
        'can_manage_customers': is_manager,
        'can_manage_suppliers': is_manager,
    })
    return context


def require_group(*group_names):
    def decorator(view_func):
        def _wrapped(request, *args, **kwargs):
            if not user_in_group(request.user, *group_names):
                return redirect('home')
            return view_func(request, *args, **kwargs)
        return _wrapped
    return decorator


def ensure_demo_pos_data(user):
    branch = Branch.objects.filter(code='MAIN').first()
    if not branch:
        branch = Branch.objects.create(
            name='Main Branch',
            code='MAIN',
            address='Lahore, Pakistan',
            ntn='1234567-8',
            strn='1234567890123',
            is_active=True,
        )

    warehouse = Warehouse.objects.filter(code='WH-001').first()
    if not warehouse:
        warehouse = Warehouse.objects.create(
            branch=branch,
            name='Main Warehouse',
            code='WH-001',
            address='Main City Market, Lahore',
            manager=user,
            is_active=True,
        )

    if not Customer.objects.filter(phone='03001234567').exists():
        Customer.objects.create(
            name='Walk-in Customer',
            phone='03001234567',
            cnic='3520212345678',
            address='Lahore',
            customer_type=Customer.CustomerType.RETAIL,
            credit_limit=0,
            opening_balance=0,
            is_active=True,
            created_by=user,
            updated_by=user,
        )

    if not CashRegisterShift.objects.filter(cashier=user, status=CashRegisterShift.Status.OPEN).exists():
        CashRegisterShift.objects.create(
            branch=branch,
            cashier=user,
            status=CashRegisterShift.Status.OPEN,
            opening_cash=Decimal('0.00'),
            expected_cash=Decimal('0.00'),
            counted_cash=Decimal('0.00'),
            difference=Decimal('0.00'),
        )

    if not Category.objects.exists():
        phones = Category.objects.create(name='Phones', description='Mobile phones', is_active=True)
        accessories = Category.objects.create(name='Accessories', description='Accessories', is_active=True)
    else:
        phones = Category.objects.filter(name='Phones').first() or Category.objects.first()
        accessories = Category.objects.filter(name='Accessories').first() or Category.objects.first()

    if not Brand.objects.exists():
        samsung = Brand.objects.create(name='Samsung', description='Samsung brand')
        apple = Brand.objects.create(name='Apple', description='Apple brand')
        others = Brand.objects.create(name='Generic', description='Generic accessories')
    else:
        samsung = Brand.objects.filter(name='Samsung').first() or Brand.objects.first()
        apple = Brand.objects.filter(name='Apple').first() or Brand.objects.first()
        others = Brand.objects.filter(name='Generic').first() or Brand.objects.first()

    if not ProductVariant.objects.exists():
        samsung_phone = Product.objects.create(
            name='Samsung A54',
            description='5G smartphone',
            category=phones,
            brand=samsung,
            product_type=Product.ProductType.PHONE,
            tracking_type=Product.TrackingType.SERIALIZED,
            unit=Product.UnitChoices.PCS,
            warranty_months=12,
            is_active=True,
            created_by=user,
            updated_by=user,
        )
        apple_phone = Product.objects.create(
            name='iPhone 14',
            description='Apple smartphone',
            category=phones,
            brand=apple,
            product_type=Product.ProductType.PHONE,
            tracking_type=Product.TrackingType.SERIALIZED,
            unit=Product.UnitChoices.PCS,
            warranty_months=12,
            is_active=True,
            created_by=user,
            updated_by=user,
        )
        cable = Product.objects.create(
            name='USB Type-C Cable',
            description='Fast charging cable',
            category=accessories,
            brand=others,
            product_type=Product.ProductType.ACCESSORY,
            tracking_type=Product.TrackingType.QUANTITY,
            unit=Product.UnitChoices.PCS,
            warranty_months=0,
            is_active=True,
            created_by=user,
            updated_by=user,
        )
        charger = Product.objects.create(
            name='Wireless Charger',
            description='Fast wireless charger',
            category=accessories,
            brand=others,
            product_type=Product.ProductType.ACCESSORY,
            tracking_type=Product.TrackingType.QUANTITY,
            unit=Product.UnitChoices.PCS,
            warranty_months=0,
            is_active=True,
            created_by=user,
            updated_by=user,
        )

        ProductVariant.objects.create(
            product=samsung_phone,
            sku='SAM-A54-8-128',
            barcode='SAM-A54-001',
            color='Blue',
            ram_gb=8,
            storage_gb=128,
            tax_rate=Decimal('18.00'),
            cost_price=Decimal('76000.00'),
            selling_price=Decimal('89000.00'),
            minimum_stock=Decimal('5.00'),
            is_active=True,
            created_by=user,
            updated_by=user,
        )
        ProductVariant.objects.create(
            product=apple_phone,
            sku='IPH-14-128',
            barcode='IPH-14-001',
            color='Midnight',
            ram_gb=6,
            storage_gb=128,
            tax_rate=Decimal('18.00'),
            cost_price=Decimal('185000.00'),
            selling_price=Decimal('201000.00'),
            minimum_stock=Decimal('5.00'),
            is_active=True,
            created_by=user,
            updated_by=user,
        )
        ProductVariant.objects.create(
            product=cable,
            sku='USB-C-001',
            barcode='USB-C-001',
            tax_rate=Decimal('18.00'),
            cost_price=Decimal('350.00'),
            selling_price=Decimal('1200.00'),
            minimum_stock=Decimal('20.00'),
            is_active=True,
            created_by=user,
            updated_by=user,
        )
        ProductVariant.objects.create(
            product=charger,
            sku='WIRELESS-CHG-001',
            barcode='WIRELESS-CHG-001',
            tax_rate=Decimal('18.00'),
            cost_price=Decimal('700.00'),
            selling_price=Decimal('3500.00'),
            minimum_stock=Decimal('12.00'),
            is_active=True,
            created_by=user,
            updated_by=user,
        )

    if not Stock.objects.exists():
        for variant in ProductVariant.objects.all():
            qty = Decimal('15.00') if variant.product.product_type == Product.ProductType.ACCESSORY else Decimal('5.00')
            Stock.objects.create(
                variant=variant,
                warehouse=warehouse,
                quantity=qty,
                reserved_quantity=Decimal('0.00'),
            )

    return branch, warehouse


def calculate_customer_due(customer):
    debit = sum(entry.debit for entry in customer.ledger.all())
    credit = sum(entry.credit for entry in customer.ledger.all())
    return customer.opening_balance + debit - credit


def calculate_supplier_due(supplier):
    debit = sum(entry.debit for entry in supplier.ledger.all())
    credit = sum(entry.credit for entry in supplier.ledger.all())
    return supplier.opening_balance + credit - debit


@login_required(login_url='login_page')
def home(request):
    ensure_demo_pos_data(request.user)
    context = role_context(request)
    products = ProductVariant.objects.select_related('product', 'product__category', 'product__brand').filter(is_active=True)
    stock_items = Stock.objects.select_related('variant__product', 'warehouse').order_by('quantity')
    sales = Sale.objects.select_related('customer', 'warehouse', 'branch', 'cashier').order_by('-created_at')[:5]
    low_stock = stock_items.filter(quantity__lte=F('variant__minimum_stock'))
    recent_sales_total = sales.aggregate(total=Sum('grand_total'))['total'] or Decimal('0')
    customer_total_due = sum(calculate_customer_due(customer) for customer in Customer.objects.prefetch_related('ledger').all())
    supplier_total_due = sum(calculate_supplier_due(supplier) for supplier in Supplier.objects.prefetch_related('ledger').all())

    context.update({
        'total_products': products.count(),
        'total_variants': products.count(),
        'low_stock_count': low_stock.count(),
        'today_revenue': recent_sales_total,
        'customer_due': customer_total_due,
        'supplier_due': supplier_total_due,
        'recent_sales': sales,
        'low_stock_items': low_stock[:6],
    })
    return render(request, 'pos/index.html', context)


def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')

    return render(request, 'pos/login.html')


def logout_page(request):
    logout(request)
    return redirect('login_page')


@login_required(login_url='login_page')
@require_group(GROUP_MANAGER)
def products_page(request):
    ensure_demo_pos_data(request.user)
    context = role_context(request)
    variants = ProductVariant.objects.select_related('product', 'product__category', 'product__brand').filter(is_active=True).order_by('product__name')
    stock_by_variant = Stock.objects.select_related('variant__product', 'warehouse')
    stock_lookup = {stock.variant_id: stock for stock in stock_by_variant}
    for variant in variants:
        stock = stock_lookup.get(variant.id)
        variant.stock_quantity = stock.quantity if stock else 0
    context['variants'] = variants
    return render(request, 'pos/products.html', context)


@login_required(login_url='login_page')
@require_group(GROUP_MANAGER)
def sales_page(request):
    ensure_demo_pos_data(request.user)
    context = role_context(request)
    quick_products = ProductVariant.objects.select_related('product', 'product__category').filter(is_active=True).order_by('-selling_price')[:8]
    sales = Sale.objects.select_related('customer', 'warehouse', 'branch').order_by('-created_at')[:10]
    customers = Customer.objects.filter(is_active=True).order_by('name')
    warehouse = Warehouse.objects.filter(code='WH-001').first()
    context.update({'quick_products': quick_products, 'recent_sales': sales, 'customers': customers, 'warehouse_id': warehouse.id if warehouse else None})
    return render(request, 'pos/sales.html', context)


@login_required(login_url='login_page')
@require_group(GROUP_MANAGER)
def stock_page(request):
    ensure_demo_pos_data(request.user)
    context = role_context(request)
    stock_items = Stock.objects.select_related('variant__product', 'warehouse').order_by('variant__product__name')
    context['stock_items'] = stock_items
    return render(request, 'pos/stock.html', context)


@login_required(login_url='login_page')
@require_group(GROUP_MANAGER)
def customers_page(request):
    ensure_demo_pos_data(request.user)
    context = role_context(request)
    customers = Customer.objects.prefetch_related('ledger').filter(is_active=True).order_by('name')
    for customer in customers:
        customer.balance = calculate_customer_due(customer)
    context['customers'] = customers
    return render(request, 'pos/customers.html', context)


@login_required(login_url='login_page')
@require_group(GROUP_MANAGER)
def suppliers_page(request):
    ensure_demo_pos_data(request.user)
    context = role_context(request)
    suppliers = Supplier.objects.prefetch_related('ledger').filter(is_active=True).order_by('company_name')
    for supplier in suppliers:
        supplier.balance = calculate_supplier_due(supplier)
    context['suppliers'] = suppliers
    return render(request, 'pos/suppliers.html', context)


@require_POST
@login_required(login_url='login_page')
def save_sale(request):
    try:
        payload = json.loads(request.body or '{}')
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON payload.'}, status=400)

    warehouse_id = payload.get('warehouse')
    customer_id = payload.get('customer')
    items = payload.get('items', [])
    payments = payload.get('payments', [])

    if not items:
        return JsonResponse({'error': 'Cart is empty.'}, status=400)

    try:
        warehouse = Warehouse.objects.get(id=warehouse_id)
    except Warehouse.DoesNotExist:
        return JsonResponse({'error': 'Warehouse not found.'}, status=400)

    customer = None
    if customer_id:
        try:
            customer = Customer.objects.get(id=customer_id)
        except Customer.DoesNotExist:
            return JsonResponse({'error': 'Customer not found.'}, status=400)

    shift = CashRegisterShift.objects.filter(cashier=request.user, status=CashRegisterShift.Status.OPEN, branch=warehouse.branch).first()
    if not shift:
        return JsonResponse({'error': 'Open a cash register shift first.'}, status=400)

    sale = Sale.objects.create(
        invoice_no=f'INV-{Sale.objects.count() + 1:05d}',
        branch=warehouse.branch,
        warehouse=warehouse,
        customer=customer,
        cashier=request.user,
        shift=shift,
        status=Sale.Status.COMPLETED,
        subtotal=0,
        discount_total=0,
        tax_total=0,
        grand_total=0,
        paid_amount=0,
        created_by=request.user,
        updated_by=request.user,
    )

    subtotal = Decimal('0')
    tax_total = Decimal('0')
    payment_total = Decimal('0')

    for entry in items:
        variant = ProductVariant.objects.filter(id=entry.get('variant')).first()
        if not variant:
            return JsonResponse({'error': f'Product variant not found: {entry.get("variant")}'}, status=400)

        qty = Decimal(str(entry.get('quantity', 1)))
        if qty <= 0:
            return JsonResponse({'error': 'Quantity must be greater than zero.'}, status=400)

        stock = Stock.objects.filter(variant=variant, warehouse=warehouse).first()
        if not stock or stock.quantity < qty:
            return JsonResponse({'error': f'Not enough stock for {variant.product.name}.'}, status=400)

        stock.quantity -= qty
        stock.save(update_fields=['quantity', 'updated_at'])

        line_total = variant.selling_price * qty
        tax_amount = (line_total * variant.tax_rate / Decimal('100'))
        subtotal += line_total
        tax_total += tax_amount

        SaleItem.objects.create(
            sale=sale,
            variant=variant,
            item_name=str(variant),
            hs_code=variant.hs_code or '',
            quantity=qty,
            unit_price=variant.selling_price,
            unit_cost=variant.cost_price,
            discount=Decimal(str(entry.get('discount', 0))),
            tax_rate=variant.tax_rate,
            tax_amount=tax_amount,
            line_total=line_total + tax_amount,
            created_by=request.user,
        )

    for pay in payments:
        method = pay.get('method', 'CASH')
        amount = Decimal(str(pay.get('amount', 0)))
        if amount <= 0:
            continue
        Payment.objects.create(
            sale=sale,
            method=method,
            amount=amount,
            reference=pay.get('reference', ''),
            received_by=request.user,
        )
        payment_total += amount

    sale.subtotal = subtotal
    sale.tax_total = tax_total
    sale.grand_total = subtotal + tax_total
    sale.paid_amount = min(payment_total, sale.grand_total)
    sale.save(update_fields=['subtotal', 'tax_total', 'grand_total', 'paid_amount', 'updated_at'])

    if customer and sale.grand_total > sale.paid_amount:
        due = sale.grand_total - sale.paid_amount
        if customer.opening_balance + due > customer.credit_limit:
            return JsonResponse({'error': 'Customer credit limit exceeded.'}, status=400)

    if customer:
        CustomerLedger.objects.create(
            customer=customer,
            entry_type=LedgerEntryType.INVOICE,
            debit=sale.grand_total,
            reference_type='SALE',
            reference_id=sale.id,
            note=sale.invoice_no,
            created_by=request.user,
        )
        if sale.paid_amount > 0:
            CustomerLedger.objects.create(
                customer=customer,
                entry_type=LedgerEntryType.PAYMENT,
                credit=sale.paid_amount,
                reference_type='SALE',
                reference_id=sale.id,
                note=sale.invoice_no,
                created_by=request.user,
            )

    return JsonResponse({'success': True, 'sale_id': sale.id, 'invoice_no': sale.invoice_no, 'total': str(sale.grand_total)})


urlpatterns = [
    path('', home, name='home'),
    path('login-page/', login_page, name='login_page'),
    path('logout/', logout_page, name='logout'),
    path('products/', products_page, name='products_page'),
    path('sales/', sales_page, name='sales_page'),
    path('stock/', stock_page, name='stock_page'),
    path('customers/', customers_page, name='customers_page'),
    path('suppliers/', suppliers_page, name='suppliers_page'),
    path('save-sale/', save_sale, name='save_sale'),
    path('admin/', admin.site.urls),
    path('pos/', include('pos.urls')),
    path('login', TokenObtainPairView.as_view()),
    path('refresh', TokenRefreshView.as_view()),
]
