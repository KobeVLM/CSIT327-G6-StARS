# Copilot Instructions for StARS Project

## Project Overview

**StARS (Student Art Sharing System)** is a Django 5.2.6 web-only platform for students to share, discover, and interact with digital artwork. The system focuses on community building, user profiles, artwork galleries, and social features for student artists.

### Core Features

- **User Management**: Registration, authentication, profiles with avatars and bios
- **Artwork Sharing**: Upload, display, and categorize student artwork
- **Social Features**: Comments, likes, follows, and community interaction
- **Gamification**: User levels, XP system, badges, and achievements
- **Content Management**: Blogs, character galleries, and art collections
- **Responsive Design**: Mobile-friendly interface for art viewing and sharing

## Project Structure

- **Root directory**: `c:\Users\Kobe\Desktop\CSIT327-G6-StARS\`
- **Django project**: `stars_project/` (contains `manage.py`)
- **Project package**: `stars/` (Django project configuration)
- **Apps grouping**: `apps/` (contains `users`, `gallery`, `gamification`, `moderation`)
- **Working directory**: Always operate from `stars_project/` when running Django commands

## Key Architecture Patterns

### Django Project Layout (updated for FIGMA conversion)

```
CSIT327-G6-StARS/
├── README.md                # Project documentation
├── requirements.txt         # Python dependencies
├── .github/
│   └── copilot-instructions.md
└── stars_project/           # Django project root
  ├── manage.py            # Django management script
  ├── venv/                # Virtual environment (local only)
  ├── media/               # User-uploaded files (avatars, artwork)
  ├── static/              # CSS, JS, images
  │   ├── css/             # Global stylesheets (variables, base, pages)
  │   └── js/              # Small JS utilities (dark mode, dropdowns)
  ├── templates/          # Global templates
  │   ├── base.html        # Base layout
  │   ├── partials/       # Reusable partials from Figma
  │   │   ├── auth_header.html
  │   │   ├── app_header.html
  │   │   └── sidebar.html
  │   └── auth/           # Auth pages converted from Figma
  │       ├── login.html
  │       └── register.html
  ├── apps/               # Grouped Django apps (recommended)
  │   ├── users/          # Authentication & user profiles
  │   ├── gallery/        # Posts and gallery features
  │   ├── gamification/   # Badges, XP, rewards
  │   └── moderation/     # Admin/moderation tools
  └── stars/              # Django project configuration package
    ├── settings.py     # Project settings (keep DB settings unchanged)
    ├── urls.py         # Main URL routing
    ├── wsgi.py         # WSGI application
    └── asgi.py         # ASGI application
```

### Development Environment Setup

- **Virtual environment**: Located at `stars_project/venv/`
- **Activation**: Use `venv\Scripts\Activate.ps1` on Windows
- **Dependencies**: Install with `pip install -r requirements.txt`
- **Required packages**: Django, Pillow (for image handling), mysqlclient (or your DB driver), python-dotenv
- **Database setup**: Run `python manage.py migrate` before first use (do NOT modify existing DB settings)
- **Media files**: Ensure `media/` directory exists for user uploads

## Development Workflow

### Essential Commands (from `stars_project/` directory)

```bash
# Environment setup
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r ..\requirements.txt

