# saleor - Saleor E-commerce Platform

A modular, high performance, headless e-commerce platform built with Django, GraphQL, React, and Next.js.

## Project Structure

- **backend/** - Django + GraphQL backend API
- **dashboard/** - React admin dashboard
- **storefront/** - Next.js e-commerce storefront

## Quick Start

### Prerequisites

- Node.js 18+ for frontend applications
- Python 3.12+ for backend
- PostgreSQL (for production)
- Redis (for caching and Celery)

### Development Setup

1. **Backend Setup**
   ```bash
   cd backend
   pip install -e .
   cp .env.example .env
   # Edit .env with your configuration
   python manage.py migrate
   python manage.py collectstatic --noinput
   python manage.py populatedb --createsuperuser
   npm run dev
   ```

2. **Dashboard Setup**
   ```bash
   cd dashboard
   pnpm install
   cp .env.template .env
   # Edit .env with your backend URL
   pnpm run dev
   ```

3. **Storefront Setup**
   ```bash
   cd storefront
   npm install
   cp .env.example .env
   # Edit .env with your backend URL
   npm run dev
   ```

## Deployment on Render.com

### Environment Variables

Copy the `.env.render` files in each folder and configure them with your actual values:

#### Backend Environment Variables
- `SECRET_KEY` - Generate a secure random key
- `DATABASE_URL` - PostgreSQL connection string (provided by Render)
- `REDIS_URL` - Redis connection string (provided by Render)
- `ALLOWED_HOSTS` - Your Render app domain
- `FAST2SMS_API_KEY` - SMS service API key

#### Dashboard Environment Variables
- `API_URL` - Backend GraphQL endpoint
- `APP_MOUNT_URI` - Dashboard mount path
- `STATIC_URL` - Static files URL

#### Storefront Environment Variables
- `NEXT_PUBLIC_API_URL` - Backend GraphQL endpoint
- `NEXT_PUBLIC_SITE_URL` - Your storefront domain
- `NEXT_PUBLIC_CHANNEL_SLUG` - Default sales channel

### Using render.yaml

1. Push your code to GitHub
2. Connect your repository to Render.com
3. Render will automatically detect and deploy all services using `render.yaml`

### Manual Deployment

1. **Backend Service**
   - Runtime: Python
   - Build Command: `pip install -e . && python manage.py collectstatic --noinput`
   - Start Command: `uvicorn saleor.asgi:application --host 0.0.0.0 --port $PORT`

2. **Dashboard Service**
   - Runtime: Node
   - Build Command: `pnpm install && pnpm run build`
   - Start Command: `pnpm run start`

3. **Storefront Service**
   - Runtime: Node
   - Build Command: `npm install && npm run build`
   - Start Command: `npm run start`

## Service URLs After Deployment

- Backend: `https://your-backend-app.onrender.com/graphql/`
- Dashboard: `https://your-dashboard-app.onrender.com/dashboard/`
- Storefront: `https://your-storefront-app.onrender.com/`

## Default Credentials

After running `populatedb`:
- Email: `admin@example.com`
- Password: `admin`

## saleor Configuration

The platform is pre-configured for rural Indian markets:

- **Platform Name**: saleor
- **Tagline**: Apna Gaon, Apna Bazaar
- **Location**: Reoti, Ballia, Uttar Pradesh
- **Delivery Radius**: 2.0 km
- **Minimum Order for Free Delivery**: ₹50
- **Platform Commission**: 5%
- **Delivery Commission**: 3%
- **Credit Limit**: ₹20,000

## Features

- Multi-vendor marketplace
- Local delivery management
- Credit (Udhaar) system
- SMS OTP authentication
- Real-time inventory management
- Order tracking
- Payment gateway integration
- Admin dashboard
- Mobile-responsive storefront

## Support

For issues and support:
- Check the [Saleor Documentation](https://docs.saleor.io/)
- Review environment variable configurations
- Ensure all services are properly connected

## License

BSD-3-Clause License
