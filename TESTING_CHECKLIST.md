# ✅ ShopCart MVP - Testing Checklist

## Pre-Test Setup
- [x] Django server running on http://127.0.0.1:8000/
- [x] Database populated with 10 sample products
- [x] Admin account created (admin/admin123)
- [x] All models created and migrated

---

## 🛍️ Product Display Tests

### Product List Page
- [ ] Visit http://127.0.0.1:8000/ - page loads correctly
- [ ] All 10 products display in a grid
- [ ] Product images show (placeholder emoji appears if no image)
- [ ] Product names are visible
- [ ] Product prices display correctly (₹ symbol)
- [ ] Stock status shows availability
- [ ] "View Details" button appears on each product
- [ ] Page is responsive (test on smaller screens)

### Product Detail Page
- [ ] Click "View Details" on any product
- [ ] Page loads with product information
- [ ] Large product image/placeholder displays
- [ ] Full product description shows
- [ ] Current price displays prominently
- [ ] Stock status shows availability
- [ ] Quantity input field appears (defaults to 1)
- [ ] "Add to Cart" button is enabled for in-stock items
- [ ] "Add to Cart" button is disabled for out-of-stock items
- [ ] Back to Products link works

---

## 🛒 Shopping Cart Tests

### Add to Cart
- [ ] Enter quantity (e.g., 2) and click "Add to Cart"
- [ ] Success message appears
- [ ] Redirected to cart page
- [ ] Item appears in cart with correct quantity
- [ ] Subtotal calculates correctly (price × quantity)
- [ ] Cart count in navigation updates
- [ ] Try adding same product again - quantity increases
- [ ] Try adding more than available stock - error shows
- [ ] Try quantity 0 or negative - validation fails
- [ ] Try quantity > 100 - validation fails

### View Cart
- [ ] Navigate to cart via nav link
- [ ] All added items display
- [ ] Product names link back to detail pages
- [ ] Prices are correct
- [ ] Quantities are correct
- [ ] Subtotals calculate correctly for each item
- [ ] Order summary shows correct totals
- [ ] Free shipping appears
- [ ] Total amount is accurate
- [ ] Item count in nav matches cart items

### Update Quantity
- [ ] Change quantity to different number
- [ ] Click "Update" button
- [ ] Success message appears
- [ ] Subtotal recalculates immediately
- [ ] Order total updates
- [ ] Try invalid quantity (0, >100) - validation fails
- [ ] Try quantity exceeding stock - validation error shows

### Remove Item
- [ ] Click "Remove" button on any item
- [ ] Confirmation dialog appears
- [ ] Item removed from cart
- [ ] Success message shows
- [ ] Total recalculates
- [ ] Item count in nav updates

### Empty Cart
- [ ] Remove all items from cart
- [ ] Empty cart message appears
- [ ] "Start Shopping" link works
- [ ] Clicking takes you back to products

---

## 💳 Checkout Tests

### Checkout Form
- [ ] Click "Proceed to Checkout" from cart
- [ ] Empty cart shows error and redirects
- [ ] Form loads with all required fields
- [ ] Form sections are clearly labeled:
  - Customer Information
  - Shipping Address
  - Payment Method

### Customer Information Validation
- [ ] First Name:
  - [ ] Empty - shows error
  - [ ] Valid name - accepted
  - [ ] With numbers - shows error
  - [ ] With special chars - shows error
- [ ] Last Name:
  - [ ] Empty - shows error
  - [ ] Valid name - accepted
  - [ ] With numbers - shows error
- [ ] Email:
  - [ ] Empty - shows error
  - [ ] Invalid format (no @) - shows error
  - [ ] Valid email - accepted
- [ ] Phone:
  - [ ] Empty - shows error
  - [ ] Less than 9 digits - shows error
  - [ ] More than 15 digits - shows error
  - [ ] Valid 10-digit number - accepted
  - [ ] With + and country code - accepted

### Shipping Address Validation
- [ ] Address:
  - [ ] Empty - shows error
  - [ ] Valid address - accepted
  - [ ] Very long address (>255) - shows error
- [ ] City:
  - [ ] Empty - shows error
  - [ ] Valid city - accepted
- [ ] State:
  - [ ] Empty - shows error
  - [ ] Valid state - accepted
- [ ] Postal Code:
  - [ ] Empty - shows error
  - [ ] Valid alphanumeric - accepted
  - [ ] Special characters - shows error

### Payment Method
- [ ] COD option appears and is selected by default
- [ ] Payment method selection works
- [ ] Help text explains COD is "Pay on Delivery"

### Order Summary (Right Sidebar)
- [ ] All items with quantities display
- [ ] Prices are correct
- [ ] Subtotal matches cart total
- [ ] Shipping is free
- [ ] Grand total is accurate
- [ ] Summary updates when form is modified (if JavaScript)

### Order Submission
- [ ] Fill all fields correctly and submit
- [ ] No errors appear
- [ ] Redirected to order confirmation page
- [ ] Order is created in database
- [ ] Stock reduces automatically (check admin)
- [ ] Cart clears after checkout

---

## ✅ Order Confirmation Tests

### Confirmation Page
- [ ] Success checkmark displays
- [ ] "Order Placed Successfully!" message shows
- [ ] Order ID displays prominently
- [ ] Order number is a valid ID from database
- [ ] Thank you message appears

