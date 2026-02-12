# Quick Image Upload Guide

## 🚀 Fast Track: Upload Images in 3 Steps

### Step 1: Open Admin Panel
```
http://127.0.0.1:8000/admin/shop/product/
```

### Step 2: Click a Product
Click on any product name (e.g., "iPhone 15 Pro Max")

### Step 3: Upload Image
1. Scroll down to **Image** field
2. Click **Choose File**
3. Select your image from computer
4. Click **Save**

## ✅ Done!
Image will now appear on all pages:
- Home page
- Product listing
- Product detail
- Category pages
- Search results
- Shopping cart

---

## 📁 Your Image Folder Structure

Create this structure if not exists:
```
media/
├── products/
│   ├── mobiles/
│   │   ├── iphone15.jpg
│   │   ├── samsung_s24.jpg
│   │   └── oneplus12.jpg
│   ├── laptops/
│   │   ├── macbook_pro.jpg
│   │   ├── dell_xps.jpg
│   │   └── asus_rog.jpg
│   ├── shoes/
│   │   ├── nike_air.jpg
│   │   ├── adidas_boost.jpg
│   │   └── puma_rsx.jpg
│   ├── watches/
│   │   ├── apple_watch.jpg
│   │   ├── samsung_watch.jpg
│   │   └── fossil_watch.jpg
│   ├── headphones/
│   │   ├── sony_wh.jpg
│   │   ├── airpods_pro.jpg
│   │   └── bose_qc.jpg
│   └── clothes/
│       ├── tshirt.jpg
│       ├── jeans.jpg
│       └── jacket.jpg
```

## 🖼️ Recommended Image Sizes

| Type | Size |
|------|------|
| Product List | 300x300 to 500x500 px |
| Product Detail | 500x500 to 800x800 px |
| Category | 300x300 px |
| Cart | 120x120 to 150x150 px |

## 💾 Supported Formats
- JPG / JPEG
- PNG
- WebP
- GIF

## ⚡ Performance Tips
1. Compress images before upload (500KB max each)
2. Use consistent dimensions
3. Use modern formats (WebP > PNG > JPG)
4. Keep file names simple

---

## 🐛 Troubleshooting

### Image doesn't appear after upload?
- Click **Save** button (don't forget!)
- Refresh browser (Ctrl+F5)
- Check if image file size is reasonable

### See "No Image" placeholder?
- You haven't uploaded image yet
- OR upload failed (check file size)
- OR file was deleted

### What about old URLs?
- ✅ All removed!
- ✅ 100% local images only
- ✅ Works completely offline

---

## 📋 Checklist

- [ ] Admin panel accessible
- [ ] Can browse products
- [ ] Can upload image via admin
- [ ] Image appears on home page
- [ ] Image appears on product detail
- [ ] Image appears in cart
- [ ] Fallback image shows (if no image)

---

**Start Here**: http://127.0.0.1:8000/admin/shop/product/

Good luck! 🎉
