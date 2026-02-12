from django.core.management.base import BaseCommand
from shop.models import Product
from decimal import Decimal


class Command(BaseCommand):
    help = 'Add sample products to the database'
    
    def handle(self, *args, **options):
        # Sample products
        products_data = [
            {
                'name': 'Wireless Headphones',
                'description': 'High-quality wireless headphones with noise cancellation. Perfect for music lovers and professionals.',
                'price': Decimal('2999.99'),
                'stock': 50
            },
            {
                'name': 'USB-C Charging Cable',
                'description': 'Durable USB-C charging cable with fast charging capability. Compatible with most devices.',
                'price': Decimal('499.99'),
                'stock': 200
            },
            {
                'name': 'Portable Power Bank',
                'description': '20000mAh portable power bank with fast charging. Keep your devices charged on the go.',
                'price': Decimal('1499.99'),
                'stock': 75
            },
            {
                'name': 'Mechanical Keyboard',
                'description': 'Professional mechanical keyboard with customizable RGB lighting. Great for gaming and typing.',
                'price': Decimal('3499.99'),
                'stock': 30
            },
            {
                'name': 'Ergonomic Mouse',
                'description': 'Wireless ergonomic mouse with precision tracking. Comfortable for long work sessions.',
                'price': Decimal('799.99'),
                'stock': 100
            },
            {
                'name': 'Webcam HD',
                'description': '1080p HD webcam with auto-focus. Ideal for video calls and streaming.',
                'price': Decimal('1999.99'),
                'stock': 45
            },
            {
                'name': 'Desk Lamp LED',
                'description': 'Energy-efficient LED desk lamp with adjustable brightness. Perfect for your workspace.',
                'price': Decimal('899.99'),
                'stock': 60
            },
            {
                'name': 'Laptop Stand',
                'description': 'Adjustable aluminum laptop stand. Improves posture and saves desk space.',
                'price': Decimal('1299.99'),
                'stock': 80
            },
            {
                'name': 'Cable Organizer Kit',
                'description': 'Complete cable management kit to organize your workspace. Includes various sizes.',
                'price': Decimal('349.99'),
                'stock': 150
            },
            {
                'name': 'USB Hub 4-Port',
                'description': '4-port USB 3.0 hub with fast data transfer. Expand your device connectivity.',
                'price': Decimal('599.99'),
                'stock': 120
            },
        ]
        
        # Create or update products
        created_count = 0
        updated_count = 0
        
        for product_data in products_data:
            product, created = Product.objects.get_or_create(
                name=product_data['name'],
                defaults=product_data
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created product: {product.name}')
                )
            else:
                # Update existing product
                for key, value in product_data.items():
                    setattr(product, key, value)
                product.save()
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(f'Updated product: {product.name}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\nSuccessfully created {created_count} products and updated {updated_count} products.'
            )
        )
