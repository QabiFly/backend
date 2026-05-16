# saleor Render Deployment Guide

This guide explains how to deploy the saleor e-commerce platform (backend, storefront, and dashboard) to Render.com.

## Prerequisites

- A Render.com account (free tier available)
- GitHub account with the saleor repository
- AWS S3 bucket for media storage (optional but recommended)
- PostgreSQL database (provided by Render)
- Redis instance (provided by Render)

## Architecture Overview

The saleor platform consists of three separate services:

1. **Backend** (Django/Saleor) - GraphQL API server
2. **Storefront** (Next.js) - Customer-facing e-commerce application
3. **Dashboard** (React/Vite) - Admin panel for store management

## Deployment Steps

### 1. Prepare Your Repository

Ensure your repository structure is:

```
saleor/
├── backend/
│   ├── .gitignore
│   ├── render.yaml
│   ├── requirements.txt
│   └── ...
├── storefront/
│   ├── .gitignore
│   ├── render.yaml
│   └── ...
└── dashboard/
│   ├── .gitignore
│   ├── render.yaml
│   └── ...
```

### 2. Deploy Backend

#### 2.1 Create PostgreSQL Database

1. Go to Render Dashboard → New → PostgreSQL
2. Name: `saleor-db`
3. Database: `saleor`
4. User: `saleor_user`
5. Region: Choose nearest to your users
6. Plan: Free tier (or paid for production)
7. Click "Create Database"

#### 2.2 Create Redis Instance

1. Go to Render Dashboard → New → Redis
2. Name: `saleor-redis`
3. Region: Same as database
4. Plan: Free tier
5. Click "Create Redis"

#### 2.3 Deploy Backend Service

1. Go to Render Dashboard → New → Web Service
2. Connect your GitHub repository
3. Select the `backend` directory as root
4. Render will auto-detect the `render.yaml` file
5. Review the configuration:
   - **Name**: saleor-backend
   - **Environment**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn saleor.wsgi:application`
6. Add Environment Variables:
   - `DATABASE_URL`: Auto-linked from PostgreSQL
   - `REDIS_URL`: Auto-linked from Redis
   - `SECRET_KEY`: Generate a secure random string
   - `ALLOWED_HOSTS`: `saleor-backend.onrender.com`
   - `DEBUG`: `false`
   - `DEFAULT_FILE_STORAGE`: `storages.backends.s3boto3.S3Boto3Storage`
   - `AWS_STORAGE_BUCKET_NAME`: Your S3 bucket name
   - `AWS_S3_REGION_NAME`: `us-east-1` (or your region)
   - `AWS_ACCESS_KEY_ID`: Your AWS access key
   - `AWS_SECRET_ACCESS_KEY`: Your AWS secret key
   - `AWS_S3_CUSTOM_DOMAIN`: Your S3 bucket domain
7. Click "Deploy Web Service"

#### 2.4 Run Migrations

After deployment, you'll need to run migrations:

1. Go to your backend service on Render
2. Click "Shell" tab
3. Run: `python manage.py migrate`
4. Run: `python manage.py createsuperuser` (create admin account)
5. Run: `python manage.py collectstatic --noinput`

### 3. Deploy Storefront

#### 3.1 Deploy Storefront Service

1. Go to Render Dashboard → New → Web Service
2. Connect your GitHub repository
3. Select the `storefront` directory as root
4. Render will auto-detect the `render.yaml` file
5. Review the configuration:
   - **Name**: saleor-storefront
   - **Environment**: Node
   - **Build Command**: `npm run build`
   - **Start Command**: `npm start`
6. Add Environment Variables:
   - `NEXT_PUBLIC_API_URI`: `https://saleor-backend.onrender.com/graphql/`
   - `NEXT_PUBLIC_API_URL`: `https://saleor-backend.onrender.com/graphql/`
   - `NODE_ENV`: `production`
7. Click "Deploy Web Service"

