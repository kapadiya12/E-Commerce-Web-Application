from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.db import transaction
from django.db.models import Q, Sum
from django.core.mail import send_mail
from django.template.loader import render_to_string
from decimal import Decimal
from datetime import datetime
from .models import Product, Cart, CartItem, Order, OrderItem, Category
from .forms import AddToCartForm, UpdateCartItemForm, CheckoutForm, RegisterForm, LoginForm
from django.core.mail import EmailMessage
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import io
from decimal import Decimal


def get_or_create_cart(request):
    """Get or create cart for the session or user"""

    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key

    # If user is logged in, get cart by user
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(
            user=request.user,
            defaults={'session_key': session_key}
        )
    else:
        # Guest user: cart by session
        cart, created = Cart.objects.get_or_create(
            session_key=session_key,
            user=None
        )

    return cart

def product_list(request):
    """Display all products - Protected view"""
    if not request.user.is_authenticated:
        messages.error(request, 'Please login to view products.')
        return redirect('user_login')

    
    categories = Category.objects.all() 
    products = Product.objects.select_related("category").all()
    # cart_count = get_cart_count(request)
    context = {
        'products': products,
        'page_title': 'Products',
        # 'cart_count': cart_count,
        'categories': categories,
    }
    return render(request, 'shop/product_list.html', context)


def product_detail(request, pk):
    """Display product details - Protected view"""
    if not request.user.is_authenticated:
        messages.error(request, 'Please login to view product details.')
        return redirect('user_login')
    
    product = get_object_or_404(Product, pk=pk)
    # cart_count = get_cart_count(request)
    form = AddToCartForm()
    
    context = {
        'product': product,
        'form': form,
        'page_title': product.name,
        # 'cart_count': cart_count
    }
    return render(request, 'shop/product_detail.html', context)

@require_http_methods(["POST"])
def add_to_cart(request, pk):
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': 'Please login first.'}, status=401)

    product = get_object_or_404(Product, pk=pk)
    cart = get_or_create_cart(request)

    if product.stock < 1:
        return JsonResponse({'success': False, 'error': 'Out of stock.'})

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': 1}
    )

    if not created:
        if cart_item.quantity + 1 > product.stock:
            return JsonResponse({
                'success': False,
                'error': f'Only {product.stock} items available.'
            })
        cart_item.quantity += 1
        cart_item.save()

    return JsonResponse({
        'success': True,
        'message': 'Added to cart',
        'cart_count': cart.get_item_count(),
        'item_qty': cart_item.quantity,
    })

@login_required(login_url='user_login')
def view_cart(request):
    """Display shopping cart - Protected view"""
    if not request.user.is_authenticated:
        messages.error(request, 'Please login to view your cart.')
        return redirect('user_login')

    
    cart = get_or_create_cart(request)
    cart_items = cart.items.all()
    # cart_count = get_cart_count(request)
    
    # Create form instances for each item
    forms_dict = {}
    for item in cart_items:
        forms_dict[item.id] = UpdateCartItemForm(instance=item)
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'total': cart.get_total(),
        'forms_dict': forms_dict,
        'page_title': 'Shopping Cart',
        # 'cart_count': cart_count
    }
    return render(request, 'shop/cart.html', context)


@require_http_methods(["POST"])
def update_cart_item(request, item_id):
    """Update quantity of cart item"""
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart = get_or_create_cart(request)
    
    # Verify cart ownership
    if cart_item.cart.id != cart.id:
        messages.error(request, 'Invalid cart item.')
        return redirect('view_cart')
    
    form = UpdateCartItemForm(request.POST, instance=cart_item)
    
    if form.is_valid():
        form.save()
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': 'Cart updated successfully!',
                'new_subtotal': float(cart_item.get_subtotal()),
                'new_total': float(cart.get_total()),
                'cart_count': cart.get_item_count()
            })
        messages.success(request, 'Cart updated successfully!')
    else:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'errors': form.errors
            }, status=400)
        
        for field, errors in form.errors.items():
            messages.error(request, f'{field}: {", ".join(errors)}')
    
    return redirect('view_cart')