### Order Details
- [ ] Customer name displays correctly
- [ ] Email shows
- [ ] Phone shows
- [ ] Complete address displays:
  - [ ] Street address
  - [ ] City, State, Postal Code
- [ ] Order items table shows:
  - [ ] Product names
  - [ ] Quantities
  - [ ] Unit prices
  - [ ] Subtotals
- [ ] Total amount matches checkout
- [ ] Payment method shows "Cash on Delivery"
- [ ] Order status shows "Pending"
- [ ] Confirmation email text appears

### Post-Order Actions
- [ ] Click "Continue Shopping" to go back to products
- [ ] Create new order with different items
- [ ] Verify new order doesn't have old cart items

---

## 🔐 Validation Tests

### Client-Side Validation
- [ ] Form prevents submission with empty required fields
- [ ] Real-time validation messages appear
- [ ] Phone input rejects non-digits
- [ ] Postal code input rejects special characters
- [ ] Quantity input has min/max limits

### Server-Side Validation
- [ ] Use browser dev tools to bypass client validation
- [ ] Server still validates and rejects invalid data
- [ ] Appropriate error messages display
- [ ] No database errors occur

### Stock Validation
- [ ] Cannot add more than available stock
- [ ] Cannot update quantity to exceed stock
- [ ] When stock becomes 0, button disables
- [ ] Stock reduces after successful order

---

## 📊 Admin Panel Tests

### Login
- [ ] Visit http://127.0.0.1:8000/admin/
- [ ] Login form appears
- [ ] Login with admin/admin123
- [ ] Successfully authenticated

### Product Management
- [ ] All 10 products appear in list
- [ ] Can click to edit a product
- [ ] Can change price, stock, description
- [ ] Can upload product image
- [ ] Changes save correctly
- [ ] Can create new product
- [ ] Can delete a product
- [ ] Stock filter works

### Order Management
- [ ] All completed orders appear
- [ ] Can click to view order details
- [ ] Customer information displays
- [ ] Order items show correctly
- [ ] Total amount matches checkout
- [ ] Status can be changed
- [ ] Orders appear in reverse chronological order

### Cart Management
- [ ] Current carts appear in admin
- [ ] Can view items in each cart
- [ ] Cart totals calculate correctly

---

## 🎨 UI/UX Tests

### Responsive Design
- [ ] Test on desktop (1920x1080)
- [ ] Test on tablet (768px width)
- [ ] Test on mobile (375px width)
- [ ] All content is readable
- [ ] No horizontal scrolling
- [ ] Buttons are clickable on touch
- [ ] Images scale properly

### Navigation
- [ ] Logo links to home
- [ ] Product link works
- [ ] Cart link works
- [ ] Cart badge updates
- [ ] Back links work everywhere
- [ ] No broken links

### Messages & Feedback
- [ ] Success messages display (green)
- [ ] Error messages display (red)
- [ ] Messages auto-dismiss or have close button
- [ ] Multiple messages queue properly

### Performance
- [ ] Pages load quickly
- [ ] No console errors
- [ ] Images load properly
- [ ] Forms submit smoothly

---

## 🔄 Complete User Flow Test

### Full Purchase Journey
- [ ] 1. Start at product list
- [ ] 2. View 3 different products
- [ ] 3. Add items to cart from 2 products
- [ ] 4. Update quantity on one item
- [ ] 5. Go to cart and verify totals
- [ ] 6. Proceed to checkout
- [ ] 7. Fill all required fields
- [ ] 8. Submit order
- [ ] 9. Verify confirmation page
- [ ] 10. Check admin to see order created
- [ ] 11. Verify stock reduced in admin
- [ ] 12. Create new cart, verify old cart is gone

---

## 🐛 Edge Cases

### Cart Edge Cases
- [ ] Add same product twice - quantity increases
- [ ] Add product at max stock - only max allowed
- [ ] Remove all items - shows empty message
- [ ] Refresh cart - items persist
- [ ] Open cart in multiple tabs - stays consistent

### Checkout Edge Cases
- [ ] Submit with just spaces in fields - rejected
- [ ] Copy-paste same data - works fine
- [ ] Go back to cart then checkout again - works
- [ ] Change quantity in cart, then checkout - new total
- [ ] Add new item to cart before checkout completes - included

### Database Edge Cases
- [ ] Product with 1 stock item - can add but max 1
- [ ] Order with multiple of same item - all tracked
- [ ] Product stock exactly matching cart - checkout succeeds

---

## 📝 Notes for Fixes

Use this section to note any issues found:

```
Issue #1:
Description:
Steps to reproduce:
Expected:
Actual:
Severity: (High/Medium/Low)

---

Issue #2:
Description:
Steps to reproduce:
Expected:
Actual:
Severity: (High/Medium/Low)
```

---

## ✨ Final Checklist

- [ ] All features implemented
- [ ] All validations working
- [ ] Admin panel functional
- [ ] Database operational
- [ ] UI is professional
- [ ] Mobile responsive
- [ ] No console errors
- [ ] No database errors
- [ ] Performance is good
- [ ] Documentation complete

---

**Testing Status**: Ready for QA ✓
**Date**: January 22, 2026
**Tester**: [Your Name]