# Django operations
python manage.py runserver      # Start development server
python manage.py migrate        # Apply database migrations
python manage.py makemigrations # Create new migrations
python manage.py createsuperuser # Create admin user
python manage.py startapp <name> # Create new Django app
```

### Git Workflow Conventions

- **Branch naming**:

  - Features: `feature/<short-description>`
  - Bug fixes: `fix/<short-description>`
  - Documentation: `docs/<short-description>`

- **Commit messages** (Conventional Commits):
  - `feat:` for new features
  - `fix:` for bug fixes
  - `docs:` for documentation
  - `chore:` for maintenance
  - `style:` for formatting
  - `refactor:` for code restructuring
  - `test:` for adding tests

### Pull Request Requirements

1. Pull latest changes from main branch
2. Ensure project runs without errors (`python manage.py runserver`)
3. Write clear PR description with what/why/testing details
4. Wait for code owner review and approval

## Important Conventions

### Settings & Database

- **Secret key**: Uses Django's insecure default in development (update for production)
- **Database**: Keep your existing MySQL database configuration in `stars/settings.py` — do NOT change database settings as requested.
- **Static files**: Use `STATIC_URL = '/static/'` and place Figma-converted CSS in `static/css/` (see mapping below)
- **Media files**: Configured for user uploads at `MEDIA_URL = '/media/'`
- **Templates**: Use `templates/` for global templates and `apps/<app>/templates/<app>/` for app-specific templates

### URL Patterns

- Main URL configuration in `stars/urls.py`
- App URLs live in `apps/<app>/urls.py` and should use namespacing (e.g., `users:login`, `gallery:dashboard`)
- Pages converted from Figma: `login`, `register`, `dashboard`, `profile`, `settings` (mapped below)

### Figma → Django Conversion Mapping (from `FIGMA_TO_DJANGO_CONVERSION/FILE_MAP.txt`)

Copy these files as-is into the project (paths are the recommended destinations):

- `/styles/globals.css` → `static/css/globals.css`
- `/components/Header.tsx` → `templates/partials/auth_header.html`
- `/components/AppHeader.tsx` → `templates/partials/app_header.html`
- `/components/pages/Login.tsx` → `templates/auth/login.html`
- `/components/pages/Register.tsx` → `templates/auth/register.html`
- `/components/pages/Dashboard.tsx` → `templates/dashboard.html`
- `/components/pages/Profile.tsx` → `templates/profile.html`
- `/components/pages/Settings.tsx` → `templates/settings.html`

Use modified versions (conflicts resolved) and convert them to Django templates:

- `/DJANGO_CONVERSION/Sidebar-simplified.tsx` → `templates/partials/sidebar.html` (convert JSX to template include)
- `/DJANGO_CONVERSION/App-simplified.tsx` → `templates/base.html` and optionally `templates/layouts/app_layout.html`

Skip these features for now (as per mapping): AdminLogin, Browse, Upload, Moderation, Badges, and `ui/*` components.

### JavaScript Interactivity

Convert `javascript-extractions.js` into `static/js/app.js` and include features:

- Dark mode toggle
- Profile dropdown menu
- Inline profile editing (progressive enhancement)
- Dashboard search
- Logout confirmation

### Icons and dependencies

You can keep using the Lucide icons via CDN (or include SVG icons in `static/images/icons/`). Tailwind classes used in the React prototype should be translated into the CSS variables and rules in `static/css/globals.css` and `static/css/base.css`.

### ERD / Models (high level)

The FIGMA conversion guide assumes and expects the following model boundaries (align these with your existing models or update carefully):

- `apps.users`:

  - User (Django's user or custom user)
  - Profile (avatar, bio, location, xp, level)
  - Settings (user preferences, dark_mode, notification preferences)

- `apps.gallery`:

  - Post (title, image, description, author, created_at, category)
  - Category
  - Tag
  - Like / Reaction

- `apps.gamification`:

  - Badge
  - Reward
  - UserProgress (xp, achievements)

- `apps.moderation`:
  - Report
  - ModerationLog

When updating `copilot-instructions.md`, we include the above ERD summary to reflect the changed ERD used by the FIGMA conversion guide.

## Current State & Next Steps

This is an active Django project with core art sharing functionality:

- ✅ User authentication system (login, register, logout)
- ✅ User profiles with avatars, bios, and XP/level system
- ✅ Settings page with profile, notifications, privacy, and appearance tabs
- ✅ Basic artwork and blog models
- ✅ Character/OC management system
- ✅ Badge and achievement system
- ✅ File upload handling for images
- ✅ Responsive CSS styling
- ✅ Requirements.txt with all dependencies

When adding new features:

1. Create feature branch: `git checkout -b feature/<description>`
2. Create Django apps: `python manage.py startapp <app_name>`
3. Add apps to `INSTALLED_APPS` in `settings.py`
4. Follow Django's MVT (Model-View-Template) pattern
5. Create URL patterns in app-specific `urls.py` files
6. Include app URLs in main `urls.py`
7. Use conventional commit messages
8. Follow PR process for code review

## Development Server Access

- **Local URL**: `http://127.0.0.1:8000/`
- **Admin interface**: `http://127.0.0.1:8000/admin/`
- **Default port**: 8000 (Django default)
