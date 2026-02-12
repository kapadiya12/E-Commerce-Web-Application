from django.urls import path
from . import views

urlpatterns = [
    # Home & Landing
    path('', views.home, name='home'),
    
    # Authentication URLs
    path('login/', views.user_login, name='user_login'),
    path('register/', views.user_register, name='user_register'),
    path('logout/', views.user_logout, name='user_logout'),
    
    # Product URLs
    path('products/', views.product_list, name='product_list'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    
    # Category URLs
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    
    # Search
    path('search/', views.search_products, name='search_products'),
    
    # Cart URLs
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/add/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    
    # Checkout URLs
    path('checkout/', views.checkout, name='checkout'),
    path('order/confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('order/<int:order_id>/invoice/download/', views.download_invoice, name='download_invoice'),
    
    # Admin URLs
    path('admin-orders/', views.admin_orders, name='admin_orders'),
    path('admin/order/<int:order_id>/update-status/', views.update_order_status, name='update_order_status'),
    
    # User Profile & Orders
    path('accounts/profile/', views.user_profile, name='user_profile'),
    path('orders/my-orders/', views.my_orders, name='my_orders'),
]
