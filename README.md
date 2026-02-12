# 🛍️ ShopCart - Shopping Cart MVP

A complete, production-ready Shopping Cart MVP built with Django. Features a modern UI, full validation, and all essential e-commerce functionality.

## ✨ Features

### 1. **Product Display**
- Browse all products with images, names, and prices
- Stock status indication
- Responsive product grid layout
- Product detail page with full information

### 2. **Shopping Cart**
- Add products to cart with quantity selection
- View cart with all items and subtotals
- Update item quantities
- Remove items from cart
- Real-time cart item count in navigation
- Session-based cart (persists across pages)

### 3. **Checkout**
- Simple yet comprehensive checkout form
- Customer information collection (name, email, phone)
- Shipping address form
- Support for Cash on Delivery (COD) payment
- Order creation with automatic stock reduction

### 4. **Order Management**
- Order confirmation page with details
- Order history in database
- Order status tracking
- Complete order information preserved

### 5. **Validation**
- **Server-side validation**: Django forms with comprehensive validation rules
- **Client-side validation**: Real-time form validation with error messages
- Stock validation before adding to cart
- Email validation
- Phone number validation
- Alphanumeric field validations

### 6. **Admin Interface**
- Manage products (CRUD operations)
- View and manage orders
- Monitor cart contents
- Full Django admin features

## 🚀 Project Structure

```
shopconfig/
├── shopconfig/          # Project settings
│   ├── settings.py      # Django configuration
│   ├── urls.py          # Main URL routing
│   └── wsgi.py
├── shop/                # Main app
│   ├── models.py        # Database models (Product, Cart, Order, etc.)
│   ├── views.py         # View logic for all pages
│   ├── forms.py         # Form validation
│   ├── admin.py         # Admin interface configuration
│   ├── urls.py          # App URL routing
│   ├── templates/shop/  # HTML templates
│   │   ├── base.html    # Base template
│   │   ├── product_list.html
│   │   ├── product_detail.html
│   │   ├── cart.html
│   │   ├── checkout.html
│   │   └── order_confirmation.html
│   └── management/commands/
│       ├── add_sample_products.py
│       └── create_admin.py
├── media/               # User uploaded files
├── manage.py
└── db.sqlite3          # Database file
```

## 📦 Database Models

### Product
- name: CharField (unique)
- description: TextField
- price: DecimalField (with min value validation)
- stock: IntegerField (with min value validation)
- image: ImageField (optional)
- created_at, updated_at: DateTimeField

### Cart
- session_key: CharField (unique)
- created_at, updated_at: DateTimeField
- Methods: get_total(), get_item_count()

### CartItem
- cart: ForeignKey(Cart)
- product: ForeignKey(Product)
- quantity: PositiveIntegerField
- added_at: DateTimeField
- Methods: get_subtotal()

### Order
- first_name, last_name: CharField
- email: EmailField
- phone: CharField
- address: CharField
- city, state: CharField
- postal_code: CharField
- total_amount: DecimalField
- payment_method: CharField (choices)
- status: CharField (choices)
- created_at, updated_at: DateTimeField

### OrderItem
- order: ForeignKey(Order)
- product: ForeignKey(Product)
- quantity: PositiveIntegerField
- price: DecimalField
- Methods: get_subtotal()

## 🔧 Installation & Setup

### Prerequisites
- Python 3.8+
- pip package manager

### 1. Install Dependencies
```bash
pip install django pillow
```

### 2. Navigate to Project Directory
```bash
cd "D:\New folder (3)"
```

### 3. Create Database & Admin User
```bash
# Already done, but to redo:
python manage.py migrate
python manage.py create_admin
```

### 4. Add Sample Products
```bash
python manage.py add_sample_products
```

### 5. Run Development Server
```bash
python manage.py runserver
```

The server will start at `http://127.0.0.1:8000/`

## 🌐 URL Routing

| URL | View | Purpose |
|-----|------|---------|
| `/` | product_list | Browse all products |
| `/product/<id>/` | product_detail | View product details |
| `/cart/` | view_cart | View shopping cart |
| `/cart/add/<id>/` | add_to_cart | Add product to cart (POST) |
| `/cart/update/<item_id>/` | update_cart_item | Update quantity (POST) |
| `/cart/remove/<item_id>/` | remove_from_cart | Remove from cart (POST) |
| `/checkout/` | checkout | Checkout form |
| `/order/confirmation/<id>/` | order_confirmation | Order confirmation |
| `/admin/` | Django Admin | Manage products & orders |

