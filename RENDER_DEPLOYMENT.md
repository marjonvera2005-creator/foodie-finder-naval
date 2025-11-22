# Deploying Foodie Finder to Render

## Prerequisites
1. GitHub account with your code pushed to a repository
2. Render account (free tier available)

## Deployment Steps

### Method 1: Using Render Dashboard (Recommended)

1. **Push your code to GitHub**
   ```bash
   git add .
   git commit -m "Prepare for Render deployment"
   git push origin main
   ```

2. **Create a new Web Service on Render**
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select your foodie-finder repository

3. **Configure the service**
   - **Name**: `foodie-finder` (or your preferred name)
   - **Environment**: `Python 3`
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn foodie_finder.wsgi --log-file -`

4. **Set Environment Variables**
   Add these in the Environment section:
   ```
   DJANGO_SETTINGS_MODULE=foodie_finder.settings_production
   SECRET_KEY=your-super-secret-key-here-change-this-to-something-random
   DEBUG=False
   ALLOWED_HOSTS=your-app-name.onrender.com
   ```

5. **Create PostgreSQL Database**
   - In Render Dashboard, click "New +" → "PostgreSQL"
   - Name: `foodie-finder-db`
   - After creation, copy the "Internal Database URL"
   - Add it as environment variable: `DATABASE_URL=<your-database-url>`

6. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment to complete (5-10 minutes)

### Method 2: Using render.yaml (Infrastructure as Code)

1. **Push code with render.yaml**
   ```bash
   git add .
   git commit -m "Add render.yaml for deployment"
   git push origin main
   ```

2. **Create service from render.yaml**
   - In Render Dashboard, click "New +" → "Blueprint"
   - Connect your repository
   - Render will automatically detect render.yaml

### Post-Deployment Steps

1. **Create superuser** (via Render Shell)
   - Go to your service → Shell tab
   - Run: `python manage.py createsuperuser`

2. **Access your app**
   - Your app will be available at: `https://your-app-name.onrender.com`
   - Admin panel: `https://your-app-name.onrender.com/admin/`

## Important Notes

- **Free tier limitations**: 
  - App sleeps after 15 minutes of inactivity
  - 750 hours/month limit
  - Database has 1GB storage limit

- **Static files**: Handled by WhiteNoise (already configured)

- **Media files**: For production, consider using cloud storage (AWS S3, Cloudinary)

- **Environment variables**: Never commit sensitive data to Git

## Troubleshooting

### Common Issues:

1. **Build fails**: Check build logs for missing dependencies
2. **App won't start**: Verify DJANGO_SETTINGS_MODULE is correct
3. **Static files missing**: Ensure `python manage.py collectstatic` runs in build
4. **Database errors**: Verify DATABASE_URL is set correctly

### Useful Commands (via Render Shell):
```bash
# Check logs
python manage.py check

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic
```

## Security Checklist

- ✅ DEBUG=False in production
- ✅ Strong SECRET_KEY
- ✅ ALLOWED_HOSTS configured
- ✅ Database URL secured
- ✅ Static files served via WhiteNoise
- ⚠️ Consider HTTPS redirects for production
- ⚠️ Consider cloud storage for media files

Your Foodie Finder app should now be live on Render! 🚀