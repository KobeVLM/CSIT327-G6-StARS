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
- **Main app**: `stars/` (Django project configuration)
- **Working directory**: Always operate from `stars_project/` when running Django commands

## Key Architecture Patterns

### Django Project Layout

```
CSIT327-G6-StARS/
├── README.md                # Project documentation
├── requirements.txt         # Python dependencies
├── .github/
│   └── copilot-instructions.md
└── stars_project/
    ├── manage.py            # Django management script
    ├── venv/               # Virtual environment (local only)
    ├── media/              # User-uploaded files (avatars, artwork)
    ├── static/             # CSS, JS, images
    │   └── css/            # Stylesheets for different pages
    ├── templates/          # HTML templates
    │   ├── base/           # Base templates and navigation
    │   └── accounts/       # User-related templates
    ├── accounts/           # Main application (users, profiles, content)
    │   ├── models.py       # User profiles, artwork, blogs, comments
    │   ├── views.py        # Authentication, profiles, content management
    │   ├── forms.py        # User input forms
    │   └── urls.py         # App URL routing
    └── stars/              # Django project configuration
        ├── settings.py     # Project settings
        ├── urls.py         # Main URL routing
        ├── wsgi.py         # WSGI application
        └── asgi.py         # ASGI application
```

### Development Environment Setup

- **Virtual environment**: Located at `stars_project/venv/`
- **Activation**: Use `venv\Scripts\Activate.ps1` on Windows
- **Dependencies**: Install with `pip install -r requirements.txt`
- **Required packages**: Django, Pillow (for image handling), psycopg2-binary, python-dotenv
- **Database setup**: Run `python manage.py migrate` before first use
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

### Settings Configuration

- **Secret key**: Uses Django's insecure default (needs updating for production)
- **Database**: SQLite with default configuration
- **Static files**: Standard Django setup with `STATIC_URL = 'static/'`
- **Media files**: Configured for user uploads at `MEDIA_URL = '/media/'`
- **Templates**: Located in `templates/` directory with app-specific subdirectories

### URL Patterns

- Main URL configuration in `stars/urls.py`
- App URLs in `accounts/urls.py` for authentication and profile features
- Current routes: login, register, profile, settings, artwork upload, blogs

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