@require_http_methods(["POST"])
def remove_from_cart(request, item_id):
    """Remove item from cart"""
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart = get_or_create_cart(request)
    
    # Verify cart ownership
    if cart_item.cart.id != cart.id:
        messages.error(request, 'Invalid cart item.')
        return redirect('view_cart')
    
    product_name = cart_item.product.name
    cart_item.delete()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': f'{product_name} removed from cart!',
            'cart_count': cart.get_item_count(),
            'cart_total': float(cart.get_total())
        })
    
    messages.success(request, f'{product_name} removed from cart!')
    return redirect('view_cart')


def checkout(request):
    """Checkout page - Protected view"""
    if not request.user.is_authenticated:
        messages.error(request, 'Please login to proceed with checkout.')
        return redirect('user_login')

    cart = get_or_create_cart(request)
    cart_items = cart.items.all()

    if not cart_items.exists():
        messages.error(request, 'Your cart is empty!')
        return redirect('product_list')
    
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        
        if form.is_valid():
            try:
                with transaction.atomic():

                    # ====== CALCULATE TOTAL ======
                    subtotal = cart.get_total()
                    tax = subtotal * Decimal('0.18')
                    grand_total = subtotal + tax

                    # ====== CREATE ORDER ======
                    order = Order.objects.create(
                        first_name=form.cleaned_data['first_name'],
                        last_name=form.cleaned_data['last_name'],
                        email=form.cleaned_data['email'],
                        phone=form.cleaned_data['phone'],
                        address=form.cleaned_data['address'],
                        city=form.cleaned_data['city'],
                        state=form.cleaned_data['state'],
                        postal_code=form.cleaned_data['postal_code'],
                        total_amount=grand_total,
                        payment_method=form.cleaned_data['payment_method'],
                        status='pending',
                        user=request.user
                    )

                    # ====== CREATE ORDER ITEMS ======
                    for cart_item in cart_items:
                        OrderItem.objects.create(
                            order=order,
                            product=cart_item.product,
                            quantity=cart_item.quantity,
                            price=cart_item.product.price
                        )

                        # Reduce stock
                        product = cart_item.product
                        product.stock -= cart_item.quantity
                        product.save()

                    # ====== CLEAR CART ======
                    cart.items.all().delete()

                    # =====================================================
                    # =============== GENERATE PDF IN MEMORY ===============
                    # =====================================================
                    buffer = io.BytesIO()
                    p = canvas.Canvas(buffer, pagesize=A4)

                    p.setFont("Helvetica-Bold", 18)
                    p.drawString(50, 800, "ShopHub - Invoice")

                    p.setFont("Helvetica", 11)
                    p.drawString(50, 770, f"Order ID: {order.id}")
                    p.drawString(50, 750, f"Customer: {order.first_name} {order.last_name}")
                    p.drawString(50, 730, f"Email: {order.email}")

                    y = 700
                    p.drawString(50, y, "Items:")
                    y -= 20

                    calc_subtotal = Decimal("0.00")

                    for item in order.items.all():
                        line_total = item.price * item.quantity
                        calc_subtotal += line_total

                        p.drawString(50, y, f"{item.product.name} (x{item.quantity})")
                        p.drawString(400, y, f"₹{line_total}")
                        y -= 20

                    calc_tax = calc_subtotal * Decimal("0.18")
                    calc_grand = calc_subtotal + calc_tax

                    y -= 30
                    p.drawString(50, y, f"Subtotal: ₹{calc_subtotal}")
                    y -= 20
                    p.drawString(50, y, f"GST (18%): ₹{calc_tax}")
                    y -= 20
                    p.setFont("Helvetica-Bold", 12)
                    p.drawString(50, y, f"Grand Total: ₹{calc_grand}")

                    p.showPage()
                    p.save()

                    buffer.seek(0)

                    # =====================================================
                    # ================= SEND EMAIL + PDF ==================
                    # =====================================================
                    email_subject = f"ShopHub Invoice - Order #{order.id}"

                    email_body = f"""
Hello {order.first_name},

Thank you for shopping with ShopHub ❤️

Your order has been placed successfully.

Order ID: {order.id}
Total Amount: ₹{calc_grand}

Your invoice PDF is attached with this email.

We will ship your order soon.

Thanks & Regards,
ShopHub Team
"""

                    email = EmailMessage(
                        subject=email_subject,
                        body=email_body,
                        from_email="king143krish@gmail.com",
                        to=[order.email],
                    )

                    email.attach(
                        f"invoice_{order.id}.pdf",
                        buffer.getvalue(),
                        "application/pdf"
                    )

                    email.send(fail_silently=False)

                    messages.success(request, 'Order placed successfully! Invoice sent to your email.')
                    return redirect('order_confirmation', order_id=order.id)

            except Exception as e:
                print("CHECKOUT ERROR:", e)
                messages.error(request, 'An error occurred while placing your order.')
                return redirect('checkout')

        else:
            for field, errors in form.errors.items():
                messages.error(request, f'{field}: {", ".join(errors)}')
    else:
        form = CheckoutForm(initial={
            'email': request.user.email,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
        })

    # cart_count = get_cart_count(request)
    subtotal = cart.get_total()
    tax = subtotal * Decimal('0.18')
    grand_total = subtotal + tax

    context = {
        'form': form,
        'cart': cart,
        'cart_items': cart_items,
        'subtotal': subtotal,
        'tax': tax,
        'grand_total': grand_total,
        'page_title': 'Checkout',
        # 'cart_count': cart_count
    }

    return render(request, 'shop/checkout.html', context)