### 4. Deploy Dashboard

#### 4.1 Deploy Dashboard Service

1. Go to Render Dashboard → New → Web Service
2. Connect your GitHub repository
3. Select the `dashboard` directory as root
4. Render will auto-detect the `render.yaml` file
5. Review the configuration:
   - **Name**: saleor-dashboard
   - **Environment**: Node
   - **Build Command**: `pnpm run build`
   - **Start Command**: `pnpm run start`
6. Add Environment Variables:
   - `API_URL`: `https://saleor-backend.onrender.com/graphql/`
   - `APP_MOUNT_URI`: `/`
   - `LOCALE_CODE`: `"EN"`
   - `FF_USE_STAGING_SCHEMA`: `false`
   - `BASE_URL`: `https://saleor-dashboard.onrender.com/`
   - `NODE_ENV`: `production`
7. Click "Deploy Web Service"

## Environment Variables Reference

### Backend Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `DATABASE_URL` | PostgreSQL connection string | Yes |
| `REDIS_URL` | Redis connection string | Yes |
| `SECRET_KEY` | Django secret key | Yes |
| `ALLOWED_HOSTS` | Allowed hostnames | Yes |
| `DEBUG` | Debug mode | Yes |
| `DEFAULT_FILE_STORAGE` | Storage backend | Yes |
| `AWS_STORAGE_BUCKET_NAME` | S3 bucket name | Yes |
| `AWS_S3_REGION_NAME` | AWS region | Yes |
| `AWS_ACCESS_KEY_ID` | AWS access key | Yes |
| `AWS_SECRET_ACCESS_KEY` | AWS secret key | Yes |
| `AWS_S3_CUSTOM_DOMAIN` | S3 custom domain | Yes |

### Storefront Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `NEXT_PUBLIC_API_URI` | Backend GraphQL API URL | Yes |
| `NEXT_PUBLIC_API_URL` | Backend GraphQL API URL | Yes |
| `NODE_ENV` | Node environment | Yes |

### Dashboard Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `API_URL` | Backend GraphQL API URL | Yes |
| `APP_MOUNT_URI` | Application mount URI | Yes |
| `LOCALE_CODE` | Locale code | Yes |
| `FF_USE_STAGING_SCHEMA` | Use staging schema | Yes |
| `BASE_URL` | Dashboard base URL | Yes |
| `NODE_ENV` | Node environment | Yes |

## Post-Deployment Configuration

### 1. Configure Saleor

1. Access dashboard at `https://saleor-dashboard.onrender.com`
2. Login with superuser account created during migration
3. Configure channels, payment gateways, shipping methods, tax settings

### 2. Configure saleor Features

1. Create delivery boys in the system
2. Set up wallet initial balances
3. Configure khata/credit rules
4. Set up Sunday collection schedules

### 3. Test Integration

1. Access storefront at `https://saleor-storefront.onrender.com`
2. Test user registration, product browsing, checkout
3. Test delivery tracking, wallet operations, khata/credit system

## Troubleshooting

### Backend Issues

**Database connection errors**: Verify DATABASE_URL is correctly linked and PostgreSQL is running

**Static files not loading**: Run `python manage.py collectstatic --noinput` and verify AWS S3 configuration

**GraphQL schema errors**: Ensure all custom apps are installed and run migrations

### Frontend Issues

**Cannot connect to backend**: Verify API URLs are correct and backend service is running

**Build errors**: Check package.json dependencies and Node version compatibility

## Cost Estimate (Free Tier)

- PostgreSQL: Free tier (90 days, then $7/month)
- Redis: Free tier
- Web Services: Free tier (750 hours/month)
- Total: $0/month initially, ~$7/month after 90 days

## Next Steps

After deployment:
1. Set up custom domain names
2. Configure SSL certificates (automatic on Render)
3. Set up monitoring and alerts
4. Configure backup strategies
5. Set up CI/CD pipeline
