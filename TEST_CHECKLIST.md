# ✅ ShopSphere - Complete Test Checklist

## **Pre-Flight Check**

- [ ] All 4 services started (Auth, Product, Order, Frontend)
- [ ] No port conflicts (3000, 5000, 8001, 8002 available)
- [ ] npm packages installed in frontend
- [ ] Python dependencies installed for services
- [ ] Browser console open (F12) for debugging

---

## **🔐 Authentication Flow**

### Test 1: Login with Demo User
```
Expected: ✅ Success
Steps:
1. Navigate to http://127.0.0.1:3000
2. Click "Show Demo Users"
3. Click login on "demo" user
4. Should redirect to /home
5. Navbar shows "demo" user
```

### Test 2: Login with Wrong Credentials
```
Expected: ✅ Error message shown
Steps:
1. Enter username: "invalid"
2. Enter password: "wrong"
3. Click "Sign In"
4. Should show "❌ Invalid credentials"
```

### Test 3: Register New User
```
Expected: ✅ Success message shown
Steps:
1. Enter new username: "testuser"
2. Enter password: "test123"
3. Click "Create Account"
4. Should show "✅ Registration successful! Now login."
5. Login with new credentials
```

### Test 4: Logout Flow
```
Expected: ✅ Redirects to login
Steps:
1. While logged in, click "Logout" button
2. Should redirect to /login
3. Navbar should not show user
```

---

## **🏠 Home Page & Products**

### Test 5: Products Display
```
Expected: ✅ 10 products loaded
Steps:
1. Login and navigate to Home
2. Should see product grid with 10 items:
   - Laptop
   - iPhone 15
   - Wireless Headphones
   - Smartwatch
   - USB-C Cable
   - Power Bank
   - Monitor
   - Mechanical Keyboard
   - Optical Mouse
   - Webcam
3. Each product shows: name, price, description, category badge
```

### Test 6: Product Search
```
Expected: ✅ Filter products by search term
Steps:
1. Type "laptop" in search box
2. Should show only Laptop product
3. Clear search
4. Should show all 10 products again
5. Search "cable" - show USB-C Cable
6. Case-insensitive search works
```

### Test 7: Add to Cart
```
Expected: ✅ Item added, cart badge updates
Steps:
1. Click "Add to Cart" on any product
2. Toast notification shows (green with ✅)
3. Cart badge in navbar shows "1"
4. Add 2 more products
5. Cart badge shows "3"
```

---

## **🛒 Cart Page**

### Test 8: View Cart Items
```
Expected: ✅ All added items displayed
Steps:
1. Click Cart in navbar
2. Should see all items added
3. Each item shows: product name, price, quantity
4. Total price calculated correctly
```

### Test 9: Remove from Cart
```
Expected: ✅ Item removed, badge updates
Steps:
1. Click remove button (🗑️) on an item
2. Item disappears
3. Cart badge decrements
4. Total price updates
```

### Test 10: Clear Cart
```
Expected: ✅ All items removed
Steps:
1. Click "Clear Cart" button
2. All items removed
3. Cart badge shows nothing
4. Message: "Your cart is empty"
```

### Test 11: Place Order
```
Expected: ✅ Order created, cart cleared
Steps:
1. Add 2-3 items to cart
2. Go to Cart page
3. Click "Place Order"
4. Toast shows success
5. Cart cleared
6. Redirect to Orders page
```

---

## **📦 Orders Page**

### Test 12: View Order History
```
Expected: ✅ Placed orders displayed
Steps:
1. Navigate to Orders page
2. Should see order created in Test 11
3. Shows: Order ID, Total, Status, Date
4. Status badge displays correctly
```

### Test 13: Order Details
```
Expected: ✅ Order info visible
Steps:
1. View order on Orders page
2. Verify order total matches cart total
3. Status shows "Pending" or "Completed"
4. Timestamp shows correct date
```

---

## **🎨 UI/UX Tests**

### Test 14: Navbar Display
```
Expected: ✅ Navbar shows/hides correctly
Steps:
1. Not logged in: navbar hidden or login button
2. Logged in: show user avatar with first letter
3. Show user username
4. Cart badge appears only when items exist
5. Responsive on mobile (resize browser)
```

### Test 15: Responsive Design
```
Expected: ✅ Works on all screen sizes
Steps:
1. Desktop (1920x1080)
2. Tablet (768x1024)
3. Mobile (375x667)
4. All text readable, buttons clickable
5. No horizontal scrolling
```

### Test 16: Loading States
```
Expected: ✅ Loading spinners shown
Steps:
1. Login (should show "Logging in..." button)
2. Search products (should load)
3. Add to cart (should not show loading, instant)
4. Place order (should show "Placing order...")
```

---

## **🔒 Security Tests**

### Test 17: Protected Routes
```
Expected: ✅ Can't access /home without login
Steps:
1. Logout (or clear localStorage)
2. Try to access http://127.0.0.1:3000/home
3. Should redirect to /login
4. Try /cart and /orders - same result
```