def order_confirmation(request, order_id):
    """Order confirmation page"""
    from django.core.mail import send_mail
    from django.conf import settings
    
    order = get_object_or_404(Order, id=order_id)
    order_items = order.items.all()
    # cart_count = get_cart_count(request)
    
    # Send confirmation email
    try:
        email_subject = f'Order Confirmation #{order.id} - ShopHub'
        email_body = f"""
Hello {order.first_name},

Thank you for your order!

Order Number: #{order.id}
Order Date: {order.created_at.strftime('%d-%m-%Y %H:%M:%S')}
Status: {order.get_status_display()}

Delivery Address:
{order.address}
{order.city}, {order.state} {order.postal_code}

Order Summary:
Subtotal: Rs{order.get_subtotal():.2f}
Shipping: FREE
Tax (18% GST): Rs{order.get_tax():.2f}
Total Amount: Rs{order.total_amount:.2f}

Payment Method: Cash on Delivery (COD)
You'll pay when your order arrives at your doorstep.

We'll process your order shortly and send you tracking details.

Thank you for shopping with us!

Best regards,
ShopHub Team
support@shophub.com
        """
        
        send_mail(
            email_subject,
            email_body,
            settings.EMAIL_HOST_USER,   # sender
            [order.email],              # receiver (customer)
            fail_silently=False         # show error if email fails
        )
    except Exception as e:
        print(f"Error sending email: {e}")
    
    context = {
        'order': order,
        'order_items': order_items,
        'page_title': 'Order Confirmation',
        # 'cart_count': cart_count
    }
    return render(request, 'shop/order_confirmation.html', context)

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from django.http import FileResponse
import io

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from django.http import FileResponse
import io
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from django.http import FileResponse
import io
from decimal import Decimal

