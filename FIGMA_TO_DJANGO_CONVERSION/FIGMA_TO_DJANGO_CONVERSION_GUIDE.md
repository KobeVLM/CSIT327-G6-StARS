# STARS: Student Artist Space
## Figma-to-Django Conversion Manual

---

## Table of Contents

1. [Introduction](#introduction)
2. [Project Structure Overview](#project-structure-overview)
3. [Step 1: Setting Up Django Project](#step-1-setting-up-django-project)
4. [Step 2: Exporting Visual Assets from Figma Prototype](#step-2-exporting-visual-assets-from-figma-prototype)
5. [Step 3: Organizing Static Files](#step-3-organizing-static-files)
6. [Step 4: Creating Reusable Template Structure](#step-4-creating-reusable-template-structure)
7. [Step 5: Creating Django Models](#step-5-creating-django-models)
8. [Step 6: Creating Django Forms](#step-6-creating-django-forms)
9. [Step 7: Creating Django Views](#step-7-creating-django-views)
10. [Step 8: URL Configuration](#step-8-url-configuration)
11. [Step 9: Converting Each Page](#step-9-converting-each-page)
12. [Step 10: Implementing Dark Mode](#step-10-implementing-dark-mode)
13. [Step 11: Implementing Search Functionality](#step-11-implementing-search-functionality)
14. [Step 12: Implementing Logout Confirmation](#step-12-implementing-logout-confirmation)
15. [Best Practices and Tips](#best-practices-and-tips)
16. [Deployment Checklist](#deployment-checklist)

---

## Introduction

This guide will help you convert the STARS (Student Artist Space) Figma prototype into a fully functional Django web application using **only Django's built-in tools**. We will not use any external CSS frameworks (like Tailwind or Bootstrap) or JavaScript frameworks (like React or Vue). Instead, we'll rely on:

- **Django Templates** for rendering HTML
- **Django Models** for database structure
- **Django Forms** for user input validation
- **Django Views** for business logic
- **Static Files** for CSS, JavaScript, and images
- **Django's built-in authentication system**

The STARS application is organized into four main Django apps:

1. **users** - Authentication, profiles, settings
2. **gallery** - Dashboard, browse, upload, posts
3. **gamification** - Badges, rewards, XP, levels
4. **moderation** - Admin functions, content moderation

---

## Project Structure Overview

Here's the recommended Django project structure:

```
stars_project/
├── manage.py
├── stars_project/              # Main project folder
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── apps/                       # All Django apps
│   ├── __init__.py
│   │
│   ├── users/                  # Authentication & User Management
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py           # User, Profile models
│   │   ├── forms.py            # Login, Register, Settings forms
│   │   ├── views.py            # Auth views
│   │   ├── urls.py
│   │   ├── migrations/
│   │   └── templates/
│   │       └── users/
│   │           ├── login.html
│   │           ├── register.html
│   │           ├── admin_login.html
│   │           ├── profile.html
│   │           └── settings.html
│   │
│   ├── gallery/                # Posts, Upload, Browse
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py           # Post, Category, Tag models
│   │   ├── forms.py            # Upload, Filter forms
│   │   ├── views.py            # Gallery views
│   │   ├── urls.py
│   │   ├── migrations/
│   │   └── templates/
│   │       └── gallery/
│   │           ├── dashboard.html
│   │           ├── browse.html
│   │           └── upload.html
│   │
│   ├── gamification/           # Badges, XP, Rewards
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py           # Badge, Reward, UserProgress models
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── migrations/
│   │   └── templates/
│   │       └── gamification/
│   │           └── badges.html
│   │
│   └── moderation/             # Admin Moderation
│       ├── __init__.py
│       ├── admin.py
│       ├── apps.py
│       ├── models.py           # ModerationLog, Report models
│       ├── views.py
│       ├── urls.py
│       ├── migrations/
│       └── templates/
│           └── moderation/
│               └── moderation.html
│
├── static/                     # Static files (collected)
│   ├── css/
│   │   ├── base.css            # Core styles
│   │   ├── variables.css       # CSS custom properties
│   │   ├── components.css      # Reusable component styles
│   │   ├── pages/              # Page-specific styles
│   │   │   ├── login.css
│   │   │   ├── dashboard.css
│   │   │   ├── browse.css
│   │   │   └── ...
│   │   └── dark-mode.css       # Dark mode overrides
│   │
│   ├── js/
│   │   ├── main.js             # General utilities
│   │   ├── dark-mode.js        # Dark mode toggle
│   │   ├── logout-confirm.js   # Logout confirmation
│   │   └── filters.js          # Image filter preview
│   │
│   └── images/
│       ├── logo.png
│       ├── placeholder.jpg
│       └── icons/
│
├── media/                      # User-uploaded files
│   ├── posts/                  # Artwork uploads
│   └── avatars/                # Profile pictures
│
└── templates/                  # Global templates
    ├── base.html               # Base layout
    ├── includes/
    │   ├── header.html         # Top navigation bar
    │   ├── sidebar.html        # Side navigation
    │   └── footer.html         # Footer (if needed)
    └── errors/
        ├── 404.html
        └── 500.html
```

---

## Step 1: Setting Up Django Project

### 1.1 Create Virtual Environment and Install Django

```bash
# Create project directory
mkdir stars_project
cd stars_project

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install Django
pip install django pillow  # Pillow for image handling

# Create requirements.txt
pip freeze > requirements.txt
```

### 1.2 Start Django Project

```bash
# Create Django project
django-admin startproject stars_project .

# Create apps directory
mkdir apps
touch apps/__init__.py

# Create Django apps
cd apps
django-admin startapp users
django-admin startapp gallery
django-admin startapp gamification
django-admin startapp moderation
cd ..
```

### 1.3 Configure settings.py

Edit `stars_project/settings.py`:

```python
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Add apps to INSTALLED_APPS
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Custom apps
    'apps.users',
    'apps.gallery',
    'apps.gamification',
    'apps.moderation',
]

# Template settings
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Global templates
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
            ],
        },
    },
]

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Media files (user uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Authentication
LOGIN_URL = 'users:login'
LOGIN_REDIRECT_URL = 'gallery:dashboard'
LOGOUT_REDIRECT_URL = 'users:login'

# Custom user model (optional but recommended)
# AUTH_USER_MODEL = 'users.CustomUser'
```

### 1.4 Create Directory Structure

```bash
# Create template directories
mkdir -p templates/includes
mkdir -p templates/errors
mkdir -p apps/users/templates/users
mkdir -p apps/gallery/templates/gallery
mkdir -p apps/gamification/templates/gamification
mkdir -p apps/moderation/templates/moderation

# Create static directories
mkdir -p static/css/pages
mkdir -p static/js
mkdir -p static/images/icons

# Create media directories
mkdir -p media/posts
mkdir -p media/avatars
```

---

## Step 2: Exporting Visual Assets from Figma Prototype

The current prototype is built with React and Tailwind CSS. To convert it to plain HTML/CSS for Django:

### 2.1 Understanding the Current Structure

Your prototype uses:
- **Tailwind utility classes** → Need to convert to custom CSS
- **React components** → Need to convert to Django templates
- **State management** → Need to convert to Django sessions/database
- **Client-side routing** → Need to convert to Django URLs

### 2.2 Converting Tailwind Classes to Custom CSS

#### Extract Color Variables

From `styles/globals.css`, extract the CSS custom properties:

**Create: `static/css/variables.css`**

```css
:root {
  /* Colors */
  --color-primary: #5865F2;
  --color-primary-foreground: #ffffff;
  --color-secondary: #E8EAF6;
  --color-secondary-foreground: #2C3E50;
  --color-background: #F5F7FB;
  --color-foreground: #2C3E50;
  --color-card: #ffffff;
  --color-border: #E0E4EB;
  --color-input: #E0E4EB;
  --color-input-background: #ffffff;
  --color-muted: #F5F7FB;
  --color-muted-foreground: #7C8AA0;
  --color-destructive: #EF4444;
  --color-success: #10B981;
  
  /* Spacing */
  --spacing-xs: 0.25rem;   /* 4px */
  --spacing-sm: 0.5rem;    /* 8px */
  --spacing-md: 1rem;      /* 16px */
  --spacing-lg: 1.5rem;    /* 24px */
  --spacing-xl: 2rem;      /* 32px */
  --spacing-2xl: 3rem;     /* 48px */
  
  /* Border radius */
  --radius-sm: 0.25rem;    /* 4px */
  --radius-md: 0.5rem;     /* 8px */
  --radius-lg: 0.75rem;    /* 12px */
  --radius-xl: 1rem;       /* 16px */
  --radius-full: 9999px;
  
  /* Font sizes */
  --font-xs: 0.75rem;      /* 12px */
  --font-sm: 0.875rem;     /* 14px */
  --font-base: 1rem;       /* 16px */
  --font-lg: 1.125rem;     /* 18px */
  --font-xl: 1.25rem;      /* 20px */
  --font-2xl: 1.5rem;      /* 24px */
  --font-3xl: 1.75rem;     /* 28px */
  
  /* Font weights */
  --font-normal: 400;
  --font-medium: 500;
  --font-semibold: 600;
  --font-bold: 700;
  
  /* Shadows */
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.1);
  --shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.1);
  --shadow-xl: 0 20px 25px rgba(0, 0, 0, 0.15);
}

/* Dark mode colors */
.dark {
  --color-background: #1a1d2e;
  --color-foreground: #e4e7eb;
  --color-card: #252938;
  --color-border: #3d4157;
  --color-input: #3d4157;
  --color-input-background: #252938;
  --color-secondary: #2d3148;
  --color-secondary-foreground: #e4e7eb;
  --color-muted: #1f2231;
  --color-muted-foreground: #9ca3af;
}
```

#### Create Base Styles

**Create: `static/css/base.css`**

```css
/* Import variables */
@import url('variables.css');

/* Reset and base styles */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html {
  font-size: 16px;
  scroll-behavior: smooth;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background-color: var(--color-background);
  color: var(--color-foreground);
  line-height: 1.5;
}

/* Typography */
h1 {
  font-size: var(--font-3xl);
  font-weight: var(--font-semibold);
  color: var(--color-foreground);
  margin-bottom: var(--spacing-md);
}

h2 {
  font-size: var(--font-2xl);
  font-weight: var(--font-semibold);
  color: var(--color-foreground);
  margin-bottom: var(--spacing-md);
}

h3 {
  font-size: var(--font-xl);
  font-weight: var(--font-medium);
  color: var(--color-foreground);
  margin-bottom: var(--spacing-sm);
}

h4 {
  font-size: var(--font-lg);
  font-weight: var(--font-medium);
  color: var(--color-foreground);
  margin-bottom: var(--spacing-sm);
}

p {
  font-size: var(--font-base);
  font-weight: var(--font-normal);
  color: var(--color-foreground);
  line-height: 1.6;
  margin-bottom: var(--spacing-md);
}

/* Links */
a {
  color: var(--color-primary);
  text-decoration: none;
  transition: color 0.2s;
}

a:hover {
  color: var(--color-primary);
  opacity: 0.8;
}

/* Images */
img {
  max-width: 100%;
  height: auto;
  display: block;
}

/* Lists */
ul, ol {
  list-style: none;
}
```

#### Create Component Styles

**Create: `static/css/components.css`**

```css
/* Buttons */
.btn {
  display: inline-block;
  padding: 0.625rem 1.5rem;
  font-size: var(--font-sm);
  font-weight: var(--font-medium);
  text-align: center;
  border-radius: var(--radius-md);
  border: none;
  cursor: pointer;
  transition: all 0.2s;
  text-decoration: none;
}

.btn-primary {
  background-color: var(--color-primary);
  color: var(--color-primary-foreground);
}

.btn-primary:hover {
  opacity: 0.9;
}

.btn-secondary {
  background-color: var(--color-secondary);
  color: var(--color-secondary-foreground);
}

.btn-secondary:hover {
  opacity: 0.8;
}

.btn-outline {
  background-color: var(--color-card);
  color: var(--color-foreground);
  border: 1px solid var(--color-border);
}

.btn-outline:hover {
  background-color: var(--color-secondary);
}

.btn-destructive {
  background-color: var(--color-destructive);
  color: white;
}

.btn-destructive:hover {
  opacity: 0.9;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Form Controls */
.form-group {
  margin-bottom: var(--spacing-lg);
}

.form-label {
  display: block;
  font-size: var(--font-sm);
  font-weight: var(--font-medium);
  color: var(--color-foreground);
  margin-bottom: var(--spacing-sm);
}

.form-input,
.form-textarea,
.form-select {
  width: 100%;
  padding: 0.625rem 0.75rem;
  font-size: var(--font-sm);
  color: var(--color-foreground);
  background-color: var(--color-input-background);
  border: 1px solid var(--color-input);
  border-radius: var(--radius-md);
  outline: none;
  transition: border-color 0.2s;
}

.form-input:focus,
.form-textarea:focus,
.form-select:focus {
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(88, 101, 242, 0.1);
}

.form-input:disabled,
.form-textarea:disabled,
.form-select:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.form-textarea {
  resize: vertical;
  min-height: 100px;
}

.form-error {
  color: var(--color-destructive);
  font-size: var(--font-sm);
  margin-top: var(--spacing-xs);
}

.form-help {
  color: var(--color-muted-foreground);
  font-size: var(--font-xs);
  margin-top: var(--spacing-xs);
}

/* Cards */
.card {
  background-color: var(--color-card);
  border-radius: var(--radius-lg);
  padding: var(--spacing-lg);
  box-shadow: var(--shadow-sm);
  transition: box-shadow 0.2s;
}

.card:hover {
  box-shadow: var(--shadow-md);
}

.card-header {
  margin-bottom: var(--spacing-md);
}

.card-title {
  font-size: var(--font-lg);
  font-weight: var(--font-semibold);
  color: var(--color-foreground);
  margin-bottom: var(--spacing-xs);
}

.card-description {
  font-size: var(--font-sm);
  color: var(--color-muted-foreground);
}

/* Alerts */
.alert {
  padding: var(--spacing-md);
  border-radius: var(--radius-md);
  margin-bottom: var(--spacing-md);
  display: flex;
  align-items: flex-start;
  gap: var(--spacing-sm);
}

.alert-success {
  background-color: rgba(16, 185, 129, 0.1);
  color: var(--color-success);
  border: 1px solid rgba(16, 185, 129, 0.2);
}

.alert-error {
  background-color: rgba(239, 68, 68, 0.1);
  color: var(--color-destructive);
  border: 1px solid rgba(239, 68, 68, 0.2);
}

.alert-info {
  background-color: rgba(88, 101, 242, 0.1);
  color: var(--color-primary);
  border: 1px solid rgba(88, 101, 242, 0.2);
}

/* Badge/Tag */
.badge {
  display: inline-flex;
  align-items: center;
  padding: 0.25rem 0.75rem;
  font-size: var(--font-xs);
  font-weight: var(--font-medium);
  border-radius: var(--radius-full);
  white-space: nowrap;
}

.badge-primary {
  background-color: rgba(88, 101, 242, 0.1);
  color: var(--color-primary);
}

.badge-secondary {
  background-color: var(--color-secondary);
  color: var(--color-secondary-foreground);
}

.badge-success {
  background-color: rgba(16, 185, 129, 0.1);
  color: var(--color-success);
}

/* Avatar */
.avatar {
  width: 40px;
  height: 40px;
  border-radius: var(--radius-full);
  background-color: var(--color-primary);
  color: var(--color-primary-foreground);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: var(--font-semibold);
  font-size: var(--font-sm);
}

.avatar-lg {
  width: 96px;
  height: 96px;
  font-size: var(--font-2xl);
}

/* Utility classes */
.container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 var(--spacing-md);
}

.flex {
  display: flex;
}

.flex-column {
  flex-direction: column;
}

.items-center {
  align-items: center;
}

.justify-between {
  justify-content: space-between;
}

.gap-sm {
  gap: var(--spacing-sm);
}

.gap-md {
  gap: var(--spacing-md);
}

.gap-lg {
  gap: var(--spacing-lg);
}

.text-center {
  text-align: center;
}

.text-muted {
  color: var(--color-muted-foreground);
}

.mb-0 { margin-bottom: 0; }
.mb-sm { margin-bottom: var(--spacing-sm); }
.mb-md { margin-bottom: var(--spacing-md); }
.mb-lg { margin-bottom: var(--spacing-lg); }
.mb-xl { margin-bottom: var(--spacing-xl); }

.mt-0 { margin-top: 0; }
.mt-sm { margin-top: var(--spacing-sm); }
.mt-md { margin-top: var(--spacing-md); }
.mt-lg { margin-top: var(--spacing-lg); }
.mt-xl { margin-top: var(--spacing-xl); }

/* Grid */
.grid {
  display: grid;
  gap: var(--spacing-md);
}

.grid-cols-2 {
  grid-template-columns: repeat(2, 1fr);
}

.grid-cols-3 {
  grid-template-columns: repeat(3, 1fr);
}

.grid-cols-4 {
  grid-template-columns: repeat(4, 1fr);
}

/* Responsive */
@media (max-width: 768px) {
  .grid-cols-2,
  .grid-cols-3,
  .grid-cols-4 {
    grid-template-columns: 1fr;
  }
}
```

### 2.3 Converting React Components to HTML

#### Example: Converting Button Component

**React/Tailwind (original):**
```jsx
<button 
  className="bg-primary text-white px-6 py-2.5 rounded hover:opacity-90"
  onClick={handleClick}
>
  Upload Artwork
</button>
```

**Plain HTML/CSS (Django-ready):**
```html
<button class="btn btn-primary" type="submit">
  Upload Artwork
</button>
```

#### Example: Converting Card Component

**React/Tailwind (original):**
```jsx
<div className="bg-white rounded-lg p-6 shadow-sm">
  <h3 className="text-lg font-semibold mb-2">Card Title</h3>
  <p className="text-sm text-muted-foreground">Description</p>
</div>
```

**Plain HTML/CSS (Django-ready):**
```html
<div class="card">
  <div class="card-header">
    <h3 class="card-title">Card Title</h3>
    <p class="card-description">Description</p>
  </div>
</div>
```

---

## Step 3: Organizing Static Files

### 3.1 CSS File Organization

Place these files in `static/css/`:

1. **variables.css** - CSS custom properties (colors, spacing, etc.)
2. **base.css** - Reset and base typography
3. **components.css** - Reusable component styles
4. **layout.css** - Layout-specific styles (header, sidebar, main)
5. **dark-mode.css** - Dark mode overrides
6. **pages/** directory - Page-specific styles

### 3.2 JavaScript File Organization

Place these files in `static/js/`:

1. **main.js** - General utilities
2. **dark-mode.js** - Dark mode toggle functionality
3. **logout-confirm.js** - Logout confirmation dialog
4. **filters.js** - Image filter preview for upload page
5. **search.js** - Search functionality

### 3.3 Image Organization

Place images in `static/images/`:

```
static/images/
├── logo.png                 # STARS logo
├── placeholder.jpg          # Placeholder for missing images
├── icons/                   # SVG icons
│   ├── heart.svg
│   ├── share.svg
│   ├── upload.svg
│   └── ...
└── sample-posts/           # Sample artwork for demo
    ├── post1.jpg
    ├── post2.jpg
    └── ...
```

**Note:** User-uploaded files go in `media/`, not `static/`.

---

## Step 4: Creating Reusable Template Structure

### 4.1 Base Template

**Create: `templates/base.html`**

This is the master template that all other pages will extend.

```html
{% load static %}
<!DOCTYPE html>
<html lang="en" class="{% if request.user.is_authenticated and request.user.profile.dark_mode %}dark{% endif %}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}STARS - Student Artist Space{% endblock %}</title>
    
    <!-- CSS Files -->
    <link rel="stylesheet" href="{% static 'css/variables.css' %}">
    <link rel="stylesheet" href="{% static 'css/base.css' %}">
    <link rel="stylesheet" href="{% static 'css/components.css' %}">
    <link rel="stylesheet" href="{% static 'css/layout.css' %}">
    <link rel="stylesheet" href="{% static 'css/dark-mode.css' %}">
    
    {% block extra_css %}{% endblock %}
</head>
<body>
    {% if request.user.is_authenticated %}
        <!-- Include header for authenticated users -->
        {% include 'includes/header.html' %}
        
        <div class="app-container">
            <!-- Include sidebar for authenticated users -->
            {% include 'includes/sidebar.html' %}
            
            <!-- Main content area -->
            <main class="main-content">
                {% block content %}{% endblock %}
            </main>
        </div>
    {% else %}
        <!-- No header/sidebar for unauthenticated users -->
        <main class="auth-page">
            {% block content %}{% endblock %}
        </main>
    {% endif %}
    
    <!-- JavaScript Files -->
    <script src="{% static 'js/main.js' %}"></script>
    {% if request.user.is_authenticated %}
        <script src="{% static 'js/dark-mode.js' %}"></script>
        <script src="{% static 'js/logout-confirm.js' %}"></script>
    {% endif %}
    
    {% block extra_js %}{% endblock %}
</body>
</html>
```

### 4.2 Header Template

**Create: `templates/includes/header.html`**

```html
{% load static %}
<header class="app-header">
    <div class="header-content">
        <!-- Logo -->
        <div class="header-logo">
            <a href="{% url 'gallery:dashboard' %}">
                <img src="{% static 'images/logo.png' %}" alt="STARS" class="logo-image">
                <span class="logo-text">STARS</span>
            </a>
        </div>
        
        <!-- Right side: User info -->
        <div class="header-right">
            <!-- User level and XP -->
            <div class="user-stats">
                <span class="user-level">
                    <svg class="icon icon-star" width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
                    </svg>
                    Level {{ request.user.profile.level }}
                </span>
                <span class="user-xp">{{ request.user.profile.xp }} XP</span>
            </div>
            
            <!-- User dropdown -->
            <div class="user-dropdown">
                <button class="user-button" id="user-menu-button">
                    <div class="avatar">
                        {{ request.user.first_name|first|default:request.user.username|first|upper }}
                    </div>
                    <span class="username">{{ request.user.username }}</span>
                    <svg class="icon icon-chevron" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                        <polyline points="6 9 12 15 18 9"></polyline>
                    </svg>
                </button>
                
                <!-- Dropdown menu (hidden by default) -->
                <div class="dropdown-menu" id="user-menu" style="display: none;">
                    <a href="{% url 'users:profile' %}" class="dropdown-item">
                        <svg class="icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                            <circle cx="12" cy="7" r="4"></circle>
                        </svg>
                        Profile
                    </a>
                    <a href="{% url 'users:settings' %}" class="dropdown-item">
                        <svg class="icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                            <circle cx="12" cy="12" r="3"></circle>
                            <path d="M12 1v6m0 6v6m-5-13l4.33 7.5m4.34 7.5L11.67 13M1 12h6m6 0h6"></path>
                        </svg>
                        Settings
                    </a>
                    <div class="dropdown-divider"></div>
                    <a href="{% url 'users:logout' %}" class="dropdown-item logout-link">
                        <svg class="icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                            <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
                            <polyline points="16 17 21 12 16 7"></polyline>
                            <line x1="21" y1="12" x2="9" y2="12"></line>
                        </svg>
                        Logout
                    </a>
                </div>
            </div>
        </div>
    </div>
</header>
```

### 4.3 Sidebar Template

**Create: `templates/includes/sidebar.html`**

```html
{% load static %}
<aside class="sidebar">
    <!-- User Profile Section -->
    <div class="sidebar-profile">
        <div class="avatar avatar-lg">
            {{ request.user.first_name|first|default:request.user.username|first|upper }}
        </div>
        <h3 class="profile-name">{{ request.user.get_full_name|default:request.user.username }}</h3>
        <p class="profile-email">@{{ request.user.username }}</p>
    </div>
    
    <!-- Navigation Menu -->
    <nav class="sidebar-nav">
        <a href="{% url 'gallery:dashboard' %}" 
           class="nav-item {% if request.resolver_match.url_name == 'dashboard' %}active{% endif %}">
            <svg class="nav-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <rect x="3" y="3" width="7" height="7"></rect>
                <rect x="14" y="3" width="7" height="7"></rect>
                <rect x="14" y="14" width="7" height="7"></rect>
                <rect x="3" y="14" width="7" height="7"></rect>
            </svg>
            Dashboard
        </a>
        
        <a href="{% url 'gallery:browse' %}" 
           class="nav-item {% if request.resolver_match.url_name == 'browse' %}active{% endif %}">
            <svg class="nav-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
                <circle cx="8.5" cy="8.5" r="1.5"></circle>
                <polyline points="21 15 16 10 5 21"></polyline>
            </svg>
            Browse
        </a>
        
        <a href="{% url 'gallery:upload' %}" 
           class="nav-item {% if request.resolver_match.url_name == 'upload' %}active{% endif %}">
            <svg class="nav-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                <polyline points="17 8 12 3 7 8"></polyline>
                <line x1="12" y1="3" x2="12" y2="15"></line>
            </svg>
            Upload
        </a>
        
        <a href="{% url 'users:profile' %}" 
           class="nav-item {% if request.resolver_match.url_name == 'profile' %}active{% endif %}">
            <svg class="nav-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                <circle cx="12" cy="7" r="4"></circle>
            </svg>
            Profile
        </a>
        
        <a href="{% url 'gamification:badges' %}" 
           class="nav-item {% if request.resolver_match.url_name == 'badges' %}active{% endif %}">
            <svg class="nav-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M12 15l-3 6v-6H6l6-9 6 9h-3v6z"></path>
            </svg>
            Badges
        </a>
        
        {% if request.user.is_staff or request.user.profile.is_moderator %}
        <a href="{% url 'moderation:dashboard' %}" 
           class="nav-item {% if request.resolver_match.url_name == 'moderation' %}active{% endif %}">
            <svg class="nav-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
            </svg>
            Moderation
        </a>
        {% endif %}
        
        <a href="{% url 'users:settings' %}" 
           class="nav-item {% if request.resolver_match.url_name == 'settings' %}active{% endif %}">
            <svg class="nav-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <circle cx="12" cy="12" r="3"></circle>
                <path d="M12 1v6m0 6v6m-5-13l4.33 7.5m4.34 7.5L11.67 13M1 12h6m6 0h6"></path>
            </svg>
            Settings
        </a>
    </nav>
    
    <!-- Stats Section -->
    <div class="sidebar-stats">
        <h4>Your Stats</h4>
        <div class="stat-item">
            <span class="stat-label">Artworks Created</span>
            <span class="stat-value">{{ request.user.profile.artwork_count }}</span>
        </div>
        <div class="stat-item">
            <span class="stat-label">Total XP</span>
            <span class="stat-value">{{ request.user.profile.xp }}</span>
        </div>
        <div class="stat-item">
            <span class="stat-label">Badges Earned</span>
            <span class="stat-value">{{ request.user.profile.badge_count }}</span>
        </div>
    </div>
</aside>
```

### 4.4 Layout CSS

**Create: `static/css/layout.css`**

```css
/* App Container */
.app-container {
  display: flex;
  min-height: 100vh;
  padding-top: 64px; /* Height of header */
}

/* Header */
.app-header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 64px;
  background-color: var(--color-card);
  border-bottom: 1px solid var(--color-border);
  z-index: 100;
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 100%;
  padding: 0 var(--spacing-lg);
}

.header-logo {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.logo-image {
  height: 32px;
  width: auto;
}

.logo-text {
  font-size: var(--font-xl);
  font-weight: var(--font-bold);
  color: var(--color-primary);
}

.header-right {
  display: flex;
  align-items: center;
  gap: var(--spacing-lg);
}

.user-stats {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  padding-right: var(--spacing-md);
  border-right: 1px solid var(--color-border);
}

.user-level,
.user-xp {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  font-size: var(--font-sm);
  font-weight: var(--font-medium);
}

.user-level {
  color: #F59E0B; /* Yellow for level */
}

.user-xp {
  color: var(--color-primary);
}

.icon-star {
  color: #F59E0B;
}

/* User Dropdown */
.user-dropdown {
  position: relative;
}

.user-button {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  background: none;
  border: none;
  cursor: pointer;
  padding: var(--spacing-xs) var(--spacing-sm);
  border-radius: var(--radius-md);
  transition: background-color 0.2s;
}

.user-button:hover {
  background-color: var(--color-secondary);
}

.username {
  font-size: var(--font-sm);
  font-weight: var(--font-medium);
  color: var(--color-foreground);
}

.dropdown-menu {
  position: absolute;
  top: calc(100% + var(--spacing-xs));
  right: 0;
  min-width: 200px;
  background-color: var(--color-card);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-lg);
  padding: var(--spacing-xs);
  z-index: 1000;
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-sm) var(--spacing-md);
  font-size: var(--font-sm);
  color: var(--color-foreground);
  text-decoration: none;
  border-radius: var(--radius-sm);
  transition: background-color 0.2s;
}

.dropdown-item:hover {
  background-color: var(--color-secondary);
}

.dropdown-divider {
  height: 1px;
  background-color: var(--color-border);
  margin: var(--spacing-xs) 0;
}

/* Sidebar */
.sidebar {
  position: fixed;
  top: 64px;
  left: 0;
  width: 280px;
  height: calc(100vh - 64px);
  background-color: var(--color-card);
  border-right: 1px solid var(--color-border);
  overflow-y: auto;
  padding: var(--spacing-lg);
}

.sidebar-profile {
  text-align: center;
  padding-bottom: var(--spacing-lg);
  border-bottom: 1px solid var(--color-border);
  margin-bottom: var(--spacing-lg);
}

.profile-name {
  font-size: var(--font-lg);
  font-weight: var(--font-semibold);
  margin-top: var(--spacing-md);
  margin-bottom: var(--spacing-xs);
}

.profile-email {
  font-size: var(--font-sm);
  color: var(--color-muted-foreground);
  margin: 0;
}

/* Sidebar Navigation */
.sidebar-nav {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
  margin-bottom: var(--spacing-xl);
}

.nav-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-sm) var(--spacing-md);
  font-size: var(--font-sm);
  font-weight: var(--font-medium);
  color: var(--color-foreground);
  text-decoration: none;
  border-radius: var(--radius-md);
  transition: background-color 0.2s;
}

.nav-item:hover {
  background-color: var(--color-secondary);
}

.nav-item.active {
  background-color: var(--color-primary);
  color: var(--color-primary-foreground);
}

.nav-icon {
  width: 20px;
  height: 20px;
  stroke-width: 2;
}

/* Sidebar Stats */
.sidebar-stats {
  padding-top: var(--spacing-lg);
  border-top: 1px solid var(--color-border);
}

.sidebar-stats h4 {
  font-size: var(--font-sm);
  font-weight: var(--font-semibold);
  margin-bottom: var(--spacing-md);
}

.stat-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-sm) 0;
}

.stat-label {
  font-size: var(--font-xs);
  color: var(--color-muted-foreground);
}

.stat-value {
  font-size: var(--font-sm);
  font-weight: var(--font-semibold);
  color: var(--color-primary);
}

/* Main Content */
.main-content {
  margin-left: 280px; /* Width of sidebar */
  flex: 1;
  padding: var(--spacing-xl);
  overflow-y: auto;
}

/* Auth Pages (no sidebar) */
.auth-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-lg);
}

/* Responsive */
@media (max-width: 768px) {
  .sidebar {
    width: 0;
    padding: 0;
    overflow: hidden;
  }
  
  .main-content {
    margin-left: 0;
  }
  
  .header-content {
    padding: 0 var(--spacing-md);
  }
  
  .user-stats {
    display: none;
  }
}
```

---

## Step 5: Creating Django Models

Now we'll create the database models for each app based on the ERD structure.

### 5.1 Users App Models

**Edit: `apps/users/models.py`**

```python
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    """Extended user profile with gamification features"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    
    # Gamification fields
    xp = models.IntegerField(default=0)  # Experience points
    level = models.IntegerField(default=1)  # User level
    
    # Stats
    artwork_count = models.IntegerField(default=0)
    badge_count = models.IntegerField(default=0)
    
    # Settings
    dark_mode = models.BooleanField(default=False)
    is_moderator = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s profile"
    
    def calculate_level(self):
        """Calculate level based on XP (every 200 XP = 1 level)"""
        return (self.xp // 200) + 1
    
    def add_xp(self, amount):
        """Add XP and update level"""
        self.xp += amount
        old_level = self.level
        self.level = self.calculate_level()
        self.save()
        
        # Return True if leveled up
        return self.level > old_level

# Create profile automatically when user is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
```

### 5.2 Gallery App Models

**Edit: `apps/gallery/models.py`**

```python
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class Category(models.Model):
    """Art categories"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Tag(models.Model):
    """Tags for posts"""
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"#{self.name}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Post(models.Model):
    """Artwork posts"""
    VISIBILITY_CHOICES = [
        ('public', 'Public'),
        ('private', 'Private'),
    ]
    
    FILTER_CHOICES = [
        ('none', 'Original'),
        ('grayscale', 'Grayscale'),
        ('sepia', 'Sepia'),
        ('brightness', 'Bright'),
        ('contrast', 'Contrast'),
        ('vintage', 'Vintage'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='posts/')
    
    # Image filter applied
    filter_applied = models.CharField(max_length=20, choices=FILTER_CHOICES, default='none')
    
    # Categorization
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='posts')
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts')
    
    # Visibility
    visibility = models.CharField(max_length=10, choices=VISIBILITY_CHOICES, default='public')
    
    # Stats
    like_count = models.IntegerField(default=0)
    share_count = models.IntegerField(default=0)
    view_count = models.IntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} by {self.user.username}"

class Like(models.Model):
    """Track likes on posts"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'post')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} likes {self.post.title}"

class Share(models.Model):
    """Track shares of posts"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shares')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='shares')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} shared {self.post.title}"
```

### 5.3 Gamification App Models

**Edit: `apps/gamification/models.py`**

```python
from django.db import models
from django.contrib.auth.models import User

class Badge(models.Model):
    """Achievement badges"""
    TIER_CHOICES = [
        ('bronze', 'Bronze'),
        ('silver', 'Silver'),
        ('gold', 'Gold'),
        ('platinum', 'Platinum'),
    ]
    
    name = models.CharField(max_length=100)
    description = models.TextField()
    tier = models.CharField(max_length=20, choices=TIER_CHOICES, default='bronze')
    icon = models.CharField(max_length=50, help_text="Icon name or emoji")
    
    # Requirements
    xp_required = models.IntegerField(default=0)
    posts_required = models.IntegerField(default=0)
    likes_required = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['xp_required', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.tier})"

class UserBadge(models.Model):
    """Track badges earned by users"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_badges')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE, related_name='user_badges')
    earned_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'badge')
        ordering = ['-earned_at']
    
    def __str__(self):
        return f"{self.user.username} earned {self.badge.name}"

class Reward(models.Model):
    """Rewards for achievements"""
    name = models.CharField(max_length=100)
    description = models.TextField()
    xp_value = models.IntegerField(default=0)
    badge = models.ForeignKey(Badge, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
```

### 5.4 Moderation App Models

**Edit: `apps/moderation/models.py`**

```python
from django.db import models
from django.contrib.auth.models import User
from apps.gallery.models import Post

class Report(models.Model):
    """User reports for inappropriate content"""
    REASON_CHOICES = [
        ('spam', 'Spam'),
        ('inappropriate', 'Inappropriate Content'),
        ('copyright', 'Copyright Violation'),
        ('harassment', 'Harassment'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('resolved', 'Resolved'),
        ('dismissed', 'Dismissed'),
    ]
    
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='reports')
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports_made')
    reason = models.CharField(max_length=20, choices=REASON_CHOICES)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Moderation
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reports_reviewed')
    reviewed_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Report on {self.post.title} by {self.reported_by.username}"

class ModerationLog(models.Model):
    """Log of moderation actions"""
    ACTION_CHOICES = [
        ('approve', 'Approved'),
        ('remove', 'Removed'),
        ('warn', 'Warned'),
        ('ban', 'Banned'),
    ]
    
    moderator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='moderation_logs')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.moderator.username} {self.action} on {self.created_at}"
```

### 5.5 Run Migrations

```bash
# Make migrations for all apps
python manage.py makemigrations users
python manage.py makemigrations gallery
python manage.py makemigrations gamification
python manage.py makemigrations moderation

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

---

## Step 6: Creating Django Forms

Forms handle user input validation on the server side.

### 6.1 Users App Forms

**Edit: `apps/users/forms.py`**

```python
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile

class RegisterForm(UserCreationForm):
    """User registration form"""
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'name@example.com',
        })
    )
    first_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'John Doe',
        })
    )
    
    class Meta:
        model = User
        fields = ('first_name', 'email', 'username', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'johndoe',
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': '••••••••',
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': '••••••••',
        })
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        if commit:
            user.save()
        return user

class LoginForm(AuthenticationForm):
    """User login form"""
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Email or username',
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': '••••••••',
        })
    )

class ProfileForm(forms.ModelForm):
    """Profile edit form"""
    first_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Your full name',
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'your@email.com',
        })
    )
    
    class Meta:
        model = Profile
        fields = ('bio',)
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': 3,
                'placeholder': 'Write your bio...',
            }),
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['first_name'].initial = self.user.first_name
            self.fields['email'].initial = self.user.email
    
    def save(self, commit=True):
        profile = super().save(commit=False)
        if self.user:
            self.user.first_name = self.cleaned_data['first_name']
            self.user.email = self.cleaned_data['email']
            self.user.save()
        if commit:
            profile.save()
        return profile

class SettingsForm(forms.ModelForm):
    """Settings form"""
    display_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
        })
    )
    
    class Meta:
        model = Profile
        fields = ('bio', 'dark_mode')
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': 3,
            }),
            'dark_mode': forms.CheckboxInput(attrs={
                'class': 'form-checkbox',
            }),
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['display_name'].initial = self.user.first_name
            self.fields['email'].initial = self.user.email
    
    def save(self, commit=True):
        profile = super().save(commit=False)
        if self.user:
            self.user.first_name = self.cleaned_data['display_name']
            self.user.email = self.cleaned_data['email']
            self.user.save()
        if commit:
            profile.save()
        return profile
```

### 6.2 Gallery App Forms

**Edit: `apps/gallery/forms.py`**

```python
from django import forms
from .models import Post, Category, Tag

class PostUploadForm(forms.ModelForm):
    """Form for uploading artwork"""
    tag = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Add a tag (e.g., portrait, digital, art)',
        }),
        help_text='Only 1 tag allowed'
    )
    
    class Meta:
        model = Post
        fields = ('title', 'description', 'image', 'category', 'filter_applied', 'visibility')
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter artwork caption',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': 4,
                'placeholder': 'Tell us more about your artwork...',
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-input',
                'accept': 'image/*',
            }),
            'category': forms.Select(attrs={
                'class': 'form-select',
            }),
            'filter_applied': forms.Select(attrs={
                'class': 'form-select',
            }),
            'visibility': forms.RadioSelect(),
        }
    
    def clean_tag(self):
        """Validate tag format"""
        tag = self.cleaned_data.get('tag', '').strip()
        if tag and not tag.replace('_', '').isalnum():
            raise forms.ValidationError('Invalid tag format. Use only letters, numbers, and underscores.')
        return tag
    
    def clean_image(self):
        """Validate image file"""
        image = self.cleaned_data.get('image')
        if image:
            # Check file size (max 10MB)
            if image.size > 10 * 1024 * 1024:
                raise forms.ValidationError('File size exceeds 10MB.')
            
            # Check file type
            if not image.content_type.startswith('image/'):
                raise forms.ValidationError('Unsupported file format. Please select an image file (PNG, JPG, GIF).')
        
        return image
    
    def save(self, commit=True):
        post = super().save(commit=False)
        if commit:
            post.save()
            
            # Handle tag (only 1 allowed)
            tag_name = self.cleaned_data.get('tag', '').strip()
            if tag_name:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                post.tags.add(tag)
        
        return post

class SearchForm(forms.Form):
    """Search form for dashboard"""
    query = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Search artworks or users...',
        })
    )
```

---

## Step 7: Creating Django Views

Views contain the business logic and connect models to templates.

### 7.1 Users App Views

**Edit: `apps/users/views.py`**

```python
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, LoginForm, ProfileForm, SettingsForm

def login_view(request):
    """User login page"""
    if request.user.is_authenticated:
        return redirect('gallery:dashboard')
    
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('gallery:dashboard')
    else:
        form = LoginForm()
    
    return render(request, 'users/login.html', {'form': form})

def register_view(request):
    """User registration page"""
    if request.user.is_authenticated:
        return redirect('gallery:dashboard')
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('gallery:dashboard')
    else:
        form = RegisterForm()
    
    return render(request, 'users/register.html', {'form': form})

def admin_login_view(request):
    """Admin login page"""
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('moderation:dashboard')
    
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_staff or user.profile.is_moderator:
                login(request, user)
                messages.success(request, 'Admin login successful!')
                return redirect('moderation:dashboard')
            else:
                messages.error(request, 'You do not have admin privileges.')
    else:
        form = LoginForm()
    
    return render(request, 'users/admin_login.html', {'form': form})

@login_required
def logout_view(request):
    """User logout"""
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('users:login')

@login_required
def profile_view(request):
    """User profile page"""
    profile = request.user.profile
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('users:profile')
    else:
        form = ProfileForm(instance=profile, user=request.user)
    
    # Get user's posts
    posts = request.user.posts.all()[:6]  # Latest 6 posts
    
    context = {
        'form': form,
        'posts': posts,
    }
    return render(request, 'users/profile.html', context)

@login_required
def settings_view(request):
    """Settings page"""
    profile = request.user.profile
    
    if request.method == 'POST':
        form = SettingsForm(request.POST, instance=profile, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Settings saved successfully!')
            return redirect('users:settings')
    else:
        form = SettingsForm(instance=profile, user=request.user)
    
    return render(request, 'users/settings.html', {'form': form})
```

### 7.2 Gallery App Views

**Edit: `apps/gallery/views.py`**

```python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Post, Category, Like
from .forms import PostUploadForm, SearchForm

@login_required
def dashboard_view(request):
    """Dashboard with search functionality"""
    search_form = SearchForm(request.GET)
    posts = Post.objects.filter(visibility='public').select_related('user', 'category')
    
    # Handle search query
    if search_form.is_valid():
        query = search_form.cleaned_data.get('query', '').strip()
        if query:
            posts = posts.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(user__username__icontains=query) |
                Q(tags__name__icontains=query)
            ).distinct()
    
    # Get user stats
    user_stats = {
        'artworkCreated': request.user.posts.count(),
        'totalXP': request.user.profile.xp,
        'posts': request.user.posts.count(),
        'badges': request.user.user_badges.count(),
    }
    
    # Limit to recent posts
    posts = posts[:12]
    
    context = {
        'search_form': search_form,
        'posts': posts,
        'user_stats': user_stats,
    }
    return render(request, 'gallery/dashboard.html', context)

@login_required
def browse_view(request):
    """Browse all artworks with filtering"""
    posts = Post.objects.filter(visibility='public').select_related('user', 'category')
    
    # Filter by category
    category_slug = request.GET.get('category')
    if category_slug:
        posts = posts.filter(category__slug=category_slug)
    
    # Filter by tag
    tag_slug = request.GET.get('tag')
    if tag_slug:
        posts = posts.filter(tags__slug=tag_slug)
    
    # Get all categories for filter
    categories = Category.objects.all()
    
    context = {
        'posts': posts,
        'categories': categories,
        'selected_category': category_slug,
    }
    return render(request, 'gallery/browse.html', context)

@login_required
def upload_view(request):
    """Upload artwork"""
    if request.method == 'POST':
        form = PostUploadForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            form.save_m2m()  # Save tags
            
            # Update user stats
            request.user.profile.artwork_count += 1
            request.user.profile.add_xp(50)  # Award 50 XP for upload
            
            messages.success(request, 'Artwork uploaded successfully!')
            return redirect('gallery:browse')
    else:
        form = PostUploadForm()
    
    # Get categories for dropdown
    categories = Category.objects.all()
    
    context = {
        'form': form,
        'categories': categories,
    }
    return render(request, 'gallery/upload.html', context)

@login_required
def like_post(request, post_id):
    """Like/unlike a post (AJAX endpoint)"""
    post = get_object_or_404(Post, id=post_id)
    
    # Check if already liked
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    
    if not created:
        # Unlike
        like.delete()
        post.like_count -= 1
        liked = False
    else:
        # Like
        post.like_count += 1
        liked = True
        
        # Award XP to post owner
        if post.user != request.user:
            post.user.profile.add_xp(5)
    
    post.save()
    
    # Return JSON response for AJAX
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        from django.http import JsonResponse
        return JsonResponse({'liked': liked, 'like_count': post.like_count})
    
    # Redirect if not AJAX
    return redirect(request.META.get('HTTP_REFERER', 'gallery:browse'))
```

### 7.3 Gamification App Views

**Edit: `apps/gamification/views.py`**

```python
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Badge, UserBadge

@login_required
def badges_view(request):
    """Badges page showing earned and available badges"""
    # Get all badges
    all_badges = Badge.objects.all()
    
    # Get user's earned badges
    earned_badge_ids = request.user.user_badges.values_list('badge_id', flat=True)
    
    # Separate earned and available badges
    earned_badges = all_badges.filter(id__in=earned_badge_ids)
    available_badges = all_badges.exclude(id__in=earned_badge_ids)
    
    # Calculate progress for available badges
    user_profile = request.user.profile
    for badge in available_badges:
        # Calculate progress percentage
        if badge.xp_required > 0:
            badge.xp_progress = min(100, (user_profile.xp / badge.xp_required) * 100)
        else:
            badge.xp_progress = 100
        
        if badge.posts_required > 0:
            badge.posts_progress = min(100, (user_profile.artwork_count / badge.posts_required) * 100)
        else:
            badge.posts_progress = 100
    
    context = {
        'earned_badges': earned_badges,
        'available_badges': available_badges,
    }
    return render(request, 'gamification/badges.html', context)
```

### 7.4 Moderation App Views

**Edit: `apps/moderation/views.py`**

```python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from apps.gallery.models import Post
from .models import Report, ModerationLog

def is_moderator(user):
    """Check if user is staff or moderator"""
    return user.is_staff or user.profile.is_moderator

@login_required
@user_passes_test(is_moderator)
def moderation_dashboard(request):
    """Moderation dashboard"""
    # Get pending reports
    pending_reports = Report.objects.filter(status='pending').select_related('post', 'reported_by')
    
    # Get recent posts
    recent_posts = Post.objects.filter(visibility='public').order_by('-created_at')[:20]
    
    # Get moderation stats
    stats = {
        'pending_reports': pending_reports.count(),
        'total_posts': Post.objects.count(),
        'public_posts': Post.objects.filter(visibility='public').count(),
    }
    
    context = {
        'pending_reports': pending_reports,
        'recent_posts': recent_posts,
        'stats': stats,
    }
    return render(request, 'moderation/moderation.html', context)

@login_required
@user_passes_test(is_moderator)
def approve_post(request, post_id):
    """Approve a post"""
    post = get_object_or_404(Post, id=post_id)
    
    # Log moderation action
    ModerationLog.objects.create(
        moderator=request.user,
        post=post,
        action='approve',
        reason='Post approved'
    )
    
    messages.success(request, f'Post "{post.title}" approved.')
    return redirect('moderation:dashboard')

@login_required
@user_passes_test(is_moderator)
def remove_post(request, post_id):
    """Remove a post"""
    post = get_object_or_404(Post, id=post_id)
    title = post.title
    
    # Log moderation action
    ModerationLog.objects.create(
        moderator=request.user,
        post=post,
        action='remove',
        reason='Post removed by moderator'
    )
    
    # Change visibility to private
    post.visibility = 'private'
    post.save()
    
    messages.warning(request, f'Post "{title}" removed.')
    return redirect('moderation:dashboard')
```

---

## Step 8: URL Configuration

Configure URLs for each app and the main project.

### 8.1 Users App URLs

**Create: `apps/users/urls.py`**

```python
from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('admin-login/', views.admin_login_view, name='admin_login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('settings/', views.settings_view, name='settings'),
]
```

### 8.2 Gallery App URLs

**Create: `apps/gallery/urls.py`**

```python
from django.urls import path
from . import views

app_name = 'gallery'

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('browse/', views.browse_view, name='browse'),
    path('upload/', views.upload_view, name='upload'),
    path('post/<int:post_id>/like/', views.like_post, name='like_post'),
]
```

### 8.3 Gamification App URLs

**Create: `apps/gamification/urls.py`**

```python
from django.urls import path
from . import views

app_name = 'gamification'

urlpatterns = [
    path('badges/', views.badges_view, name='badges'),
]
```

### 8.4 Moderation App URLs

**Create: `apps/moderation/urls.py`**

```python
from django.urls import path
from . import views

app_name = 'moderation'

urlpatterns = [
    path('', views.moderation_dashboard, name='dashboard'),
    path('approve/<int:post_id>/', views.approve_post, name='approve_post'),
    path('remove/<int:post_id>/', views.remove_post, name='remove_post'),
]
```

### 8.5 Main Project URLs

**Edit: `stars_project/urls.py`**

```python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Redirect root to login
    path('', RedirectView.as_view(pattern_name='users:login', permanent=False)),
    
    # App URLs
    path('accounts/', include('apps.users.urls')),
    path('gallery/', include('apps.gallery.urls')),
    path('gamification/', include('apps.gamification.urls')),
    path('moderation/', include('apps.moderation.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```

---

## Step 9: Converting Each Page

Now we'll convert each page from the React prototype to Django templates.

### 9.1 Login Page

**Create: `apps/users/templates/users/login.html`**

```html
{% extends 'base.html' %}
{% load static %}

{% block title %}Login - STARS{% endblock %}

{% block extra_css %}
<link rel="stylesheet" href="{% static 'css/pages/login.css' %}">
{% endblock %}

{% block content %}
<div class="auth-container">
    <div class="auth-card">
        <!-- Logo -->
        <div class="auth-logo">
            <img src="{% static 'images/logo.png' %}" alt="STARS" class="logo-image">
            <h1>STARS</h1>
            <p class="tagline">Student Artist Space</p>
        </div>
        
        <!-- Welcome Text -->
        <div class="auth-header">
            <h2>Welcome Back</h2>
            <p class="text-muted">Sign in to your account to continue</p>
        </div>
        
        <!-- Display Messages -->
        {% if messages %}
            {% for message in messages %}
                <div class="alert alert-{{ message.tags }}">
                    {{ message }}
                </div>
            {% endfor %}
        {% endif %}
        
        <!-- Form Errors -->
        {% if form.non_field_errors %}
            <div class="alert alert-error">
                {% for error in form.non_field_errors %}
                    <p>{{ error }}</p>
                {% endfor %}
            </div>
        {% endif %}
        
        <!-- Login Form -->
        <form method="post" class="auth-form">
            {% csrf_token %}
            
            <div class="form-group">
                <label for="{{ form.username.id_for_label }}" class="form-label">
                    Email or Username
                </label>
                {{ form.username }}
                {% if form.username.errors %}
                    <div class="form-error">
                        {% for error in form.username.errors %}
                            {{ error }}
                        {% endfor %}
                    </div>
                {% endif %}
            </div>
            
            <div class="form-group">
                <label for="{{ form.password.id_for_label }}" class="form-label">
                    Password
                </label>
                {{ form.password }}
                {% if form.password.errors %}
                    <div class="form-error">
                        {% for error in form.password.errors %}
                            {{ error }}
                        {% endfor %}
                    </div>
                {% endif %}
            </div>
            
            <button type="submit" class="btn btn-primary btn-block">
                Sign In
            </button>
        </form>
        
        <!-- Links -->
        <div class="auth-links">
            <p>
                Don't have an account? 
                <a href="{% url 'users:register' %}">Create Account</a>
            </p>
            <p>
                <a href="{% url 'users:admin_login' %}" class="admin-link">
                    Admin Login
                </a>
            </p>
        </div>
    </div>
</div>
{% endblock %}
```

**Create: `static/css/pages/login.css`**

```css
.auth-container {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: var(--spacing-lg);
    background: linear-gradient(135deg, var(--color-primary) 0%, #4338ca 100%);
}

.auth-card {
    background-color: var(--color-card);
    border-radius: var(--radius-xl);
    box-shadow: var(--shadow-xl);
    padding: var(--spacing-2xl);
    max-width: 450px;
    width: 100%;
}

.auth-logo {
    text-align: center;
    margin-bottom: var(--spacing-xl);
}

.auth-logo .logo-image {
    width: 64px;
    height: 64px;
    margin: 0 auto var(--spacing-md);
}

.auth-logo h1 {
    font-size: var(--font-3xl);
    color: var(--color-primary);
    margin-bottom: var(--spacing-xs);
}

.tagline {
    font-size: var(--font-sm);
    color: var(--color-muted-foreground);
    margin: 0;
}

.auth-header {
    text-align: center;
    margin-bottom: var(--spacing-xl);
}

.auth-header h2 {
    margin-bottom: var(--spacing-xs);
}

.auth-form {
    margin-bottom: var(--spacing-lg);
}

.btn-block {
    width: 100%;
}

.auth-links {
    text-align: center;
}

.auth-links p {
    font-size: var(--font-sm);
    color: var(--color-muted-foreground);
    margin-bottom: var(--spacing-sm);
}

.auth-links a {
    color: var(--color-primary);
    font-weight: var(--font-medium);
}

.admin-link {
    color: var(--color-muted-foreground) !important;
    font-size: var(--font-xs);
}
```

### 9.2 Dashboard Page with Integrated Search

**Create: `apps/gallery/templates/gallery/dashboard.html`**

```html
{% extends 'base.html' %}
{% load static %}

{% block title %}Dashboard - STARS{% endblock %}

{% block extra_css %}
<link rel="stylesheet" href="{% static 'css/pages/dashboard.css' %}">
{% endblock %}

{% block content %}
<div class="dashboard-container">
    <!-- Page Header -->
    <div class="page-header">
        <div>
            <h1>Dashboard</h1>
            <p class="text-muted">Welcome back, {{ request.user.first_name|default:request.user.username }}!</p>
        </div>
    </div>
    
    <!-- Search Bar -->
    <div class="search-section">
        <form method="get" action="{% url 'gallery:dashboard' %}" class="search-form">
            <svg class="search-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <circle cx="11" cy="11" r="8"></circle>
                <path d="m21 21-4.35-4.35"></path>
            </svg>
            {{ search_form.query }}
            <button type="submit" class="btn btn-primary">Search</button>
        </form>
    </div>
    
    <!-- Stats Cards -->
    <div class="stats-grid">
        <div class="stat-card">
            <div class="stat-icon stat-icon-blue">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
                    <circle cx="8.5" cy="8.5" r="1.5"></circle>
                    <polyline points="21 15 16 10 5 21"></polyline>
                </svg>
            </div>
            <div class="stat-content">
                <p class="stat-label">Artworks Created</p>
                <p class="stat-value">{{ user_stats.artworkCreated }}</p>
            </div>
        </div>
        
        <div class="stat-card">
            <div class="stat-icon stat-icon-purple">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
                </svg>
            </div>
            <div class="stat-content">
                <p class="stat-label">Total XP</p>
                <p class="stat-value">{{ user_stats.totalXP }}</p>
            </div>
        </div>
        
        <div class="stat-card">
            <div class="stat-icon stat-icon-green">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <path d="M12 15l-3 6v-6H6l6-9 6 9h-3v6z"></path>
                </svg>
            </div>
            <div class="stat-content">
                <p class="stat-label">Badges Earned</p>
                <p class="stat-value">{{ user_stats.badges }}</p>
            </div>
        </div>
    </div>
    
    <!-- Recent Artworks -->
    <div class="artworks-section">
        <div class="section-header">
            <h2>Recent Artworks</h2>
            <a href="{% url 'gallery:browse' %}" class="btn btn-outline">View All</a>
        </div>
        
        <div class="artworks-grid">
            {% for post in posts %}
                <div class="artwork-card">
                    <div class="artwork-image-container">
                        {% if post.image %}
                            <img src="{{ post.image.url }}" alt="{{ post.title }}" class="artwork-image">
                        {% else %}
                            <img src="{% static 'images/placeholder.jpg' %}" alt="Placeholder" class="artwork-image">
                        {% endif %}
                    </div>
                    
                    <div class="artwork-content">
                        <div class="artwork-header">
                            <div class="avatar avatar-sm">
                                {{ post.user.first_name|first|default:post.user.username|first|upper }}
                            </div>
                            <div>
                                <h4 class="artwork-title">{{ post.title }}</h4>
                                <p class="artwork-author">@{{ post.user.username }}</p>
                            </div>
                        </div>
                        
                        <div class="artwork-stats">
                            <span class="stat-item">
                                <svg class="icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                                    <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path>
                                </svg>
                                {{ post.like_count }}
                            </span>
                            <span class="stat-item">
                                <svg class="icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                                    <circle cx="18" cy="5" r="3"></circle>
                                    <circle cx="6" cy="12" r="3"></circle>
                                    <circle cx="18" cy="19" r="3"></circle>
                                    <line x1="8.59" y1="13.51" x2="15.42" y2="17.49"></line>
                                    <line x1="15.41" y1="6.51" x2="8.59" y2="10.49"></line>
                                </svg>
                                {{ post.share_count }}
                            </span>
                        </div>
                    </div>
                </div>
            {% empty %}
                <div class="empty-state">
                    <p>No artworks found.</p>
                    <a href="{% url 'gallery:upload' %}" class="btn btn-primary">Upload Your First Artwork</a>
                </div>
            {% endfor %}
        </div>
    </div>
</div>
{% endblock %}
```

### 9.3 Upload Page

**Create: `apps/gallery/templates/gallery/upload.html`**

```html
{% extends 'base.html' %}
{% load static %}

{% block title %}Upload Artwork - STARS{% endblock %}

{% block extra_css %}
<link rel="stylesheet" href="{% static 'css/pages/upload.css' %}">
{% endblock %}

{% block content %}
<div class="upload-container">
    <div class="page-header">
        <h1>Upload Artwork</h1>
        <p class="text-muted">Share your creative work with the community</p>
    </div>
    
    <!-- Messages -->
    {% if messages %}
        {% for message in messages %}
            <div class="alert alert-{{ message.tags }}">
                {{ message }}
            </div>
        {% endfor %}
    {% endif %}
    
    <!-- Upload Form -->
    <form method="post" enctype="multipart/form-data" class="upload-form">
        {% csrf_token %}
        
        <!-- Image Upload -->
        <div class="card">
            <label class="form-label">Image Upload *</label>
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
                    <svg class="upload-icon" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                        <polyline points="17 8 12 3 7 8"></polyline>
                        <line x1="12" y1="3" x2="12" y2="15"></line>
                    </svg>
                    <p>Click to upload or drag and drop</p>
                    <p class="upload-help">PNG, JPG, or GIF (max. 10MB)</p>
                </label>
                <div id="preview-container" style="display: none;">
                    <img id="preview-image" src="" alt="Preview" class="preview-image">
                    <button type="button" id="remove-image" class="btn btn-outline btn-sm">Remove</button>
                </div>
            </div>
            {% if form.image.errors %}
                <div class="form-error">
                    {% for error in form.image.errors %}
                        {{ error }}
                    {% endfor %}
                </div>
            {% endif %}
        </div>
        
        <!-- Image Filters -->
        <div class="card" id="filters-section" style="display: none;">
            <label class="form-label">Image Filters</label>
            <div class="filters-grid">
                <label class="filter-option">
                    <input type="radio" name="filter_applied" value="none" checked>
                    <div class="filter-preview" data-filter="none">
                        <div class="filter-sample"></div>
                        <span>Original</span>
                    </div>
                </label>
                <label class="filter-option">
                    <input type="radio" name="filter_applied" value="grayscale">
                    <div class="filter-preview" data-filter="grayscale(100%)">
                        <div class="filter-sample"></div>
                        <span>Grayscale</span>
                    </div>
                </label>
                <label class="filter-option">
                    <input type="radio" name="filter_applied" value="sepia">
                    <div class="filter-preview" data-filter="sepia(100%)">
                        <div class="filter-sample"></div>
                        <span>Sepia</span>
                    </div>
                </label>
                <label class="filter-option">
                    <input type="radio" name="filter_applied" value="brightness">
                    <div class="filter-preview" data-filter="brightness(1.3)">
                        <div class="filter-sample"></div>
                        <span>Bright</span>
                    </div>
                </label>
                <label class="filter-option">
                    <input type="radio" name="filter_applied" value="contrast">
                    <div class="filter-preview" data-filter="contrast(1.3)">
                        <div class="filter-sample"></div>
                        <span>Contrast</span>
                    </div>
                </label>
                <label class="filter-option">
                    <input type="radio" name="filter_applied" value="vintage">
                    <div class="filter-preview" data-filter="sepia(50%) contrast(1.2)">
                        <div class="filter-sample"></div>
                        <span>Vintage</span>
                    </div>
                </label>
            </div>
        </div>
        
        <!-- Post Details -->
        <div class="card">
            <div class="form-group">
                <label for="{{ form.title.id_for_label }}" class="form-label">
                    Caption / Description *
                </label>
                {{ form.title }}
                {% if form.title.errors %}
                    <div class="form-error">
                        {% for error in form.title.errors %}
                            {{ error }}
                        {% endfor %}
                    </div>
                {% endif %}
            </div>
            
            <div class="form-group">
                <label for="{{ form.description.id_for_label }}" class="form-label">
                    Description
                </label>
                {{ form.description }}
                {% if form.description.errors %}
                    <div class="form-error">
                        {% for error in form.description.errors %}
                            {{ error }}
                        {% endfor %}
                    </div>
                {% endif %}
            </div>
            
            <div class="form-group">
                <label for="{{ form.category.id_for_label }}" class="form-label">
                    Category Selection *
                </label>
                {{ form.category }}
                {% if form.category.errors %}
                    <div class="form-error">
                        {% for error in form.category.errors %}
                            {{ error }}
                        {% endfor %}
                    </div>
                {% endif %}
            </div>
            
            <div class="form-group">
                <label for="{{ form.tag.id_for_label }}" class="form-label">
                    Tag (1 only)
                </label>
                {{ form.tag }}
                <p class="form-help">{{ form.tag.help_text }}</p>
                {% if form.tag.errors %}
                    <div class="form-error">
                        {% for error in form.tag.errors %}
                            {{ error }}
                        {% endfor %}
                    </div>
                {% endif %}
            </div>
            
            <div class="form-group">
                <label class="form-label">Visibility</label>
                <div class="radio-group">
                    {% for choice in form.visibility %}
                        <label class="radio-label">
                            {{ choice.tag }}
                            <span>{{ choice.choice_label }}</span>
                        </label>
                    {% endfor %}
                </div>
            </div>
        </div>
        
        <!-- Submit Buttons -->
        <div class="form-actions">
            <button type="submit" class="btn btn-primary">Upload Artwork</button>
            <a href="{% url 'gallery:browse' %}" class="btn btn-outline">Cancel</a>
        </div>
    </form>
</div>
{% endblock %}

{% block extra_js %}
<script src="{% static 'js/filters.js' %}"></script>
{% endblock %}
```

**Create: `static/js/filters.js`**

```javascript
// Image preview and filter functionality
document.addEventListener('DOMContentLoaded', function() {
    const imageInput = document.getElementById('id_image');
    const uploadArea = document.getElementById('upload-area');
    const previewContainer = document.getElementById('preview-container');
    const previewImage = document.getElementById('preview-image');
    const removeButton = document.getElementById('remove-image');
    const filtersSection = document.getElementById('filters-section');
    const uploadLabel = uploadArea.querySelector('.upload-label');
    const filterOptions = document.querySelectorAll('input[name="filter_applied"]');
    
    // Handle file selection
    imageInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            // Validate file type
            if (!file.type.startsWith('image/')) {
                alert('Please select an image file.');
                return;
            }
            
            // Validate file size (10MB max)
            if (file.size > 10 * 1024 * 1024) {
                alert('File size exceeds 10MB.');
                return;
            }
            
            // Show preview
            const reader = new FileReader();
            reader.onload = function(e) {
                previewImage.src = e.target.result;
                uploadLabel.style.display = 'none';
                previewContainer.style.display = 'block';
                filtersSection.style.display = 'block';
            };
            reader.readAsDataURL(file);
        }
    });
    
    // Remove image
    removeButton.addEventListener('click', function() {
        imageInput.value = '';
        previewImage.src = '';
        uploadLabel.style.display = 'block';
        previewContainer.style.display = 'none';
        filtersSection.style.display = 'none';
    });
    
    // Apply filter to preview
    filterOptions.forEach(function(option) {
        option.addEventListener('change', function() {
            const filterValue = this.closest('.filter-option').querySelector('.filter-preview').dataset.filter;
            previewImage.style.filter = filterValue;
        });
    });
});
```

---

## Step 10: Implementing Dark Mode

### 10.1 Dark Mode CSS

**Create: `static/css/dark-mode.css`**

```css
/* Dark mode styles */
.dark {
  /* Colors are already defined in variables.css */
}

/* Smooth transitions */
body,
.card,
.form-input,
.form-textarea,
.form-select,
.btn {
  transition: background-color 0.3s, color 0.3s, border-color 0.3s;
}
```

### 10.2 Dark Mode Toggle JavaScript

**Create: `static/js/dark-mode.js`**

```javascript
// Dark mode toggle functionality
document.addEventListener('DOMContentLoaded', function() {
    const darkModeCheckbox = document.getElementById('id_dark_mode');
    
    if (darkModeCheckbox) {
        // Set initial state
        const isDarkMode = darkModeCheckbox.checked;
        updateDarkMode(isDarkMode);
        
        // Listen for changes
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

### 10.3 Settings Page with Dark Mode Toggle

**Create: `apps/users/templates/users/settings.html`**

```html
{% extends 'base.html' %}
{% load static %}

{% block title %}Settings - STARS{% endblock %}

{% block content %}
<div class="settings-container">
    <div class="page-header">
        <h1>Settings</h1>
        <p class="text-muted">Manage your account preferences and settings</p>
    </div>
    
    {% if messages %}
        {% for message in messages %}
            <div class="alert alert-{{ message.tags }}">
                {{ message }}
            </div>
        {% endfor %}
    {% endif %}
    
    <form method="post" class="settings-form">
        {% csrf_token %}
        
        <!-- Account Information -->
        <div class="card">
            <div class="card-header">
                <h3 class="card-title">Account Information</h3>
            </div>
            
            <div class="form-group">
                <label for="{{ form.display_name.id_for_label }}" class="form-label">
                    Display Name
                </label>
                {{ form.display_name }}
            </div>
            
            <div class="form-group">
                <label for="{{ form.email.id_for_label }}" class="form-label">
                    Email Address
                </label>
                {{ form.email }}
            </div>
            
            <div class="form-group">
                <label for="{{ form.bio.id_for_label }}" class="form-label">
                    Bio
                </label>
                {{ form.bio }}
            </div>
        </div>
        
        <!-- Appearance -->
        <div class="card">
            <div class="card-header">
                <h3 class="card-title">Appearance</h3>
            </div>
            
            <div class="form-group">
                <label class="toggle-label">
                    {{ form.dark_mode }}
                    <span>Dark Mode</span>
                </label>
                <p class="form-help">Enable dark mode for better viewing at night</p>
            </div>
        </div>
        
        <!-- Save Button -->
        <div class="form-actions">
            <button type="submit" class="btn btn-primary">Save Changes</button>
        </div>
    </form>
</div>
{% endblock %}

{% block extra_js %}
<script src="{% static 'js/dark-mode.js' %}"></script>
{% endblock %}
```

---

## Step 11: Implementing Search Functionality

Search is integrated into the Dashboard view (already shown in Step 9.2). The search filters posts by:
- Post title
- Post description
- Username
- Tag names

The view handles the search query and filters the queryset accordingly.

---

## Step 12: Implementing Logout Confirmation

### 12.1 Logout Confirmation JavaScript

**Create: `static/js/logout-confirm.js`**

```javascript
// Logout confirmation
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

### 12.2 Header Dropdown Toggle

**Add to: `static/js/main.js`**

```javascript
// General utilities
document.addEventListener('DOMContentLoaded', function() {
    // User dropdown toggle
    const userMenuButton = document.getElementById('user-menu-button');
    const userMenu = document.getElementById('user-menu');
    
    if (userMenuButton && userMenu) {
        userMenuButton.addEventListener('click', function(e) {
            e.stopPropagation();
            const isHidden = userMenu.style.display === 'none' || !userMenu.style.display;
            userMenu.style.display = isHidden ? 'block' : 'none';
        });
        
        // Close dropdown when clicking outside
        document.addEventListener('click', function() {
            userMenu.style.display = 'none';
        });
        
        userMenu.addEventListener('click', function(e) {
            e.stopPropagation();
        });
    }
});
```

---

## Step 13: Best Practices and Tips

### 13.1 Django Template Best Practices

1. **Always use {% csrf_token %} in forms**
   ```html
   <form method="post">
       {% csrf_token %}
       ...
   </form>
   ```

2. **Use {% load static %} at the top of templates**
   ```html
   {% load static %}
   <link rel="stylesheet" href="{% static 'css/style.css' %}">
   ```

3. **Use {% url %} for links instead of hardcoded URLs**
   ```html
   <a href="{% url 'users:profile' %}">Profile</a>
   ```

4. **Use template filters for formatting**
   ```html
   {{ user.date_joined|date:"F d, Y" }}
   {{ post.title|truncatewords:10 }}
   ```

5. **Handle empty states**
   ```html
   {% for post in posts %}
       ...
   {% empty %}
       <p>No posts found.</p>
   {% endfor %}
   ```

### 13.2 CSS Organization Tips

1. **Use CSS custom properties for theming**
2. **Keep selectors specific but not too deep**
3. **Use BEM naming convention** (Block-Element-Modifier)
4. **Group related properties together**
5. **Use mobile-first responsive design**

### 13.3 JavaScript Best Practices

1. **Always use `addEventListener`** instead of inline handlers
2. **Check if elements exist before accessing them**
3. **Use `e.preventDefault()` when needed**
4. **Keep JavaScript minimal** (Django handles most logic)
5. **Use AJAX sparingly** (like/unlike functionality)

### 13.4 Django Security

1. **Never disable {% csrf_token %}**
2. **Use @login_required decorator** on protected views
3. **Validate all user input** in forms
4. **Use Django's built-in authentication**
5. **Set DEBUG=False in production**
6. **Use environment variables** for sensitive data

### 13.5 Performance Optimization

1. **Use select_related() and prefetch_related()** to reduce database queries
2. **Add database indexes** on frequently queried fields
3. **Use Django's caching framework** for expensive queries
4. **Optimize images** before uploading
5. **Use pagination** for large lists

---

## Step 14: Deployment Checklist

### 14.1 Pre-Deployment Steps

1. **Collect static files**
   ```bash
   python manage.py collectstatic
   ```

2. **Run migrations**
   ```bash
   python manage.py migrate
   ```

3. **Create initial data**
   ```python
   # Create categories
   python manage.py shell
   >>> from apps.gallery.models import Category
   >>> Category.objects.create(name='Digital Painting')
   >>> Category.objects.create(name='Abstract Art')
   >>> Category.objects.create(name='Illustration')
   >>> Category.objects.create(name='Traditional Art')
   >>> Category.objects.create(name='Character Art')
   >>> Category.objects.create(name='Watercolor')
   ```

4. **Create sample badges**
   ```python
   >>> from apps.gamification.models import Badge
   >>> Badge.objects.create(
   ...     name='First Upload',
   ...     description='Upload your first artwork',
   ...     tier='bronze',
   ...     icon='🎨',
   ...     posts_required=1
   ... )
   ```

5. **Update settings.py for production**
   ```python
   DEBUG = False
   ALLOWED_HOSTS = ['yourdomain.com']
   SECRET_KEY = os.environ.get('SECRET_KEY')
   ```

### 14.2 Environment Variables

Create a `.env` file (don't commit to Git):

```
SECRET_KEY=your-secret-key-here
DEBUG=False
DATABASE_URL=your-database-url
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

### 14.3 Production Server Setup

1. **Install gunicorn**
   ```bash
   pip install gunicorn
   ```

2. **Create gunicorn config**
   ```bash
   gunicorn stars_project.wsgi:application --bind 0.0.0.0:8000
   ```

3. **Setup nginx** as reverse proxy

4. **Setup SSL certificate** (Let's Encrypt)

---

## Conclusion

This guide covered the complete conversion of the STARS Figma prototype to Django:

✅ **Project Structure** - Organized Django apps (users, gallery, gamification, moderation)  
✅ **Static Files** - Converted Tailwind CSS to custom CSS using CSS variables  
✅ **Templates** - Created reusable base templates with {% extends %} and {% include %}  
✅ **Models** - Defined database schema for all entities  
✅ **Forms** - Created Django forms for all user inputs  
✅ **Views** - Implemented business logic using Django views  
✅ **URLs** - Configured URL routing for all pages  
✅ **Dark Mode** - Implemented theme toggle with database storage  
✅ **Search** - Integrated search in Dashboard  
✅ **Authentication** - Used Django's built-in auth system  

**Key Takeaways:**
- Keep HTML semantic and simple
- Use Django template tags ({{ }}, {% %}, {% url %})
- Store user preferences in database (dark mode)
- Validate all input server-side with Django forms
- Use CSS custom properties for consistent theming
- Minimal JavaScript (only for UI interactions)

Your Django application is now ready for deployment! 🚀
