# StARS Deployment Guide

## Prerequisites

1. **Supabase Account**: Sign up at [supabase.com](https://supabase.com)
2. **Render Account**: Sign up at [render.com](https://render.com)
3. **GitHub Repository**: Your code should be in a GitHub repository

## Step 1: Set up Supabase Database

1. Create a new project in Supabase
2. Go to **Settings > Database**
3. Copy your connection string (it looks like):
   ```
   postgresql://postgres:[PASSWORD]@db.[PROJECT_REF].supabase.co:5432/postgres
   ```
4. Save this URL - you'll need it for Render

## Step 2: Generate a Secret Key

Run this command to generate a secure secret key:

```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## Step 3: Deploy to Render

### 3.1 Create Web Service

1. Go to [render.com](https://render.com) and click "New +"
2. Select "Web Service"
3. Connect your GitHub repository
4. Configure the service:

**Basic Settings:**
- **Name**: `stars-app` (or your preferred name)
- **Environment**: `Python 3`
- **Build Command**: `./build.sh`
- **Start Command**: `gunicorn stars.wsgi:application`

**Advanced Settings:**
- **Root Directory**: `stars_project`

### 3.2 Environment Variables

Add these environment variables in Render:

```bash
# Required Variables
DEBUG=False
SECRET_KEY=your-generated-secret-key-here
DATABASE_URL=your-supabase-connection-string
ALLOWED_HOSTS=your-app-name.onrender.com

# Security Settings (optional but recommended)
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
```

### 3.3 Deploy

1. Click "Create Web Service"
2. Render will automatically build and deploy your app
3. Wait for the build to complete (usually 3-5 minutes)

## Step 4: Post-Deployment Setup

After successful deployment, you may need to:

1. **Create a superuser** (run in Render Shell):
   ```bash
   python manage.py createsuperuser
   ```

2. **Create sample data** (optional):
   ```bash
   python manage.py create_sample_data
   ```

## Step 5: Domain Configuration

1. In Render, go to your service settings
2. Add custom domain if needed
3. Update `ALLOWED_HOSTS` environment variable to include your domain

## Environment Variables Reference

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `DEBUG` | Debug mode (False for production) | `False` |
| `SECRET_KEY` | Django secret key | `your-generated-key` |
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://...` |
| `ALLOWED_HOSTS` | Comma-separated allowed hosts | `myapp.onrender.com` |

### Optional Security Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SECURE_SSL_REDIRECT` | Force HTTPS redirect | `True` |
| `SECURE_HSTS_SECONDS` | HSTS max age | `31536000` |

## Local Development

For local development, create a `.env` file in the `stars_project` directory:

```bash
# Copy from .env.production.example and modify
cp .env.production.example .env

# Edit .env with your local settings
DEBUG=True
SECRET_KEY=your-dev-secret-key
DATABASE_URL=mysql://user:pass@localhost/stars_db
ALLOWED_HOSTS=127.0.0.1,localhost
```

## Troubleshooting

### Common Issues

1. **Build fails**: Check that all requirements are in `requirements.txt`
2. **Database connection fails**: Verify DATABASE_URL format
3. **Static files not loading**: Ensure WhiteNoise is properly configured
4. **Permission denied on build.sh**: File should be executable

### Debugging

1. Check Render logs in the dashboard
2. Use Render Shell to run Django management commands
3. Test database connection with:
   ```bash
   python manage.py dbshell
   ```

## Security Best Practices

1. **Never commit `.env` files** to version control
2. **Use strong secret keys** (generate new ones for production)
3. **Keep DEBUG=False** in production
4. **Use environment variables** for all sensitive data
5. **Enable HTTPS** security headers
6. **Regularly update dependencies**

## File Structure After Setup

```
stars_project/
├── .env                          # Local environment (don't commit)
├── .env.production.example       # Template for production
├── build.sh                      # Render build script
├── Procfile                      # Process configuration
├── runtime.txt                   # Python version
├── requirements.txt              # Dependencies
├── manage.py
└── stars/
    └── settings.py               # Updated for production
```

## Next Steps

1. Set up monitoring and error tracking
2. Configure backup strategies for your database
3. Set up CI/CD pipelines
4. Configure custom domain and SSL
5. Set up email service for notifications