@login_required(login_url='user_login')
def download_invoice(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Colors & fonts
    p.setStrokeColor(colors.HexColor("#9ca3af"))  # soft gray
    p.setLineWidth(0.7)

    y = height - 50

    # ===== HEADER =====
    p.setFont("Helvetica-Bold", 18)
    p.drawString(50, y, "ShopHub")
    
    p.setFont("Helvetica", 11)
    p.drawRightString(width-50, y, f"Order ID: {order.id}")
    y -= 20
    p.drawRightString(width-50, y, f"Date: {order.created_at.strftime('%d-%m-%Y')}")

    # Line
    y -= 20
    p.line(50, y, width-50, y)

    # ===== INVOICE TITLE =====
    y -= 40
    p.setFont("Helvetica-Bold", 22)
    p.drawString(50, y, "INVOICE")

    # ===== BILL TO =====
    y -= 40
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, y, "Bill To:")

    p.setFont("Helvetica", 11)
    y -= 18
    p.drawString(50, y, f"Name: {order.first_name} {order.last_name}")
    y -= 16
    p.drawString(50, y, f"Phone: {order.phone}")
    y -= 16
    p.drawString(50, y, f"Address: {order.address}, {order.city}, {order.state} - {order.postal_code}")

    # ===== TABLE HEADER =====
    y -= 40
    p.line(50, y, width-50, y)
    y -= 20

    p.setFont("Helvetica-Bold", 11)
    p.drawString(50, y, "Item")
    p.drawString(300, y, "Qty")
    p.drawString(360, y, "Price")
    p.drawString(450, y, "Total")

    y -= 10
    p.line(50, y, width-50, y)

    # ===== ITEMS =====
    p.setFont("Helvetica", 11)
    y -= 20

    subtotal = Decimal("0.00")

    for item in order.items.all():
        line_total = item.price * item.quantity
        subtotal += line_total

        p.drawString(50, y, item.product.name[:40])
        p.drawString(300, y, str(item.quantity))
        p.drawString(360, y, f"Rs. {item.price:.2f}")
        p.drawString(450, y, f"Rs. {line_total:.2f}")
        y -= 20

        if y < 150:
            p.showPage()
            y = height - 100

    # ===== TOTALS =====
    y -= 10
    p.line(50, y, width-50, y)

    tax = subtotal * Decimal("0.18")
    grand_total = subtotal + tax

    y -= 30
    p.setFont("Helvetica", 11)
    p.drawRightString(430, y, "Subtotal:")
    p.drawRightString(width-50, y, f"Rs. {subtotal:.2f}")

    y -= 20
    p.drawRightString(430, y, "GST (18%):")
    p.drawRightString(width-50, y, f"Rs. {tax:.2f}")

    y -= 25
    p.setFont("Helvetica-Bold", 12)
    p.drawRightString(430, y, "Grand Total:")
    p.drawRightString(width-50, y, f"Rs. {grand_total:.2f}")

    # ===== FOOTER =====
    y -= 60
    p.setFont("Helvetica", 10)
    p.setFillColor(colors.grey)
    p.drawString(50, y, "Thank you for your purchase!")
    y -= 14
    p.drawString(50, y, "For support, contact support@shophub.com")

    p.showPage()
    p.save()

    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=f"invoice_{order.id}.pdf")


def home(request):
    """Landing page - Simple and clean"""
    categories = Category.objects.all()
    
    # Add random product image to each category if no category image
    for category in categories:
        if not category.image:
            random_product = category.products.filter(image__isnull=False).exclude(image='').first()
            if random_product:
                category.random_image = random_product.image
            else:
                category.random_image = None
    
    # cart_count = get_cart_count(request) if request.user.is_authenticated else 0
    context = {
        'page_title': 'Welcome to Our Store',
        'categories': categories,
        # 'cart_count': cart_count
    }
    return render(request, 'shop/home.html', context)


