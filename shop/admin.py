from django.contrib import admin
from .models import Category, Product, Cart, CartItem, Order, OrderItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'slug')
    readonly_fields = ('created_at', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    
    fieldsets = (
        ('Category Information', {
            'fields': ('name', 'slug', 'description', 'image')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'is_in_stock', 'created_at')
    list_filter = ('category', 'created_at', 'price')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Product Information', {
            'fields': ('name', 'description', 'category', 'price', 'stock', 'image')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'session_key', 'get_item_count', 'get_total', 'created_at')
    readonly_fields = ('session_key', 'created_at', 'updated_at')
    
    def get_item_count(self, obj):
        return obj.get_item_count()
    get_item_count.short_description = 'Items'
    
    def get_total(self, obj):
        return f"₹{obj.get_total()}"
    get_total.short_description = 'Total'


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart', 'product', 'quantity', 'get_subtotal')
    readonly_fields = ('added_at',)
    
    def get_subtotal(self, obj):
        return f"₹{obj.get_subtotal()}"
    get_subtotal.short_description = 'Subtotal'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',          # ✅ SHOW USER COLUMN
        'first_name',
        'last_name',
        'email',
        'total_amount',
        'payment_method',
        'status',
        'created_at'
    )

    list_filter = ('status', 'payment_method', 'created_at')

    search_fields = (
        'first_name',
        'last_name',
        'email',
        'phone',
        'user__username',   # ✅ SEARCH BY USERNAME
        'user__email'
    )

    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('User Account', {   # ✅ NEW SECTION
            'fields': ('user',)
        }),
        ('Customer Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone')
        }),
        ('Shipping Address', {
            'fields': ('address', 'city', 'state', 'postal_code')
        }),
        ('Order Details', {
            'fields': ('total_amount', 'payment_method', 'status')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )




@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'get_user',        # ✅ SHOW USER
        'order',
        'product',
        'quantity',
        'price',
        'get_subtotal'
    )

    readonly_fields = ('price',)

    search_fields = (
        'order__user__username',
        'order__user__email',
        'product__name',
    )

    list_filter = (
        'order__status',
    )

    def get_subtotal(self, obj):
        return f"₹{obj.get_subtotal()}"
    get_subtotal.short_description = 'Subtotal'

    def get_user(self, obj):
        if obj.order.user:
            return obj.order.user.username
        return "Guest"
    get_user.short_description = 'User'
