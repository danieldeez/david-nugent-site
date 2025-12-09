# Deployment Guide for Render.com

This guide walks you through deploying the David Nugent BL Django website to Render.com.

## Prerequisites

1. A GitHub account
2. A Render.com account (free tier available)
3. Your environment variable values ready (SECRET_KEY, API keys, etc.)

## Step 1: Generate a New SECRET_KEY

**IMPORTANT:** Do not use the default SECRET_KEY in production!

Generate a new secret key using Python:

```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Save this value - you'll need it for Render environment variables.

## Step 2: Push to GitHub

1. **Initialize Git repository** (if not already done):
   ```bash
   git init
   git add .
   git commit -m "Initial commit - prepare for deployment"
   ```

2. **Create a new repository on GitHub**:
   - Go to https://github.com/new
   - Name it (e.g., "barrister-site")
   - Do NOT initialize with README (we already have files)
   - Click "Create repository"

3. **Push your code**:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/barrister-site.git
   git branch -M main
   git push -u origin main
   ```

## Step 3: Create Render Web Service

1. **Log in to Render**: https://dashboard.render.com/

2. **Create New Web Service**:
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select your `barrister-site` repository

3. **Configure the service**:
   - **Name**: `david-nugent-bl` (or your choice)
   - **Region**: Choose closest to your users
   - **Branch**: `main`
   - **Runtime**: `Python 3`
   - **Build Command**: `bash build.sh`
   - **Start Command**: `gunicorn core.wsgi:application --log-file -`
   - **Instance Type**: Free (or paid for better performance)

## Step 4: Add Environment Variables

In the Render dashboard, scroll to "Environment Variables" and add:

### Required Variables:

```
SECRET_KEY=<your-generated-secret-key-from-step-1>
DEBUG=False
ALLOWED_HOSTS=your-app-name.onrender.com
```

### Optional but Recommended:

```
LLM_BASE_URL=https://api.deepseek.com
LLM_API_KEY=<your-llm-api-key>
LLM_MODEL=deepseek-chat
ASSISTANT_ENABLED=1
CALENDLY_SIGNING_KEY=<your-calendly-key>
```

**Note**: After your first deploy, you'll get the actual Render URL. Update `ALLOWED_HOSTS` to include it.
Example: `ALLOWED_HOSTS=david-nugent-bl.onrender.com`

You can also add multiple hosts separated by commas:
`ALLOWED_HOSTS=david-nugent-bl.onrender.com,www.yourcustomdomain.com`

## Step 5: Deploy

1. Click "Create Web Service"
2. Render will automatically:
   - Clone your repository
   - Install dependencies from `requirements.txt`
   - Run `build.sh` (collectstatic + migrate)
   - Start the application with gunicorn

3. **Monitor the build logs** for any errors

4. Once complete, you'll see a URL like: `https://david-nugent-bl.onrender.com`

## Step 6: Verify Deployment

1. Visit your Render URL
2. Check that:
   - Static files load (CSS, images)
   - Pages render correctly
   - Owner login works at `/site-access-dk2847/`
   - AI assistant works (if enabled)

## Step 7: Add Custom Domain (Optional)

1. In Render dashboard, go to Settings → Custom Domains
2. Add your domain (e.g., `davidnugent.ie`)
3. Follow Render's DNS configuration instructions
4. Update `ALLOWED_HOSTS` environment variable to include your domain

## Troubleshooting

### Static Files Not Loading
- Check that `collectstatic` ran successfully in build logs
- Verify `STATIC_ROOT` is set in settings.py
- Ensure WhiteNoise middleware is enabled

### Database Errors
- Check that migrations ran in build logs
- Render provides a PostgreSQL addon if you need it (SQLite works for small sites)

### 500 Internal Server Error
- Check Render logs: Dashboard → Logs
- Verify all environment variables are set correctly
- Ensure `DEBUG=False` and `ALLOWED_HOSTS` includes your Render domain

### Owner Login Not Working
- URL is: `https://your-domain.onrender.com/site-access-dk2847/`
- Check that migrations ran successfully
- Create superuser if needed (via Render Shell)

## Creating a Superuser on Render

To create an admin user:

1. In Render dashboard, go to your service
2. Click "Shell" in the top navigation
3. Run:
   ```bash
   python manage.py createsuperuser
   ```
4. Follow the prompts

## Important Notes

- **Database**: The SQLite database will reset on each deploy. For production, consider Render's PostgreSQL addon.
- **Media Files**: Uploaded files (images) won't persist with SQLite. Use cloud storage (AWS S3, Cloudflare R2) for production.
- **Free Tier**: Render's free tier spins down after 15 minutes of inactivity. First request after may be slow.
- **Logs**: Always check logs when troubleshooting: Dashboard → Your Service → Logs

## Maintenance

### Updating the Site

1. Make changes locally
2. Test thoroughly
3. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Description of changes"
   git push
   ```
4. Render will automatically redeploy

### Manual Redeploy

In Render dashboard → Manual Deploy → "Deploy latest commit"

## Security Checklist

- ✅ `DEBUG=False` in production
- ✅ Strong `SECRET_KEY` (50+ random characters)
- ✅ `ALLOWED_HOSTS` properly configured
- ✅ `.env` file NOT committed to Git
- ✅ HTTPS enabled (automatic on Render)
- ✅ Regular Django/dependency updates

## Support

- Render Documentation: https://render.com/docs
- Django Deployment Checklist: https://docs.djangoproject.com/en/stable/howto/deployment/checklist/
