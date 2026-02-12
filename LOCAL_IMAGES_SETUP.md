# Django E-Commerce with Local Images - Setup Guide

## Overview
Your e-commerce website is now configured to use **local images only** from the `media/` folder. No external image URLs are used anywhere.

## Current Configuration

### ✅ Models Updated
- **Product Model**: Changed from `URLField` to `ImageField(upload_to='products/')`
- **Category Model**: Changed from `URLField` to `ImageField(upload_to='categories/')`

### ✅ Settings Configured
```python
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

### ✅ URLs Configured
Media files are served automatically in development:
```python
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

### ✅ Templates Updated
All templates now use:
```html
{% if product.image %}
    <img src="{{ product.image.url }}" alt="{{ product.name }}" loading="lazy">
{% else %}
    <img src="{% static 'images/no-image.svg' %}" alt="No Image" loading="lazy">
{% endif %}
```

**Key Features:**
- ✅ Uses `{{ product.image.url }}` for local images
- ✅ Fallback to `no-image.svg` for missing images
- ✅ `loading="lazy"` for performance optimization
- ✅ All external image URLs removed

## Folder Structure

```
project/
├── media/                          # ← Your local images go here
│   ├── products/                   # Product images
│   │   ├── mobiles/
│   │   │   ├── mobile1.jpg
│   │   │   ├── mobile2.jpg
│   │   │   └── ...
│   │   ├── laptops/
│   │   │   ├── laptop1.jpg
│   │   │   └── ...
│   │   ├── shoes/
│   │   ├── watches/
│   │   ├── headphones/
│   │   └── clothes/
│   └── categories/                 # Category images (optional)
│
├── shop/
│   ├── static/
│   │   └── images/
│   │       └── no-image.svg        # ← Fallback placeholder
│   ├── templates/
│   └── ...
│
└── ...
```

## How to Assign Images to Products

### Step 1: Prepare Your Images
Ensure your images are in the correct folder structure:
```
media/products/mobiles/
├── iphone.jpg
├── samsung.jpg
└── ...
```

### Step 2: Go to Admin Panel
1. Visit: `http://127.0.0.1:8000/admin/`
2. Login with your admin credentials
3. Go to **Shop > Products**

### Step 3: Upload Images
For each product:
1. Click the product name to edit
2. Scroll down to the **Image** field
3. Click **Choose File**
4. Select your image from `media/products/[category]/`
5. Click **Save**

### Step 4: Verify
Visit the front-end pages to see images:
- Home page: `http://127.0.0.1:8000/`
- Product list: `http://127.0.0.1:8000/products/`
- Category pages: `http://127.0.0.1:8000/category/mobiles/`

## Migration Info

A new migration was created:
```
shop/migrations/0003_alter_category_image_alter_product_image.py
```

This migration changed:
- `Category.image`: URLField → ImageField
- `Product.image`: URLField → ImageField

The migration has already been applied to your database.

## Image Upload Specifications

### Recommended Image Sizes
- **Product List & Category**: 300x300 to 500x500 pixels
- **Product Detail**: 500x500 to 800x800 pixels
- **Thumbnail**: 120x120 to 150x150 pixels

### Supported Formats
- JPEG (.jpg, .jpeg)
- PNG (.png)
- WebP (.webp)
- GIF (.gif)

### File Size Recommendations
- Max: 5-10 MB per image
- Recommended: 100-500 KB per image
- Use compression tools to optimize

## Django Admin Features

### Image Upload Features
- ✅ Click "Choose File" to upload from your computer
- ✅ Preview images in admin panel
- ✅ Clear image and re-upload anytime
- ✅ See uploaded path in admin

### View Uploaded Images
Path: `media/products/[image_filename]`

Example: If you uploaded `iphone.jpg` for iPhone 15 Pro Max:
- Stored at: `media/products/iphone.jpg`
- Served at: `http://127.0.0.1:8000/media/products/iphone.jpg`
- Used in template: `{{ product.image.url }}`

## Troubleshooting

### Images Not Appearing
1. Check if image file exists in `media/` folder
2. Verify file permissions (readable)
3. Check browser console for 404 errors
4. Ensure `MEDIA_URL` and `MEDIA_ROOT` are configured correctly

### 404 on Image
- Images must be uploaded via Django admin (not manually placed)
- Or manually place images in the correct folder structure
- Django will detect them automatically

### Fallback Image Shows
- This is normal if product has no image assigned
- Assign image via admin panel to fix

## Sample Products Status

The following 18 products have been created with **NO IMAGES**:

### Mobiles (3)
- iPhone 15 Pro Max
- Samsung Galaxy S24
- OnePlus 12

### Laptops (3)
- MacBook Pro 16" M3
- Dell XPS 15
- ASUS ROG Gaming Laptop

### Shoes (3)
- Nike Air Max 90
- Adidas Ultraboost 23
- Puma RS-X

### Watches (3)
- Apple Watch Series 9
- Samsung Galaxy Watch 6
- Fossil Smartwatch

### Headphones (3)
- Sony WH-1000XM5
- Apple AirPods Pro 2
- Bose QuietComfort 45

### Clothes (3)
- Premium Cotton T-Shirt
- Denim Jeans
- Winter Jacket

## Next Steps

1. **Prepare Images**: Organize images in `media/products/[category]/`
2. **Upload via Admin**: Go to admin and upload images for each product
3. **Test**: Visit pages to verify images display correctly
4. **Deploy**: When ready, use appropriate media serving in production

## Production Deployment Notes

### Important for Production
1. Use proper WSGI/ASGI server (not Django's runserver)
2. Configure proper static/media file serving:
   - Use WhiteNoise for static files
   - Use AWS S3 / Cloudinary for media files
   - Or configure nginx/Apache to serve media folder

3. Update settings:
```python
# In production settings
if not DEBUG:
    # Configure proper media serving
    # e.g., AWS S3, Cloudinary, etc.
    pass
```

## Admin Panel Image Management

### Best Practices
1. ✅ Always upload via admin (creates proper file structure)
2. ✅ Use clear, descriptive filenames
3. ✅ Keep image sizes reasonable (500KB max)
4. ✅ Use consistent image dimensions
5. ❌ Don't manually place files in media/ (use admin instead)

## File References

**Key Files Modified:**
- `shop/models.py` - Changed to ImageField
- `shopconfig/settings.py` - Already configured
- `shopconfig/urls.py` - Already configured
- `shop/templates/shop/*.html` - All updated
- `shop/management/commands/load_sample_data.py` - Simplified
- `shop/static/images/no-image.svg` - New fallback

## Testing Checklist

- [ ] Home page loads with fallback images
- [ ] Product list displays no-image placeholders
- [ ] Product detail page shows image
- [ ] Category pages work
- [ ] Search results display
- [ ] Cart shows product images
- [ ] Admin panel shows image upload field
- [ ] Can upload image and see it on front-end
- [ ] Fallback image appears for products without images

## Performance Optimization

### Already Implemented
- ✅ `loading="lazy"` on all images (deferred loading)
- ✅ Local images (no external requests)
- ✅ Image caching via Django
- ✅ Proper MIME types

### Optional Enhancements
- Add image compression middleware
- Use image optimization library (PIL)
- Implement CDN for media files
- Add image versioning

## Need Help?

Check these files for image implementation details:
- Templates: `shop/templates/shop/home.html`
- Models: `shop/models.py`
- Admin: `shop/admin.py`
- Settings: `shopconfig/settings.py`
- Fallback image: `shop/static/images/no-image.svg`

---

**Status**: ✅ All external image URLs removed. System is 100% offline for images.