### Test 18: Token Persistence
```
Expected: ✅ Token saved and restored
Steps:
1. Login with demo user
2. Refresh page (F5)
3. Should still be logged in
4. Clear localStorage
5. Refresh page
6. Should be redirected to /login
```

### Test 19: Token Expiry (401 Error)
```
Expected: ✅ Auto-logout on invalid token
Steps:
1. Login and get token
2. Manually clear token in localStorage
3. Try to make API call
4. Should redirect to /login
```

---

## **🐛 Error Handling**

### Test 20: Network Errors
```
Expected: ✅ Graceful error messages
Steps:
1. Stop Auth Service
2. Try to login
3. Should show "❌ Connection error..."
4. Restart service
5. Login works again
```

### Test 21: Invalid API Response
```
Expected: ✅ Handle errors gracefully
Steps:
1. Modify product search to invalid endpoint
2. Should show error, not crash
3. Page still functional
```

---

## **📱 Browser Compatibility**

- [ ] Chrome (Latest)
- [ ] Firefox (Latest)
- [ ] Safari (Latest)
- [ ] Edge (Latest)
- [ ] Mobile browsers (iOS Safari, Chrome Mobile)

---

## **⚡ Performance Tests**

### Test 22: Page Load Time
```
Expected: ✅ < 3 seconds
Steps:
1. Open DevTools (F12)
2. Go to Network tab
3. Refresh home page
4. Check Total time
5. Should load in < 3 seconds
```

### Test 23: Search Performance
```
Expected: ✅ Instant results
Steps:
1. Type in search box quickly
2. Results filter in real-time
3. No lag or freeze
4. Completes before user finishes typing
```

### Test 24: Cart Operations
```
Expected: ✅ Instant add/remove
Steps:
1. Add to cart should be instant
2. Remove from cart should be instant
3. No loading spinner needed
4. Cart badge updates immediately
```

---

## **🎯 End-to-End User Journey**

### Test 25: Complete Shopping Flow
```
Scenario: New user buys products
Steps:
1. Start at login page
2. Click Show Demo Users
3. Login with john / john123
4. Browse home page (10 products visible)
5. Search for "watch" (Smartwatch appears)
6. Add Smartwatch to cart
7. See cart badge "1"
8. Continue shopping, add Monitor
9. Cart badge shows "2"
10. Add USB-C Cable
11. Cart badge shows "3"
12. Go to cart
13. See 3 items, total price correct
14. Place order
15. Success message shown
16. Redirected to Orders page
17. See new order with correct total
18. Logout
19. Redirected to login
20. Can't access /home anymore
```

Expected: ✅ All 20 steps complete without errors

---

## **📋 Data Persistence Tests**

### Test 26: Cart Persistence
```
Expected: ✅ Cart saved across refresh
Steps:
1. Add items to cart
2. Refresh page (F5)
3. Items still in cart
4. Quantities unchanged
5. Total price same
```

### Test 27: Auth Persistence
```
Expected: ✅ Stay logged in after refresh
Steps:
1. Login with demo user
2. Refresh page (F5)
3. Should still be logged in
4. User name visible in navbar
5. Can access protected pages
```

---

## **🚀 Production Readiness**

### Test 28: Build Process
```bash
Expected: ✅ No build errors
Steps:
cd frontend
npm run build
# Should complete with no errors
# Check build/ folder exists
```

### Test 29: Docker Build
```bash
Expected: ✅ All services build successfully
Steps:
docker-compose build
# All 4 services should build
# No errors in output
```

### Test 30: Docker Run
```bash
Expected: ✅ All services start with docker-compose
Steps:
docker-compose up
# All services should start
# All health checks should pass
# App accessible at localhost:3000
```

---

## **📊 Test Summary**

| Test # | Category | Status | Notes |
|--------|----------|--------|-------|
| 1-4 | Auth | ⬜ | |
| 5-7 | Products | ⬜ | |
| 8-11 | Cart | ⬜ | |
| 12-13 | Orders | ⬜ | |
| 14-16 | UI/UX | ⬜ | |
| 17-19 | Security | ⬜ | |
| 20-21 | Errors | ⬜ | |
| 22-24 | Performance | ⬜ | |
| 25 | E2E | ⬜ | |
| 26-27 | Persistence | ⬜ | |
| 28-30 | Production | ⬜ | |

---

## **Issues Found & Fixed**

| Issue | Status | Resolution |
|-------|--------|-----------|
| | ⬜ | |
| | ⬜ | |

---

## **Sign-Off**

**Tested By**: ________________
**Date**: ________________
**Environment**: Local / Docker / Production
**Browser**: ________________
**Result**: ✅ PASS / ⚠️ PARTIAL / ❌ FAIL

**Notes**:
```
[Space for additional notes]
```

---

**All tests should pass before deploying to production!**

🎉 When all 30 tests pass, ShopSphere is ready for deployment!