def user_register(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('product_list')
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        
        if form.is_valid():
            try:
                user = User.objects.create_user(
                    username=form.cleaned_data['username'],
                    email=form.cleaned_data['email'],
                    password=form.cleaned_data['password']
                )
                messages.success(request, 'Account created successfully! Please login.')
                return redirect('user_login')
            
            except Exception as e:
                messages.error(request, f'An error occurred: {str(e)}')
                # ❌ NO REDIRECT HERE
        
        # ❗ If form is invalid, Django keeps user data automatically
    else:
        form = RegisterForm()
    
    context = {
        'form': form,
        'page_title': 'Create Account'
    }
    return render(request, 'shop/register.html', context)

def user_login(request):
    """User login view with detailed error messages"""
    if request.user.is_authenticated:
        return redirect('product_list')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            # Step 1: Check if username exists
            if not User.objects.filter(username=username).exists():
                messages.error(request, 'Username does not exist.')
            else:
                # Step 2: Check password
                user = authenticate(request, username=username, password=password)
                
                if user is None:
                    messages.error(request, 'Incorrect password.')
                else:
                    # Step 3: Login success
                    login(request, user)
                    messages.success(request, f'Welcome back, {user.first_name or user.username}!')
                    next_url = request.GET.get('next', 'product_list')
                    return redirect(next_url)
        else:
            # Form validation errors (empty fields, etc.)
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
    else:
        form = LoginForm()
    
    context = {
        'form': form,
        'page_title': 'Login'
    }
    return render(request, 'shop/login.html', context)


def user_logout(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


def category_detail(request, slug):
    """View products by category - Protected view"""
    if not request.user.is_authenticated:
        messages.error(request, 'Please login to view products.')
        return redirect('user_login')   

    category = get_object_or_404(Category, slug=slug)
    products = category.products.all()
    categories = Category.objects.all()
    
    context = {
        'category': category,
        'products': products,
        'categories': categories,
        'page_title': f'{category.name} Products'
    }
    return render(request, 'shop/category_detail.html', context)


def search_products(request):
    """Search products - Protected view"""
    if not request.user.is_authenticated:
        messages.error(request, 'Please login to search products.')
        return redirect('user_login')

    
    query = request.GET.get('q', '').strip()
    products = []
    categories = Category.objects.all()
    
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
    
    # cart_count = get_cart_count(request)
    context = {
        'query': query,
        'products': products,
        'categories': categories,
        'page_title': f'Search Results for "{query}"' if query else 'Search',
        # 'cart_count': cart_count
    }
    return render(request, 'shop/search_results.html', context)

# Admin/Order Management Views

def admin_orders(request):
    """Admin panel to view and manage orders"""
    # Check if user is staff/admin
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('home')
    
    orders = Order.objects.all().order_by('-created_at')
    # cart_count = get_cart_count(request) if request.user.is_authenticated else 0
    
    context = {
        'orders': orders,
        'page_title': 'Order Management',
        # 'cart_count': cart_count
    }
    return render(request, 'shop/admin_orders.html', context)


@require_http_methods(["POST"])
def update_order_status(request, order_id):
    """Update order status"""
    if not request.user.is_staff:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    order = get_object_or_404(Order, id=order_id)
    new_status = request.POST.get('status', '').strip()
    
    if new_status not in dict(Order.ORDER_STATUS_CHOICES):
        return JsonResponse({'error': f'Invalid status: {new_status}'}, status=400)
    
    old_status = order.status
    order.status = new_status
    order.save()
    
    # Log the status change
    print(f"Order #{order_id} status changed from '{old_status}' to '{new_status}' by {request.user.username}")
    
    return JsonResponse({
        'success': True,
        'message': f'Order status updated to "{new_status}"',
        'order_id': order_id,
        'new_status': new_status,
        'status_display': order.get_status_display()
    })


# User Profile and Orders Views

@login_required(login_url='user_login')
def user_profile(request):
    """User profile page"""
    user = request.user
    user_orders_count = Order.objects.filter(user=user).count()
    # cart_count = get_cart_count(request)
    
    context = {
        'user': user,
        'user_orders_count': user_orders_count,
        'page_title': 'My Profile',
        # 'cart_count': cart_count
    }
    return render(request, 'shop/profile.html', context)


@login_required(login_url='user_login')
def my_orders(request):
    """User orders history page"""
    user = request.user
    orders = Order.objects.filter(user=user).order_by('-created_at')
    # cart_count = get_cart_count(request)
    
    context = {
        'orders': orders,
        'page_title': 'My Orders',
        # 'cart_count': cart_count
    }
    return render(request, 'shop/my_orders.html', context)