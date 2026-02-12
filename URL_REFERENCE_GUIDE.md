# 🔗 Complete URL Reference Guide

## Base URL
```
http://127.0.0.1:8000/
```

---

## 📍 Main Pages

### Home
```
http://127.0.0.1:8000/
URL Name: home
Features: Hero banner, featured products, all categories
```

### All Products
```
http://127.0.0.1:8000/products/
URL Name: product_list
Features: Grid layout, sidebar category filter
```

---

## 🔍 Search

### Search Results
```
http://127.0.0.1:8000/search/?q=iphone
URL Name: search_products
Query Parameter: q (search term)
Examples:
  - ?q=iphone
  - ?q=laptop
  - ?q=shoe
  - ?q=watch
  - ?q=headphone
  - ?q=shirt
```

---

## 📂 Categories

### Mobiles
```
http://127.0.0.1:8000/category/mobiles/
Products: iPhone, Samsung, OnePlus
```

### Laptops
```
http://127.0.0.1:8000/category/laptops/
Products: MacBook, Dell, ASUS
```

### Shoes
```
http://127.0.0.1:8000/category/shoes/
Products: Nike, Adidas, Puma
```

### Watches
```
http://127.0.0.1:8000/category/watches/
Products: Apple, Samsung, Fossil
```

### Headphones
```
http://127.0.0.1:8000/category/headphones/
Products: Sony, Apple AirPods, Bose
```

### Clothes
```
http://127.0.0.1:8000/category/clothes/
Products: T-Shirt, Jeans, Winter Jacket
```

---

## 🛍️ Product Operations

### View Product Details
```
http://127.0.0.1:8000/product/1/
http://127.0.0.1:8000/product/2/
... and so on
URL Name: product_detail
Parameter: pk (product ID)
```

### Add to Cart (POST)
```
http://127.0.0.1:8000/cart/add/1/
URL Name: add_to_cart
Method: POST
Parameter: pk (product ID)
```

### View Cart
```
http://127.0.0.1:8000/cart/
URL Name: view_cart
```

### Update Cart Item Quantity (POST)
```
http://127.0.0.1:8000/cart/update/1/
URL Name: update_cart_item
Method: POST
Parameter: item_id (cart item ID)
```

### Remove from Cart (POST)
```
http://127.0.0.1:8000/cart/remove/1/
URL Name: remove_from_cart
Method: POST
Parameter: item_id (cart item ID)
```

---

## 🛒 Checkout

### Checkout Page
```
http://127.0.0.1:8000/checkout/
URL Name: checkout
GET: Display form
POST: Submit order
```

### Order Confirmation
```
http://127.0.0.1:8000/order/confirmation/1/
URL Name: order_confirmation
Parameter: order_id (order ID)
```

---

## 👤 Authentication

### Login
```
http://127.0.0.1:8000/login/
URL Name: login
```

### Sign Up
```
http://127.0.0.1:8000/signup/
URL Name: signup
```

### Logout
```
http://127.0.0.1:8000/logout/
URL Name: logout
```

---

## 🔧 Admin Panel

### Django Admin
```
http://127.0.0.1:8000/admin/
Credentials:
  Username: admin
  Password: admin123
```

---

## 📋 Complete URL Routing Table

| URL | Name | Method | Description |
|-----|------|--------|-------------|
| `/` | home | GET | Home page |
| `/products/` | product_list | GET | All products |
| `/product/<id>/` | product_detail | GET | Product details |
| `/category/<slug>/` | category_detail | GET | Category products |
| `/search/` | search_products | GET | Search results |
| `/cart/add/<id>/` | add_to_cart | POST | Add to cart |
| `/cart/` | view_cart | GET | View cart |
| `/cart/update/<id>/` | update_cart_item | POST | Update quantity |
| `/cart/remove/<id>/` | remove_from_cart | POST | Remove item |
| `/checkout/` | checkout | GET/POST | Checkout form |
| `/order/confirmation/<id>/` | order_confirmation | GET | Order confirmation |
| `/login/` | login | GET/POST | Login page |
| `/signup/` | signup | GET/POST | Sign up page |
| `/logout/` | logout | GET | Logout |
| `/admin/` | admin | GET/POST | Admin panel |

