import os
import random
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from shop.models import Product


class Command(BaseCommand):
    help = 'Assign random images to products based on their category'
    
    def handle(self, *args, **options):
        # Map category names to image folders
        category_images = {
            'mobiles': [
                'aaditya-ailawadhi-D6pgxi3gwNQ-unsplash.jpg',
                'arpad-czapp-Cg94g0QFHv4-unsplash.jpg',
                'd-c-tr-nh-1t1CBECuqvs-unsplash.jpg',
                'jakob-owens-fecW3iL4Uxo-unsplash.jpg',
                'martin-engel-crblx-CmCns-unsplash.jpg',
                'rishabh-malhotra-83ypHTv6J2M-unsplash.jpg',
                'v-a-tao-OxvlDO8RwKg-unsplash.jpg',
            ],
            'laptops': [
                'alex-knight-j4uuKnN43_M-unsplash.jpg',
                'c-d-x-PDX_a_82obo-unsplash.jpg',
                'christopher-gower-m_HRfLhgABo-unsplash.jpg',
                'howard-bouchevereau-RSCirJ70NDM-unsplash.jpg',
                'kari-shea-1SAnrIxw5OY-unsplash (1).jpg',
                'kari-shea-1SAnrIxw5OY-unsplash.jpg',
                'maxim-hopman-Hin-rzhOdWs-unsplash.jpg',
            ],
            'shoes': [
                'artem-bondarchuk-XPBYi4K8vFI-unsplash.jpg',
                'jeff-tumale-SD9Jyl1xNQ4-unsplash.jpg',
                'linda-xu-fUEP0djb1hA-unsplash.jpg',
                'maksim-larin-1vy2QcZd5FU-unsplash.jpg',
                'ryan-plomp-jvoZ-Aux9aw-unsplash.jpg',
                'ryan-plomp-PGTO_A0eLt4-unsplash.jpg',
                'xavier-teo-SxAXphIPWeg-unsplash.jpg',
            ],
            'watches': [
                'hunters-race-dE0sBTZCVoY-unsplash.jpg',
                'mambawatches-ukJdqKqFcDA-unsplash.jpg',
                'paul-cuoco-CO2vOhPqlrM-unsplash.jpg',
                'puru-raj-B6z8FAfi7zY-unsplash.jpg',
                'ryan-waring-p2WUEFGrAdA-unsplash.jpg',
                'tadeusz-lakota-Tb38UzCvKCY-unsplash.jpg',
                'vvs--KRN2kU9e1s-unsplash.jpg',
                'yash-parashar-LWPPpkn6NEQ-unsplash.jpg',
            ],
            'headphones': [
                'akhil-yerabati-Q2uV5TkjNz8-unsplash.jpg',
                'kiran-ck-LSNJ-pltdu8-unsplash.jpg',
                'lee-campbell-GI6L2pkiZgQ-unsplash.jpg',
                'luke-peterson-lUMj2Zv5HUE-unsplash.jpg',
                'sam-grozyan-yDC3NXxrtyc-unsplash.jpg',
                'tomasz-gawlowski-YDZPdqv3FcA-unsplash.jpg',
            ],
            'clothes': [
                'bao-bao-GREEBEtyR9Y-unsplash.jpg',
                'cristofer-maximilian-AqLIkOzWDAk-unsplash.jpg',
                'faith-yarn-Wr0TpKqf26s-unsplash.jpg',
                'geoffroy-danest-0fG6zACWGJY-unsplash.jpg',
                'marlon-alves-A0mSSCEVh9A-unsplash.jpg',
                'mediamodifier-7cERndkOyDw-unsplash.jpg',
                'tobias-tullius-Fg15LdqpWrs-unsplash.jpg',
            ],
        }
        
        media_root = 'media/products'
        total_assigned = 0
        
        # Get all products
        products = Product.objects.all()
        
        print("\n" + "="*60)
        print("ASSIGNING IMAGES TO PRODUCTS")
        print("="*60 + "\n")
        
        for product in products:
            # Get category name
            category_name = product.category.name.lower()
            
            # Skip if no images for this category
            if category_name not in category_images:
                print(f"❌ No images found for category: {category_name}")
                continue
            
            # Get random image from category
            image_list = category_images[category_name]
            random_image = random.choice(image_list)
            
            # Build path to image
            image_path = os.path.join(media_root, category_name, random_image)
            
            try:
                # Read image file
                with open(image_path, 'rb') as f:
                    image_content = f.read()
                
                # Assign to product
                product.image.save(random_image, ContentFile(image_content), save=True)
                
                print(f"✅ {product.name:40} → {random_image[:45]}")
                total_assigned += 1
                
            except FileNotFoundError:
                print(f"⚠️  File not found: {image_path}")
            except Exception as e:
                print(f"❌ Error assigning image to {product.name}: {str(e)}")
        
        print("\n" + "="*60)
        print(f"✅ Successfully assigned {total_assigned} images!")
        print("="*60 + "\n")
        self.stdout.write(
            self.style.SUCCESS(
                f'Images assigned successfully! Total: {total_assigned}'
            )
        )
