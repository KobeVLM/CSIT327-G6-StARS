# Django Conversion - File Dependencies

## 📦 Complete File List (Simplified for Django)

### **1. Core CSS** (Copy First)
```
/styles/globals.css
```

### **2. Layout Components**
```
/components/Header.tsx          → Used by Login, Register
/components/AppHeader.tsx       → Used by Dashboard, Profile, Settings
/components/Sidebar.tsx         → Use SIMPLIFIED version (see below)
```

### **3. Page Components**
```
/components/pages/Login.tsx
/components/pages/Register.tsx
/components/pages/Dashboard.tsx
/components/pages/Profile.tsx
/components/pages/Settings.tsx
```

### **4. Main App Logic**
```
App.tsx                         → Use SIMPLIFIED version (see below)
```

---

## 🔗 Lucide Icons Dependencies

### **Icons Used (Install via CDN or npm)**

**Header.tsx:**
- `Palette`

**AppHeader.tsx:**
- `Palette`, `Star`, `ChevronDown`, `Settings`, `LogOut`

**Sidebar.tsx (Simplified):**
- `Home`, `User`

**Login.tsx:**
- `Palette`, `AlertCircle`, `Loader2`

**Register.tsx:**
- `Palette`, `AlertCircle`, `Loader2`

**Dashboard.tsx:**
- `Upload`, `Search`, `Award`, `ImageIcon`, `TrendingUp`, `Edit`, `X`

**Profile.tsx:**
- `MapPin`, `Globe`, `Calendar`, `Heart`, `Share2`, `Edit`, `Save`, `X`

**Settings.tsx:**
- `Bell`, `Globe`, `User`, `Lock`, `Moon`, `Sun`

### **CDN Installation (Add to Django base.html):**
```html
<script src="https://unpkg.com/lucide@latest"></script>
<script>
  lucide.createIcons();
</script>
```

---

## 🎨 Tailwind Classes Used

Your design uses **ONLY Tailwind utility classes** - no custom components needed!

### **Common Patterns:**

**Cards:**
```html
<div class="bg-white rounded-lg p-6 shadow-sm">
```

**Buttons (Primary):**
```html
<button class="bg-primary text-white px-6 py-2.5 rounded hover:opacity-90">
```

**Buttons (Secondary):**
```html
<button class="bg-secondary text-foreground px-4 py-2 rounded hover:bg-secondary/80">
```

**Input Fields:**
```html
<input class="w-full px-3 py-2 border border-input rounded bg-white">
```

**Alert (Error):**
```html
<div class="p-3 bg-destructive/10 border border-destructive/20 rounded flex items-start gap-2">
```

**Alert (Success):**
```html
<div class="bg-success/10 border border-success/20 rounded-lg px-4 py-3">
```

---

## 🚫 What to EXCLUDE

### **Don't Copy These Files:**
```
❌ /components/pages/AdminLogin.tsx
❌ /components/pages/Browse.tsx
❌ /components/pages/Upload.tsx
❌ /components/pages/Moderation.tsx
❌ /components/pages/Badges.tsx
❌ /components/ui/*  (entire shadcn folder - not used!)
```

---

## 📝 Modifications Needed

### **1. Sidebar.tsx - Remove Browse/Upload/Admin**
**Original has:**
- Browse
- Upload Artwork
- Moderation (admin)

**Simplified version keeps only:**
- Home (Dashboard)
- Profile

**File:** `/DJANGO_CONVERSION/Sidebar-simplified.tsx`

---

### **2. App.tsx - Remove Admin/Browse/Upload logic**
**Original has:**
- AdminLogin handling
- Browse page
- Upload page
- Moderation page
- isAdmin state

**Simplified version keeps only:**
- Login/Register
- Dashboard
- Profile
- Settings

**File:** `/DJANGO_CONVERSION/App-simplified.tsx`

---

### **3. Login.tsx - Remove Admin Login Link**
You can either:
- Keep the "Admin Login" button (it does nothing in simplified version)
- Or modify Login.tsx to remove this line (around line 165):
```tsx
// Remove this section:
<div className="mt-3 text-center pt-3 border-t border-border">
  <button
    onClick={onNavigateToAdminLogin}
    className="text-muted-foreground hover:text-primary transition-colors"
    style={{ fontSize: '0.75rem', fontWeight: '500' }}
  >
    Admin Login
  </button>
</div>
```

---

## 🔄 Django Conversion Steps

### **Step 1: Copy Files**
```
django_project/
├── static/
│   ├── css/
│   │   └── globals.css                    ← Copy from /styles/
│   └── js/
│       ├── darkmode.js                    ← Extract from Settings.tsx
│       └── dropdown.js                    ← Extract from AppHeader.tsx
│
├── templates/
│   ├── base.html                          ← AppHeader + Sidebar layout
│   ├── auth/
│   │   ├── login.html                     ← From Login.tsx
│   │   └── register.html                  ← From Register.tsx
│   ├── dashboard.html                     ← From Dashboard.tsx
│   ├── profile.html                       ← From Profile.tsx
│   └── settings.html                      ← From Settings.tsx
```

### **Step 2: Extract JavaScript**
You'll need vanilla JS for:
1. **Dark Mode Toggle** (Settings page)
2. **Profile Dropdown** (AppHeader)
3. **Inline Profile Edit** (Profile page)
4. **Dashboard Search** (Dashboard page)

### **Step 3: Django Views**
Create views for:
- `LoginView` / `RegisterView` (Django auth)
- `DashboardView`
- `ProfileView` / `ProfileUpdateView`
- `SettingsView`

---

## ✅ Checklist

**Files to Copy:**
- [ ] `/styles/globals.css`
- [ ] `/components/Header.tsx`
- [ ] `/components/AppHeader.tsx`
- [ ] `/components/Sidebar.tsx` (use simplified version)
- [ ] `/components/pages/Login.tsx`
- [ ] `/components/pages/Register.tsx`
- [ ] `/components/pages/Dashboard.tsx`
- [ ] `/components/pages/Profile.tsx`
- [ ] `/components/pages/Settings.tsx`

**Modifications:**
- [ ] Use simplified `Sidebar.tsx`
- [ ] Use simplified `App.tsx`
- [ ] Optional: Remove "Admin Login" from Login.tsx

**Dependencies:**
- [ ] Add Lucide Icons CDN to base.html
- [ ] Include Tailwind CSS build
- [ ] Extract JavaScript for interactivity

---

## 🎯 Result

You'll have a **fully functional Django prototype** with:
✅ Login/Register with email validation
✅ Dashboard with search and stats
✅ Profile with inline editing
✅ Settings with dark mode toggle
✅ Clean design matching your Figma specs

**Zero external UI library dependencies** - just HTML, CSS, and vanilla JS!