---

## 🧪 Sample Test URLs

### Browse & Shop
```
1. http://127.0.0.1:8000/
   ↓ Click "Start Shopping"
2. http://127.0.0.1:8000/products/
   ↓ Click product
3. http://127.0.0.1:8000/product/1/
   ↓ Click "Add to Cart"
4. http://127.0.0.1:8000/cart/
   ↓ Click "Checkout"
5. http://127.0.0.1:8000/checkout/
   ↓ Fill & Submit
6. http://127.0.0.1:8000/order/confirmation/1/
```

### Search & Category
```
1. http://127.0.0.1:8000/search/?q=iphone
   ↓ See results
2. http://127.0.0.1:8000/category/mobiles/
   ↓ View category products
3. http://127.0.0.1:8000/category/laptops/
   ↓ Switch category
```

### Authentication
```
1. http://127.0.0.1:8000/signup/
   ↓ Create account
2. http://127.0.0.1:8000/login/
   ↓ Login with credentials
3. http://127.0.0.1:8000/logout/
   ↓ Logout
```

---

## 📱 Mobile URLs

All URLs work perfectly on mobile:
- Responsive design
- Touch-friendly buttons
- Mobile-optimized images
- Readable text sizes

Test on iPhone/Android:
- Same URLs work
- Optimized layout
- Fast performance

---

## 🔐 Admin URLs

### Models Accessible
```
/admin/shop/product/               - Products
/admin/shop/category/              - Categories
/admin/shop/cart/                  - Shopping carts
/admin/shop/cartitem/              - Cart items
/admin/shop/order/                 - Orders
/admin/shop/orderitem/             - Order items
/admin/auth/user/                  - Users
```

### Admin Actions
- Add products
- Edit products
- Delete products
- View orders
- Manage users
- View categories
- View carts

---

## 📊 Query Parameters

### Search
```
?q=search_term
Examples:
  /search/?q=iphone
  /search/?q=laptop
  /search/?q=shoe
```

### Pagination (Ready to add)
```
?page=2
/products/?page=2
/category/mobiles/?page=2
```

### Filters (Ready to add)
```
?price_min=1000&price_max=50000
?in_stock=true
?rating=4.5
```

---

## 🔗 Template Tag URLs

### Django URL Tag
```django
{% url 'home' %}
{% url 'product_list' %}
{% url 'product_detail' pk=product.id %}
{% url 'category_detail' slug=category.slug %}
{% url 'search_products' %}
{% url 'view_cart' %}
{% url 'checkout' %}
{% url 'login' %}
{% url 'signup' %}
{% url 'logout' %}
```

---

## ✅ Quick Reference

### Get Product by ID
```
ID 1: iPhone 15 Pro Max - /product/1/
ID 2: Samsung Galaxy S24 - /product/2/
ID 3: OnePlus 12 - /product/3/
... up to ID 18
```

### Browse by Category
```
Mobiles:     /category/mobiles/
Laptops:     /category/laptops/
Shoes:       /category/shoes/
Watches:     /category/watches/
Headphones:  /category/headphones/
Clothes:     /category/clothes/
```

### Perform Actions
```
Search:      /search/?q=iphone
Add to cart: /cart/add/1/      (POST)
View cart:   /cart/
Checkout:    /checkout/
Login:       /login/
Sign up:     /signup/
Logout:      /logout/
Admin:       /admin/
```

---

## 🎯 Most Used URLs

1. **http://127.0.0.1:8000/** - Home page
2. **http://127.0.0.1:8000/products/** - All products
3. **http://127.0.0.1:8000/cart/** - Shopping cart
4. **http://127.0.0.1:8000/search/?q=** - Search products
5. **http://127.0.0.1:8000/category/mobiles/** - Popular category
6. **http://127.0.0.1:8000/checkout/** - Checkout
7. **http://127.0.0.1:8000/admin/** - Admin panel

---

**Last Updated**: January 22, 2026  
**Status**: ✅ All URLs Working  
**Total URLs**: 12+ main + admin URLs
