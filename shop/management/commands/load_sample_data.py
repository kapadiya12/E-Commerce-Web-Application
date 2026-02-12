from django.core.management.base import BaseCommand
from shop.models import Category, Product

class Command(BaseCommand):
    help = 'Load sample products without images into the database. You will manually assign local images via admin.'

    def handle(self, *args, **options):
        self.stdout.write("Loading categories...")
        
        # Create categories
        categories_data = [
            {'name': 'Mobiles', 'slug': 'mobiles'},
            {'name': 'Laptops', 'slug': 'laptops'},
            {'name': 'Shoes', 'slug': 'shoes'},
            {'name': 'Watches', 'slug': 'watches'},
            {'name': 'Headphones', 'slug': 'headphones'},
            {'name': 'Clothes', 'slug': 'clothes'},
        ]
        
        categories = {}
        for cat_data in categories_data:
            cat, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults={'name': cat_data['name']}
            )
            categories[cat_data['slug']] = cat
            if created:
                self.stdout.write(f"✓ Created category: {cat.name}")
        
        self.stdout.write("\nLoading products...")
        
        # Products data WITHOUT image URLs (will be assigned manually from media folder)
        products_data = [
            # Mobiles
            {
                'name': 'iPhone 15 Pro Max',
                'description': 'Latest Apple flagship with A17 Pro chip, advanced camera system, and all-day battery',
                'price': 99999.00,
                'stock': 15,
                'category': 'mobiles',
            },
            {
                'name': 'Samsung Galaxy S24',
                'description': 'Powerful Android phone with stunning AMOLED display and 5G connectivity',
                'price': 79999.00,
                'stock': 20,
                'category': 'mobiles',
            },
            {
                'name': 'OnePlus 12',
                'description': 'Fast and smooth performance with 120Hz display and rapid charging',
                'price': 49999.00,
                'stock': 25,
                'category': 'mobiles',
            },
            
            # Laptops
            {
                'name': 'MacBook Pro 16" M3',
                'description': 'Powerful laptop for professionals with stunning Retina display',
                'price': 199999.00,
                'stock': 8,
                'category': 'laptops',
            },
            {
                'name': 'Dell XPS 15',
                'description': 'Sleek and powerful Windows laptop with InfinityEdge display',
                'price': 149999.00,
                'stock': 10,
                'category': 'laptops',
            },
            {
                'name': 'ASUS ROG Gaming Laptop',
                'description': 'High-performance gaming laptop with RTX 4090 graphics',
                'price': 249999.00,
                'stock': 6,
                'category': 'laptops',
            },
            
            # Shoes
            {
                'name': 'Nike Air Max 90',
                'description': 'Classic and comfortable sneakers with iconic design',
                'price': 9999.00,
                'stock': 50,
                'category': 'shoes',
            },
            {
                'name': 'Adidas Ultraboost 23',
                'description': 'Premium running shoes with boost technology for comfort',
                'price': 12999.00,
                'stock': 40,
                'category': 'shoes',
            },
            {
                'name': 'Puma RS-X',
                'description': 'Retro-inspired casual shoes with modern comfort',
                'price': 7999.00,
                'stock': 45,
                'category': 'shoes',
            },
            
            # Watches
            {
                'name': 'Apple Watch Series 9',
                'description': 'Smart watch with fitness tracking and health monitoring',
                'price': 39999.00,
                'stock': 20,
                'category': 'watches',
            },
            {
                'name': 'Samsung Galaxy Watch 6',
                'description': 'Stylish watch with AMOLED display and Samsung Wear OS',
                'price': 29999.00,
                'stock': 25,
                'category': 'watches',
            },
            {
                'name': 'Fossil Smartwatch',
                'description': 'Classic design meets modern smartwatch technology',
                'price': 19999.00,
                'stock': 30,
                'category': 'watches',
            },
            
            # Headphones
            {
                'name': 'Sony WH-1000XM5',
                'description': 'Premium noise-canceling wireless headphones with excellent sound',
                'price': 29999.00,
                'stock': 15,
                'category': 'headphones',
            },
            {
                'name': 'Apple AirPods Pro 2',
                'description': 'Wireless earbuds with active noise cancellation and spatial audio',
                'price': 24999.00,
                'stock': 20,
                'category': 'headphones',
            },
            {
                'name': 'Bose QuietComfort 45',
                'description': 'Comfortable headphones with excellent noise cancellation',
                'price': 19999.00,
                'stock': 18,
                'category': 'headphones',
            },
            
            # Clothes
            {
                'name': 'Premium Cotton T-Shirt',
                'description': 'High-quality 100% cotton t-shirt, comfortable and durable',
                'price': 999.00,
                'stock': 100,
                'category': 'clothes',
            },
            {
                'name': 'Denim Jeans',
                'description': 'Classic blue denim jeans with perfect fit',
                'price': 2499.00,
                'stock': 80,
                'category': 'clothes',
            },
            {
                'name': 'Winter Jacket',
                'description': 'Warm and stylish winter jacket for cold weather',
                'price': 5999.00,
                'stock': 40,
                'category': 'clothes',
            },
        ]
        
        # Create products
        for product_data in products_data:
            category = categories[product_data.pop('category')]
            product, created = Product.objects.get_or_create(
                name=product_data['name'],
                defaults={**product_data, 'category': category}
            )
            if created:
                self.stdout.write(f"✓ Created product: {product.name}")
        
        self.stdout.write("\n✓ Sample data loaded successfully!")
        self.stdout.write("\n" + "="*60)
        self.stdout.write("NEXT STEPS: Assign Images to Products")
        self.stdout.write("="*60)
        self.stdout.write("\n1. Go to admin: http://127.0.0.1:8000/admin/shop/product/")
        self.stdout.write("2. Click on each product to edit")
        self.stdout.write("3. In the 'Image' field, upload images from your media/ folder")
        self.stdout.write("4. Images should be placed in: media/products/")
        self.stdout.write("5. For each category (mobiles/, laptops/, shoes/, etc.)")
        self.stdout.write("="*60)
