# STARS Design Extraction Guide
## What to Copy from Your React Prototype to Django

---

## Quick Navigation

- [Part 1: CSS Extraction](#part-1-css-extraction)
- [Part 2: Component Structure Extraction](#part-2-component-structure-extraction)
- [Part 3: Page-by-Page Extraction](#part-3-page-by-page-extraction)
- [Part 4: JavaScript Extraction](#part-4-javascript-extraction)
- [Part 5: Verification Checklist](#part-5-verification-checklist)

---

## Part 1: CSS Extraction

### Step 1.1: Extract Color Variables from `styles/globals.css`

**📂 Source File:** `/styles/globals.css`

**✂️ What to Copy:**
- All CSS custom properties from `:root` block (lines 3-22)
- All dark mode properties from `:root.dark` block (lines 24-43)

**📁 Destination:** `static/css/variables.css` (Django)

**✅ Action:**

1. Copy the `:root` block from your `globals.css`
2. Rename `--font-size`, `--font-weight-*` to match the guide's naming:
   - `--font-weight-medium: 500` → Keep as is
   - `--font-weight-normal: 400` → Keep as is
3. Add spacing, border-radius, font-size, and shadow variables from the guide

**Example Conversion:**

```css
/* FROM: styles/globals.css (your current file) */
:root {
  --background: #F5F7FB;
  --foreground: #2C3E50;
  --primary: #5865F2;
  --border: #E0E4EB;
  /* ... etc */
}

/* TO: static/css/variables.css (Django) */
:root {
  /* Colors (keep exactly as is) */
  --color-primary: #5865F2;
  --color-background: #F5F7FB;
  --color-foreground: #2C3E50;
  --color-border: #E0E4EB;
  /* ... etc */
  
  /* ADD these new variables: */
  --spacing-xs: 0.25rem;
  --spacing-sm: 0.5rem;
  --spacing-md: 1rem;
  --spacing-lg: 1.5rem;
  --spacing-xl: 2rem;
  --spacing-2xl: 3rem;
  
  --radius-sm: 0.25rem;
  --radius-md: 0.5rem;
  --radius-lg: 0.75rem;
  --radius-xl: 1rem;
  --radius-full: 9999px;
  
  --font-xs: 0.75rem;
  --font-sm: 0.875rem;
  --font-base: 1rem;
  --font-lg: 1.125rem;
  --font-xl: 1.25rem;
  --font-2xl: 1.5rem;
  --font-3xl: 1.75rem;
  
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.1);
  --shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.1);
}
```

---

### Step 1.2: Extract Typography from `styles/globals.css`

**📂 Source File:** `/styles/globals.css` (lines 73-131)

**✂️ What to Copy:**
- Typography styles for h1, h2, h3, h4, p, label, button, input

**📁 Destination:** `static/css/base.css` (Django)

**✅ Action:**

Copy the typography section and convert Tailwind variables to standard CSS:

```css
/* FROM: styles/globals.css */
h1 {
  font-size: 1.875rem;
  font-weight: var(--font-weight-medium);
  line-height: 1.5;
  color: var(--foreground);
}

/* TO: static/css/base.css */
h1 {
  font-size: var(--font-3xl);  /* Or keep 1.875rem */
  font-weight: var(--font-semibold);
  color: var(--color-foreground);
  margin-bottom: var(--spacing-md);
}
```

**📝 Note:** See the full `base.css` example in **FIGMA_TO_DJANGO_CONVERSION_GUIDE.md** → **Step 2.2** → **"Create Base Styles"**

---

### Step 1.3: Create Component Styles from Tailwind Classes

**📂 Source Files:** All component files in `/components/`

**✂️ What to Extract:**
- Common Tailwind patterns (buttons, inputs, cards, etc.)

**📁 Destination:** `static/css/components.css` (Django)

**✅ Action:**

Look for repeated Tailwind patterns in your components and convert them:

| Tailwind Pattern (React) | CSS Class (Django) | Location |
|--------------------------|-------------------|----------|
| `className="bg-primary text-white px-6 py-2.5 rounded"` | `.btn-primary` | components.css |
| `className="bg-white rounded-lg p-6 shadow-sm"` | `.card` | components.css |
| `className="w-full px-3 py-2 border border-input rounded"` | `.form-input` | components.css |
| `className="text-sm text-muted-foreground"` | `.text-muted` + `font-size: var(--font-sm)` | components.css |

**📝 Full component styles:** See **FIGMA_TO_DJANGO_CONVERSION_GUIDE.md** → **Step 2.2** → **"Create Component Styles"**

---

## Part 2: Component Structure Extraction

### Step 2.1: Extract Header/Navbar Structure

**📂 Source File:** `/components/AppHeader.tsx`

**✂️ What to Copy:**
- JSX structure (HTML elements)
- User info display (level, XP, username)
- Dropdown menu items
- SVG icons

**📁 Destination:** `templates/includes/header.html` (Django)

**✅ Step-by-Step:**

1. **Open:** `/components/AppHeader.tsx`
2. **Find:** The main return JSX (starting around line 40)
3. **Copy:** The entire JSX structure
4. **Convert:**

```jsx
// FROM: components/AppHeader.tsx (React)
<header className="h-16 bg-card border-b border-border flex items-center justify-between px-6">
  <div className="flex items-center gap-2">
    <span className="text-xl font-bold text-primary">STARS</span>
  </div>
  
  <div className="flex items-center gap-4">
    {/* User stats */}
    <div className="flex items-center gap-3">
      <span className="text-sm font-medium flex items-center gap-1">
        <Star className="w-4 h-4 text-yellow-500" fill="currentColor" />
        Level {user.level}
      </span>
      <span className="text-sm text-primary font-medium">{user.xp} XP</span>
    </div>
    
    {/* User dropdown */}
    <div className="relative">
      <button className="flex items-center gap-2">
        <div className="w-8 h-8 rounded-full bg-primary text-white">
          {user.username.charAt(0).toUpperCase()}
        </div>
        <span>{user.username}</span>
      </button>
    </div>
  </div>
</header>
```

```html
<!-- TO: templates/includes/header.html (Django) -->
<header class="app-header">
  <div class="header-content">
    <div class="header-logo">
      <a href="{% url 'gallery:dashboard' %}">
        <span class="logo-text">STARS</span>
      </a>
    </div>
    
    <div class="header-right">
      <!-- User stats -->
      <div class="user-stats">
        <span class="user-level">
          <svg class="icon icon-star" width="16" height="16"><!-- SVG path --></svg>
          Level {{ request.user.profile.level }}
        </span>
        <span class="user-xp">{{ request.user.profile.xp }} XP</span>
      </div>
      
      <!-- User dropdown -->
      <div class="user-dropdown">
        <button class="user-button">
          <div class="avatar">
            {{ request.user.username|first|upper }}
          </div>
          <span>{{ request.user.username }}</span>
        </button>
      </div>
    </div>
  </div>
</header>
```

**📝 Full header template:** See **FIGMA_TO_DJANGO_CONVERSION_GUIDE.md** → **Step 4.2**

---

### Step 2.2: Extract Sidebar Structure

**📂 Source File:** `/components/Sidebar.tsx`

**✂️ What to Copy:**
- Navigation menu items
- User profile section
- Stats section
- SVG icons for each menu item

**📁 Destination:** `templates/includes/sidebar.html` (Django)

**✅ Step-by-Step:**

1. **Open:** `/components/Sidebar.tsx`
2. **Find:** Navigation items (look for `onNavigate('dashboard')`, etc.)
3. **Copy:** The menu structure
4. **Convert:**

```jsx
// FROM: components/Sidebar.tsx (React)
<nav className="flex flex-col gap-1 mb-8">
  <button
    onClick={() => onNavigate('dashboard')}
    className={`flex items-center gap-3 px-4 py-2.5 rounded-lg ${
      currentPage === 'dashboard' 
        ? 'bg-primary text-primary-foreground' 
        : 'text-foreground hover:bg-secondary'
    }`}
  >
    <LayoutGrid className="w-5 h-5" />
    Dashboard
  </button>
  
  <button onClick={() => onNavigate('browse')}>
    <Image className="w-5 h-5" />
    Browse
  </button>
  
  {/* ...more nav items */}
</nav>
```

```html
<!-- TO: templates/includes/sidebar.html (Django) -->
<nav class="sidebar-nav">
  <a href="{% url 'gallery:dashboard' %}" 
     class="nav-item {% if request.resolver_match.url_name == 'dashboard' %}active{% endif %}">
    <svg class="nav-icon" width="20" height="20"><!-- SVG path --></svg>
    Dashboard
  </a>
  
  <a href="{% url 'gallery:browse' %}" 
     class="nav-item {% if request.resolver_match.url_name == 'browse' %}active{% endif %}">
    <svg class="nav-icon" width="20" height="20"><!-- SVG path --></svg>
    Browse
  </a>
  
  <!-- ...more nav items -->
</nav>
```

**🎨 CSS for active state:**

```css
/* static/css/layout.css */
.nav-item.active {
  background-color: var(--color-primary);
  color: var(--color-primary-foreground);
}
```

**📝 Full sidebar template:** See **FIGMA_TO_DJANGO_CONVERSION_GUIDE.md** → **Step 4.3**

---

## Part 3: Page-by-Page Extraction

### Step 3.1: Login Page

**📂 Source File:** `/components/pages/Login.tsx`

**✂️ What to Copy:**
1. **Layout structure** - Container, card, logo section
2. **Form fields** - Email/username input, password input
3. **Links** - Register link, Admin login link
4. **Styling patterns** - Card styling, form styling

**📁 Destination:** `apps/users/templates/users/login.html` (Django)

**✅ Extraction Steps:**

1. **Open:** `/components/pages/Login.tsx`

2. **Identify sections to copy:**
   - Line ~20-30: Logo and welcome section
   - Line ~40-70: Form inputs
   - Line ~80-90: Links section

3. **Extract each section:**

```jsx
// SECTION 1: Logo & Header (from Login.tsx)
<div className="text-center mb-8">
  <div className="w-16 h-16 bg-primary rounded-2xl flex items-center justify-center mx-auto mb-4">
    <Palette className="w-8 h-8 text-white" />
  </div>
  <h1 className="text-3xl font-semibold text-foreground mb-2">STARS</h1>
  <p className="text-sm text-muted-foreground">Student Artist Space</p>
</div>

<div className="mb-6">
  <h2 className="text-2xl font-semibold text-center mb-2">Welcome Back</h2>
  <p className="text-sm text-muted-foreground text-center">
    Sign in to your account to continue
  </p>
</div>
```

```html
<!-- TO: Django template -->
<div class="auth-logo">
  <div class="logo-icon">
    <svg width="32" height="32"><!-- Palette SVG --></svg>
  </div>
  <h1>STARS</h1>
  <p class="tagline">Student Artist Space</p>
</div>

<div class="auth-header">
  <h2>Welcome Back</h2>
  <p class="text-muted">Sign in to your account to continue</p>
</div>
```

```jsx
// SECTION 2: Form (from Login.tsx)
<form onSubmit={handleSubmit} className="space-y-4">
  <div>
    <label className="block text-sm font-medium mb-1.5">
      Email or Username
    </label>
    <input
      type="text"
      value={email}
      onChange={(e) => setEmail(e.target.value)}
      placeholder="name@example.com"
      className="w-full px-3 py-2 border border-input rounded-md bg-input-background"
      required
    />
  </div>
  
  <div>
    <label className="block text-sm font-medium mb-1.5">Password</label>
    <input
      type="password"
      value={password}
      onChange={(e) => setPassword(e.target.value)}
      placeholder="••••••••"
      className="w-full px-3 py-2 border border-input rounded-md bg-input-background"
      required
    />
  </div>
  
  <button
    type="submit"
    className="w-full bg-primary text-white py-2.5 rounded-md hover:opacity-90"
  >
    Sign In
  </button>
</form>
```

```html
<!-- TO: Django template -->
<form method="post" class="auth-form">
  {% csrf_token %}
  
  <div class="form-group">
    <label for="{{ form.username.id_for_label }}" class="form-label">
      Email or Username
    </label>
    {{ form.username }}
    {% if form.username.errors %}
      <div class="form-error">{{ form.username.errors }}</div>
    {% endif %}
  </div>
  
  <div class="form-group">
    <label for="{{ form.password.id_for_label }}" class="form-label">
      Password
    </label>
    {{ form.password }}
    {% if form.password.errors %}
      <div class="form-error">{{ form.password.errors }}</div>
    {% endif %}
  </div>
  
  <button type="submit" class="btn btn-primary btn-block">
    Sign In
  </button>
</form>
```

```jsx
// SECTION 3: Links (from Login.tsx)
<div className="text-center text-sm text-muted-foreground">
  <p className="mb-2">
    Don't have an account?{' '}
    <button
      onClick={onNavigateToRegister}
      className="text-primary font-medium hover:underline"
    >
      Create Account
    </button>
  </p>
  <button
    onClick={onNavigateToAdminLogin}
    className="text-muted-foreground hover:text-foreground"
  >
    Admin Login
  </button>
</div>
```

```html
<!-- TO: Django template -->
<div class="auth-links">
  <p>
    Don't have an account? 
    <a href="{% url 'users:register' %}">Create Account</a>
  </p>
  <p>
    <a href="{% url 'users:admin_login' %}" class="admin-link">Admin Login</a>
  </p>
</div>
```

**📝 Complete Login template:** See **FIGMA_TO_DJANGO_CONVERSION_GUIDE.md** → **Step 9.1**

---

### Step 3.2: Dashboard Page

**📂 Source File:** `/components/pages/Dashboard.tsx`

**✂️ What to Copy:**
1. **Search bar** (lines ~30-50)
2. **Stats cards** (lines ~60-120)
3. **Artworks grid** (lines ~130-200)

**📁 Destination:** `apps/gallery/templates/gallery/dashboard.html` (Django)

**✅ Extraction Steps:**

```jsx
// FROM: components/pages/Dashboard.tsx

// SECTION 1: Search Bar
<div className="mb-6">
  <div className="relative">
    <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-muted-foreground" />
    <input
      type="text"
      value={searchQuery}
      onChange={(e) => setSearchQuery(e.target.value)}
      placeholder="Search artworks or users..."
      className="w-full pl-10 pr-4 py-2.5 border border-input rounded-lg"
    />
  </div>
</div>
```

```html
<!-- TO: Django template -->
<div class="search-section">
  <form method="get" action="{% url 'gallery:dashboard' %}" class="search-form">
    <svg class="search-icon" width="20" height="20"><!-- Search SVG --></svg>
    {{ search_form.query }}
    <button type="submit" class="btn btn-primary">Search</button>
  </form>
</div>
```

```jsx
// SECTION 2: Stats Cards
<div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
  <div className="bg-card p-6 rounded-lg border border-border">
    <div className="flex items-center gap-4">
      <div className="w-12 h-12 rounded-lg bg-primary/10 flex items-center justify-center">
        <Image className="w-6 h-6 text-primary" />
      </div>
      <div>
        <p className="text-sm text-muted-foreground">Artworks Created</p>
        <p className="text-2xl font-semibold">{userStats.artworkCreated}</p>
      </div>
    </div>
  </div>
  
  {/* More stat cards... */}
</div>
```

```html
<!-- TO: Django template -->
<div class="stats-grid">
  <div class="stat-card">
    <div class="stat-icon stat-icon-blue">
      <svg width="24" height="24"><!-- Image SVG --></svg>
    </div>
    <div class="stat-content">
      <p class="stat-label">Artworks Created</p>
      <p class="stat-value">{{ user_stats.artworkCreated }}</p>
    </div>
  </div>
  
  <!-- More stat cards... -->
</div>
```

```jsx
// SECTION 3: Artworks Grid
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
  {mockPosts.map((post) => (
    <div key={post.id} className="bg-card rounded-lg overflow-hidden border border-border">
      <div className="aspect-[4/3] bg-muted">
        <img src={post.image} alt={post.title} className="w-full h-full object-cover" />
      </div>
      <div className="p-4">
        <div className="flex items-center gap-2 mb-3">
          <div className="w-8 h-8 rounded-full bg-primary text-white">
            {post.user.charAt(0).toUpperCase()}
          </div>
          <div>
            <h4 className="font-medium text-sm">{post.title}</h4>
            <p className="text-xs text-muted-foreground">@{post.user}</p>
          </div>
        </div>
        
        <div className="flex items-center gap-4 text-sm text-muted-foreground">
          <span className="flex items-center gap-1">
            <Heart className="w-4 h-4" /> {post.likes}
          </span>
          <span className="flex items-center gap-1">
            <Share2 className="w-4 h-4" /> {post.shares}
          </span>
        </div>
      </div>
    </div>
  ))}
</div>
```

```html
<!-- TO: Django template -->
<div class="artworks-grid">
  {% for post in posts %}
    <div class="artwork-card">
      <div class="artwork-image-container">
        <img src="{{ post.image.url }}" alt="{{ post.title }}" class="artwork-image">
      </div>
      
      <div class="artwork-content">
        <div class="artwork-header">
          <div class="avatar avatar-sm">
            {{ post.user.username|first|upper }}
          </div>
          <div>
            <h4 class="artwork-title">{{ post.title }}</h4>
            <p class="artwork-author">@{{ post.user.username }}</p>
          </div>
        </div>
        
        <div class="artwork-stats">
          <span class="stat-item">
            <svg class="icon" width="16" height="16"><!-- Heart SVG --></svg>
            {{ post.like_count }}
          </span>
          <span class="stat-item">
            <svg class="icon" width="16" height="16"><!-- Share SVG --></svg>
            {{ post.share_count }}
          </span>
        </div>
      </div>
    </div>
  {% endfor %}
</div>
```

**📝 Complete Dashboard template:** See **FIGMA_TO_DJANGO_CONVERSION_GUIDE.md** → **Step 9.2**

---

### Step 3.3: Upload Page

**📂 Source File:** `/components/pages/Upload.tsx`

**✂️ What to Copy:**
1. **File upload area** (lines ~170-220)
2. **Filter section** (lines ~230-250)
3. **Form fields** (lines ~260-395)
4. **Tag input** (lines ~314-362)

**📁 Destination:** `apps/gallery/templates/gallery/upload.html` (Django)

**✅ Extraction Steps:**

```jsx
// FROM: components/pages/Upload.tsx

// SECTION 1: File Upload Area
<div className="border-2 border-dashed border-border rounded-lg p-8 text-center">
  <input
    ref={fileInputRef}
    type="file"
    accept="image/*"
    onChange={handleFileChange}
    className="hidden"
    id="file-upload"
  />
  <label htmlFor="file-upload" className="cursor-pointer">
    {previewUrl ? (
      <div>
        <img src={previewUrl} alt="Preview" className="max-h-64 rounded" />
        <button type="button" onClick={removeFile}>
          <X className="w-4 h-4" />
        </button>
      </div>
    ) : (
      <>
        <UploadIcon className="w-12 h-12 mx-auto mb-3 text-muted-foreground" />
        <p>Click to upload or drag and drop</p>
        <p>PNG, JPG, or GIF (max. 10MB)</p>
      </>
    )}
  </label>
</div>
```

```html
<!-- TO: Django template -->
<div class="upload-area" id="upload-area">
  <input 
    type="file" 
    name="image" 
    id="id_image" 
    accept="image/*" 
    class="upload-input"
    required
  >
  <label for="id_image" class="upload-label">
    <svg class="upload-icon" width="48" height="48"><!-- Upload SVG --></svg>
    <p>Click to upload or drag and drop</p>
    <p class="upload-help">PNG, JPG, or GIF (max. 10MB)</p>
  </label>
  <div id="preview-container" style="display: none;">
    <img id="preview-image" src="" alt="Preview" class="preview-image">
    <button type="button" id="remove-image" class="btn btn-outline">Remove</button>
  </div>
</div>
```

```jsx
// SECTION 2: Tag Input (1 tag only - from your current fix)
<div>
  <label className="block mb-2">Tag (1 only)</label>
  <div className="flex gap-2 mb-2">
    <input
      type="text"
      value={tagInput}
      onChange={(e) => setTagInput(e.target.value)}
      placeholder={tags.length >= 1 ? "Tag limit reached" : "Add a tag"}
      className="flex-1 px-3 py-2 border border-input rounded"
      disabled={tags.length >= 1}
    />
    <button
      type="button"
      onClick={handleAddTag}
      className="bg-secondary px-4 py-2 rounded"
      disabled={tags.length >= 1}
    >
      Add
    </button>
  </div>
  {tags.length >= 1 && (
    <p className="text-muted-foreground text-xs">
      Maximum 1 tag allowed. Remove to add a different one.
    </p>
  )}
  {tags.map(tag => (
    <span key={tag} className="inline-flex items-center bg-primary/10 px-3 py-1 rounded-full">
      #{tag}
      <button onClick={() => removeTag(tag)}>
        <X className="w-3 h-3" />
      </button>
    </span>
  ))}
</div>
```

```html
<!-- TO: Django template -->
<div class="form-group">
  <label for="{{ form.tag.id_for_label }}" class="form-label">
    Tag (1 only)
  </label>
  {{ form.tag }}
  <p class="form-help">{{ form.tag.help_text }}</p>
  {% if form.tag.errors %}
    <div class="form-error">{{ form.tag.errors }}</div>
  {% endif %}
</div>
```

**📝 Note:** The tag validation (1 tag only) is handled server-side in Django forms. See **FIGMA_TO_DJANGO_CONVERSION_GUIDE.md** → **Step 6.2**

**📝 Complete Upload template:** See **FIGMA_TO_DJANGO_CONVERSION_GUIDE.md** → **Step 9.3**

---

### Step 3.4: Profile Page

**📂 Source File:** `/components/pages/Profile.tsx`

**✂️ What to Copy:**
1. **Profile header** with avatar and user info
2. **Bio section** (inline editable in React, form-based in Django)
3. **Stats section** (Level, XP, Joined date)
4. **Artworks grid**

**📁 Destination:** `apps/users/templates/users/profile.html` (Django)

**✅ Quick Mapping:**

| React Component Section | Django Template Section | Notes |
|------------------------|------------------------|-------|
| `<div className="w-24 h-24 rounded-full bg-primary">` | `<div class="avatar avatar-lg">` | Avatar with initial |
| `{isEditing ? <textarea> : <p>}` | `<form method="post">{{ form.bio }}</form>` | Django form handles edit |
| `Level {level}` | `Level {{ request.user.profile.level }}` | Dynamic from DB |
| `{xp} XP` | `{{ request.user.profile.xp }} XP` | Dynamic from DB |

---

### Step 3.5: Settings Page

**📂 Source File:** `/components/pages/Settings.tsx`

**✂️ What to Copy:**
1. **Account info section** (name, email, bio)
2. **Dark mode toggle**
3. **Password reset section** (if you have it)

**📁 Destination:** `apps/users/templates/users/settings.html` (Django)

**✅ Key Conversion:**

```jsx
// FROM: components/pages/Settings.tsx
<div className="flex items-center justify-between">
  <div>
    <label className="font-medium">Dark Mode</label>
    <p className="text-sm text-muted-foreground">Enable dark mode</p>
  </div>
  <button
    onClick={onToggleDarkMode}
    className={`relative w-12 h-6 rounded-full ${
      darkMode ? 'bg-primary' : 'bg-gray-300'
    }`}
  >
    <span className={`absolute w-5 h-5 bg-white rounded-full transition-transform ${
      darkMode ? 'translate-x-6' : 'translate-x-1'
    }`} />
  </button>
</div>
```

```html
<!-- TO: Django template -->
<div class="form-group">
  <label class="toggle-label">
    {{ form.dark_mode }}
    <span>Dark Mode</span>
  </label>
  <p class="form-help">Enable dark mode for better viewing at night</p>
</div>
```

**📝 Note:** Django handles the toggle with a checkbox. CSS styles the checkbox as a toggle switch.

---

### Step 3.6: Browse Page

**📂 Source File:** `/components/pages/Browse.tsx`

**✂️ What to Copy:**
1. **Filter sidebar** (category filter)
2. **Artworks grid** (similar to Dashboard)
3. **Like button functionality**

**📁 Destination:** `apps/gallery/templates/gallery/browse.html` (Django)

---

### Step 3.7: Moderation Page

**📂 Source File:** `/components/pages/Moderation.tsx`

**✂️ What to Copy:**
1. **Stats cards** (pending reports, total posts)
2. **Posts table/grid**
3. **Action buttons** (Approve, Remove)

**📁 Destination:** `apps/moderation/templates/moderation/moderation.html` (Django)

---

## Part 4: JavaScript Extraction

### Step 4.1: Dark Mode Toggle

**📂 Source File:** `/App.tsx` (lines 21-29, 74-83)

**✂️ What to Copy:**

```jsx
// FROM: App.tsx
const handleToggleDarkMode = () => {
  const newDarkMode = !darkMode;
  setDarkMode(newDarkMode);
  localStorage.setItem('darkMode', String(newDarkMode));
  
  if (newDarkMode) {
    document.documentElement.classList.add('dark');
  } else {
    document.documentElement.classList.remove('dark');
  }
};
```

**📁 Destination:** `static/js/dark-mode.js` (Django)

```javascript
// TO: static/js/dark-mode.js
document.addEventListener('DOMContentLoaded', function() {
  const darkModeCheckbox = document.getElementById('id_dark_mode');
  
  if (darkModeCheckbox) {
    const isDarkMode = darkModeCheckbox.checked;
    updateDarkMode(isDarkMode);
    
    darkModeCheckbox.addEventListener('change', function() {
      updateDarkMode(this.checked);
    });
  }
});

function updateDarkMode(enabled) {
  if (enabled) {
    document.documentElement.classList.add('dark');
  } else {
    document.documentElement.classList.remove('dark');
  }
}
```

**📝 See:** **FIGMA_TO_DJANGO_CONVERSION_GUIDE.md** → **Step 10.2**

---

### Step 4.2: Image Upload Preview

**📂 Source File:** `/components/pages/Upload.tsx` (lines 71-96)

**✂️ What to Copy:**

```jsx
// FROM: Upload.tsx
const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
  const file = e.target.files?.[0];
  if (!file) return;
  
  if (!file.type.startsWith('image/')) {
    setError('Unsupported file format.');
    return;
  }
  
  if (file.size > 10 * 1024 * 1024) {
    setError('File size exceeds 10MB.');
    return;
  }
  
  setError('');
  setSelectedFile(file);
  
  const reader = new FileReader();
  reader.onloadend = () => {
    setPreviewUrl(reader.result as string);
  };
  reader.readAsDataURL(file);
};
```

**📁 Destination:** `static/js/filters.js` (Django)

```javascript
// TO: static/js/filters.js
imageInput.addEventListener('change', function(e) {
  const file = e.target.files[0];
  if (file) {
    if (!file.type.startsWith('image/')) {
      alert('Please select an image file.');
      return;
    }
    
    if (file.size > 10 * 1024 * 1024) {
      alert('File size exceeds 10MB.');
      return;
    }
    
    const reader = new FileReader();
    reader.onload = function(e) {
      previewImage.src = e.target.result;
      uploadLabel.style.display = 'none';
      previewContainer.style.display = 'block';
    };
    reader.readAsDataURL(file);
  }
});
```

**📝 See:** **FIGMA_TO_DJANGO_CONVERSION_GUIDE.md** → **Step 9.3** → JavaScript section

---

### Step 4.3: Logout Confirmation

**📂 Source File:** `/components/AppHeader.tsx` (logout button click)

**✂️ What to Copy:**

```jsx
// FROM: AppHeader.tsx
<button
  onClick={() => {
    if (confirm('Are you sure you want to logout?')) {
      onLogout();
    }
  }}
  className="flex items-center gap-2"
>
  <LogOut className="w-4 h-4" />
  Logout
</button>
```

**📁 Destination:** `static/js/logout-confirm.js` (Django)

```javascript
// TO: static/js/logout-confirm.js
document.addEventListener('DOMContentLoaded', function() {
  const logoutLinks = document.querySelectorAll('.logout-link');
  
  logoutLinks.forEach(function(link) {
    link.addEventListener('click', function(e) {
      const confirmed = confirm('Are you sure you want to logout?');
      if (!confirmed) {
        e.preventDefault();
      }
    });
  });
});
```

**📝 See:** **FIGMA_TO_DJANGO_CONVERSION_GUIDE.md** → **Step 12.1**

---

## Part 5: SVG Icons Extraction

### Step 5.1: Common Icons to Extract

**📂 Source Files:** All component files using Lucide React icons

**✂️ Icons to Find and Convert:**

| React Icon | SVG Path | Usage |
|-----------|----------|-------|
| `<Search />` | Circle + line | Dashboard search |
| `<Heart />` | Path with curves | Like button |
| `<Share2 />` | Circles + lines | Share button |
| `<Upload />` | Arrow + lines | Upload page |
| `<LayoutGrid />` | Rectangles | Dashboard nav icon |
| `<Image />` | Rectangle + circle + polyline | Browse nav icon |
| `<Star />` | Filled star path | User level |
| `<LogOut />` | Arrow + door | Logout button |

**✅ How to Find SVG Paths:**

1. **Visit:** https://lucide.dev/icons/
2. **Search:** for the icon name (e.g., "heart")
3. **Click:** "Copy SVG"
4. **Paste:** into Django template

**Example:**

```jsx
// FROM: React component
import { Heart } from 'lucide-react';
<Heart className="w-4 h-4" />
```

```html
<!-- TO: Django template -->
<svg class="icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
  <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path>
</svg>
```

---

## Part 6: Verification Checklist

### ✅ CSS Files Created

- [ ] `static/css/variables.css` - All color and spacing variables
- [ ] `static/css/base.css` - Typography and reset styles
- [ ] `static/css/components.css` - Button, form, card styles
- [ ] `static/css/layout.css` - Header, sidebar, main layout
- [ ] `static/css/dark-mode.css` - Dark mode overrides
- [ ] `static/css/pages/login.css` - Login page styles
- [ ] `static/css/pages/dashboard.css` - Dashboard page styles
- [ ] `static/css/pages/upload.css` - Upload page styles

### ✅ Template Files Created

- [ ] `templates/base.html` - Base layout with header/sidebar
- [ ] `templates/includes/header.html` - Top navigation
- [ ] `templates/includes/sidebar.html` - Side navigation
- [ ] `apps/users/templates/users/login.html`
- [ ] `apps/users/templates/users/register.html`
- [ ] `apps/users/templates/users/profile.html`
- [ ] `apps/users/templates/users/settings.html`
- [ ] `apps/gallery/templates/gallery/dashboard.html`
- [ ] `apps/gallery/templates/gallery/browse.html`
- [ ] `apps/gallery/templates/gallery/upload.html`

### ✅ JavaScript Files Created

- [ ] `static/js/main.js` - General utilities (dropdown toggle)
- [ ] `static/js/dark-mode.js` - Dark mode toggle
- [ ] `static/js/logout-confirm.js` - Logout confirmation
- [ ] `static/js/filters.js` - Image preview and filters

### ✅ Content Extracted

- [ ] All color values from `styles/globals.css`
- [ ] Typography styles from `styles/globals.css`
- [ ] Header structure from `components/AppHeader.tsx`
- [ ] Sidebar structure from `components/Sidebar.tsx`
- [ ] Login form from `components/pages/Login.tsx`
- [ ] Dashboard layout from `components/pages/Dashboard.tsx`
- [ ] Upload form from `components/pages/Upload.tsx`
- [ ] Profile layout from `components/pages/Profile.tsx`
- [ ] Settings form from `components/pages/Settings.tsx`
- [ ] All SVG icons converted from Lucide React

---

## Quick Start Summary

**To convert your prototype to Django:**

1. **Start with CSS:** Extract from `styles/globals.css` → Create Django CSS files
2. **Create Templates:** Convert component JSX → Django HTML templates
3. **Add JavaScript:** Extract client-side logic → Create Django JS files
4. **Replace Dynamic Values:** `{user.username}` → `{{ request.user.username }}`
5. **Add Django Tags:** `href="/dashboard"` → `href="{% url 'gallery:dashboard' %}"`
6. **Test Each Page:** Verify styling matches prototype

**Follow this order:**
1. CSS files (variables, base, components, layout)
2. Base template + header + sidebar
3. Login page (simplest, test auth)
4. Dashboard page (test with real data)
5. Upload page (test forms and file upload)
6. Profile page
7. Settings page (test dark mode)
8. Browse and Moderation pages

---

## Need Help?

- **For complete template code:** See `FIGMA_TO_DJANGO_CONVERSION_GUIDE.md` Step 9
- **For CSS examples:** See `FIGMA_TO_DJANGO_CONVERSION_GUIDE.md` Step 2
- **For Django models:** See `FIGMA_TO_DJANGO_CONVERSION_GUIDE.md` Step 5
- **For Django forms:** See `FIGMA_TO_DJANGO_CONVERSION_GUIDE.md` Step 6
- **For Django views:** See `FIGMA_TO_DJANGO_CONVERSION_GUIDE.md` Step 7

**This extraction guide is your roadmap. Start with Part 1 (CSS) and work your way through!** 🚀
