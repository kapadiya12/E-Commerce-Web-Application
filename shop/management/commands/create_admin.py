from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Create a superuser account'
    
    def handle(self, *args, **options):
        # Delete existing admin user if it exists
        User.objects.filter(username='admin').delete()
        
        # Create new superuser
        User.objects.create_superuser(
            username='admin',
            email='admin@shop.com',
            password='admin123'
        )
        
        self.stdout.write(
            self.style.SUCCESS(
                'Superuser created successfully!\nUsername: admin\nPassword: admin123'
            )
        )