## 👤 Default Admin Credentials

- **Username**: admin
- **Password**: admin123
- **URL**: http://127.0.0.1:8000/admin/

## 📋 Validation Details

### Add to Cart Form
- Quantity: 1-100 range
- Stock availability check
- Product existence validation

### Update Cart Form
- Quantity: 1-100 range
- Stock availability check
- Cart ownership verification

### Checkout Form
- **First Name**: Required, letters only
- **Last Name**: Required, letters only
- **Email**: Valid email format
- **Phone**: 9-15 digits
- **Address**: Required, max 255 chars
- **City**: Required, max 50 chars
- **State**: Required, max 50 chars
- **Postal Code**: Alphanumeric only
- **Payment Method**: COD selected

All validations are performed both client-side (JavaScript) and server-side (Django forms).

## 🎨 Frontend Features

- **Responsive Design**: Mobile-friendly Bootstrap 5 layout
- **Modern Styling**: Gradient colors, smooth transitions
- **Error Messages**: Clear, user-friendly error notifications
- **Loading States**: Feedback for user actions
- **Accessibility**: Semantic HTML, proper form labels

## 💾 Sample Products

The system comes with 10 pre-loaded products:
1. Wireless Headphones - ₹2,999.99
2. USB-C Charging Cable - ₹499.99
3. Portable Power Bank - ₹1,499.99
4. Mechanical Keyboard - ₹3,499.99
5. Ergonomic Mouse - ₹799.99
6. Webcam HD - ₹1,999.99
7. Desk Lamp LED - ₹899.99
8. Laptop Stand - ₹1,299.99
9. Cable Organizer Kit - ₹349.99
10. USB Hub 4-Port - ₹599.99

## 🔐 Security Features

- CSRF protection on all forms
- Session-based authentication
- Input validation and sanitization
- SQL injection prevention (ORM)
- XSS protection in templates

## 📊 Key Implementation Details

### Session-Based Cart
- Uses Django sessions to maintain cart across page visits
- Automatic cart creation when needed
- Cart persists for logged-out users

### Stock Management
- Real-time stock availability check
- Automatic stock reduction on order placement
- Prevents overselling

### Order Processing
- Atomic transaction handling
- Automatic cart clearing after order
- Comprehensive order data preservation

### Error Handling
- User-friendly error messages
- Form validation feedback
- Graceful error pages

## 🚀 Future Enhancements (Optional)

1. **User Authentication**
   - User registration and login
   - Order history per user
   - Saved addresses

2. **Advanced Features**
   - Product categories
   - Search and filtering
   - Product reviews and ratings
   - Discount codes

3. **Payment Integration**
   - Razorpay integration
   - Multiple payment methods
   - Digital receipts via email

4. **Analytics**
   - Sales dashboard
   - Product performance metrics
   - User behavior tracking

## 🐛 Troubleshooting

### Port 8000 Already in Use
```bash
python manage.py runserver 8001
```

### Database Issues
```bash
python manage.py migrate
python manage.py migrate shop
```

### Missing Media Files
The media directory is automatically created. Ensure it exists at:
`D:\New folder (3)\media\`

## 📝 Testing the Application

1. **Add Products to Cart**
   - Visit product list
   - Click "View Details"
   - Enter quantity and click "Add to Cart"

2. **Update Cart**
   - Go to cart page
   - Change quantities and click Update
   - Remove items as needed

3. **Complete Purchase**
   - Click "Proceed to Checkout"
   - Fill all required fields
   - Submit order
   - View confirmation

4. **Admin Panel**
   - Visit http://127.0.0.1:8000/admin/
   - Login with admin/admin123
   - View products and orders

## 📄 File Descriptions

- **models.py**: Database schema and business logic
- **views.py**: View functions for all pages
- **forms.py**: Form classes with validation rules
- **admin.py**: Admin interface configuration
- **urls.py**: URL routing
- **templates/**: HTML templates with Bootstrap styling
- **management/commands/**: Custom Django management commands

## ⚡ Performance Notes

- Optimized database queries
- Efficient cart calculations
- Minimal template rendering
- Static file compression ready

## 📞 Support

For issues or improvements, check:
1. Django logs in terminal
2. Browser console for JavaScript errors
3. Django admin for data verification

---

**Created**: January 22, 2026  
**Technology**: Django 5.0.1, Bootstrap 5, SQLite  
**Status**: Production Ready MVP ✓
