from django.core.management.base import BaseCommand
from shop.models import Order


class Command(BaseCommand):
    help = 'Update order status'

    def add_arguments(self, parser):
        parser.add_argument('order_id', type=int, help='Order ID')
        parser.add_argument('status', type=str, help='New status (pending, confirmed, shipped, delivered, cancelled)')

    def handle(self, *args, **options):
        order_id = options['order_id']
        new_status = options['status']
        
        try:
            order = Order.objects.get(id=order_id)
            
            if new_status not in dict(Order.ORDER_STATUS_CHOICES):
                self.stdout.write(
                    self.style.ERROR(f'Invalid status. Choose from: {", ".join([s[0] for s in Order.ORDER_STATUS_CHOICES])}')
                )
                return
            
            order.status = new_status
            order.save()
            
            self.stdout.write(
                self.style.SUCCESS(f'Order #{order_id} status updated to "{new_status}"')
            )
        except Order.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'Order #{order_id} not found')
            )
