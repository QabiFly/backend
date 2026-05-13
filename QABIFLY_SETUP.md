# QabiFly Storefront and Dashboard Setup Guide

This guide explains how to set up and use the QabiFly storefront and dashboard with the custom backend features including delivery tracking, wallet management, and khata (credit) system.

## Overview

QabiFly is a custom e-commerce platform built on Saleor with additional features:
- **Delivery Tracking**: Real-time delivery boy location tracking and assignment management
- **Wallet System**: Digital wallet for users with top-up, withdrawal, and transfer functionality
- **Khata (Credit) System**: Traditional credit book system for customers with Sunday collections

## Prerequisites

- Node.js >= 18 (for storefront)
- Node.js >= 24 (for dashboard)
- Python 3.8+ (for backend)
- PostgreSQL database
- Redis (for caching)

## Backend Setup

The backend is a Saleor-based Django application with custom apps.

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Copy the example environment file:
```bash
cp .env.example .env
```

Edit `.env` with your database and Redis configuration.

### 3. Run Migrations

```bash
python manage.py migrate
```

### 4. Create Superuser

```bash
python manage.py createsuperuser
```

### 5. Start the Backend Server

```bash
python manage.py runserver
```

The backend GraphQL API will be available at `http://localhost:8000/graphql/`

## Storefront Setup

The storefront is a Next.js-based React application.

### 1. Install Dependencies

```bash
cd storefront
npm install
```

### 2. Configure Environment Variables

The storefront uses the `.env.local` file which has been configured to connect to the local backend:

```
NEXT_PUBLIC_API_URI=http://localhost:8000/graphql/
NEXT_PUBLIC_API_URL=http://localhost:8000/graphql/
```

### 3. Start the Development Server

```bash
npm run dev
```

The storefront will be available at `http://localhost:3000`

### 4. Build for Production

```bash
npm run build
npm start
```

## Dashboard Setup

The dashboard is a React/Vite application.

### 1. Install Dependencies

```bash
cd dashboard
pnpm install
```

### 2. Configure Environment Variables

The dashboard uses the `.env.local` file which has been configured to connect to the local backend:

```
API_URL=http://localhost:8000/graphql/
APP_MOUNT_URI=/
LOCALE_CODE="EN"
FF_USE_STAGING_SCHEMA=false
BASE_URL=http://localhost:9000/
```

### 3. Generate GraphQL Types

```bash
pnpm run generate
```

### 4. Start the Development Server

```bash
pnpm run dev
```

The dashboard will be available at `http://localhost:9000`

### 5. Build for Production

```bash
pnpm run build
pnpm run start
```

## QabiFly Features

### Storefront Features

#### 1. Delivery Tracking
- **Location**: `/account/delivery-tracking`
- **Features**: Real-time delivery boy location tracking with 5-second polling
- **Access**: Available to authenticated users

#### 2. Wallet Management
- **Location**: `/account/wallet`
- **Features**: 
  - View wallet balance and transaction history
  - Top-up wallet using UPI
  - Withdraw funds to UPI ID
- **Access**: Available to authenticated users

#### 3. Khata (Credit) System
- **Location**: `/account/khata`
- **Features**:
  - View udhaar (credit) records
  - View Sunday collection history
  - Pay udhaar amounts online
- **Access**: Available to authenticated users

### Dashboard Features

#### 1. Delivery Management
- **Location**: `/qabifly/delivery`
- **Features**:
  - View live delivery locations
  - Manage delivery assignments
  - Track delivery status and OTP verification
- **Access**: Admin and staff users

#### 2. Wallet Management
- **Location**: `/qabifly/wallet`
- **Features**:
  - View all user wallets
  - Top-up user wallets
  - Process withdrawals
  - View transaction history
- **Access**: Admin and staff users

#### 3. Khata Management
- **Location**: `/qabifly/khata`
- **Features**:
  - View all udhaar records
  - Create new udhaar entries
  - Manage Sunday collections
  - Process payments
- **Access**: Admin and staff users

## GraphQL API

The backend extends Saleor's GraphQL API with custom queries and mutations:

### Delivery Queries
```graphql
query {
  liveDeliveries {
    id
    deliveryBoy { id email firstName lastName }
    order { id number }
    latitude longitude speed batteryLevel
    recordedAt
  }
}
```

### Wallet Queries
```graphql
query {
  myWallet {
    id balance pendingBalance totalEarned totalWithdrawn
    upiId isActive availableBalance
  }
  myTransactions {
    id amount transactionType purpose
    balanceAfter description status
    createdAt
  }
}
```

### Khata Queries
```graphql
query {
  myUdhaar {
    id amount paidAmount remaining
    dueDate isOverdue status
    createdAt updatedAt
  }
  mySundayCollections {
    id amount collectedAmount status
    collectionDate collectedAt notes
  }
}
```

### Mutations

Delivery:
- `updateDeliveryLocation`
- `acceptDeliveryAssignment`
- `verifyDeliveryOtp`

Wallet:
- `topupWallet`
- `withdrawWallet`
- `transferWallet`

Khata:
- `createUdhaar`
- `payUdhaar`
- `createSundayCollection`
- `collectSundayCollection`

## File Structure

### Storefront
```
storefront/
├── src/
│   ├── @next/graphql/
│   │   ├── qabiflyQueries.ts      # QabiFly GraphQL queries
│   │   └── qabiflyMutations.ts    # QabiFly GraphQL mutations
│   └── pages/account/
│       ├── delivery-tracking.tsx  # Delivery tracking page
│       ├── wallet.tsx             # Wallet management page
│       └── khata.tsx             # Khata management page
└── .env.local                     # Environment configuration
```

### Dashboard
```
dashboard/
├── src/
│   └── qabifly/
│       ├── queries.ts             # QabiFly GraphQL queries
│       ├── mutations.ts           # QabiFly GraphQL mutations
│       ├── DeliveryPage.tsx       # Delivery management page
│       ├── WalletPage.tsx         # Wallet management page
│       └── KhataPage.tsx          # Khata management page
└── .env.local                     # Environment configuration
```

### Backend
```
backend/
├── delivery/                      # Delivery app
│   ├── models.py                  # Delivery models
│   ├── graphql/
│   │   ├── queries.py            # Delivery queries
│   │   └── mutations.py          # Delivery mutations
│   └── types.py                  # GraphQL types
├── wallet/                        # Wallet app
│   ├── models.py                  # Wallet models
│   └── graphql/
│       ├── queries.py            # Wallet queries
│       └── mutations.py          # Wallet mutations
├── khata/                         # Khata app
│   ├── models.py                  # Khata models
│   └── graphql/
│       ├── queries.py            # Khata queries
│       └── mutations.py          # Khata mutations
└── qabifly_graphql/
    └── schema.py                 # Combined GraphQL schema
```

## Troubleshooting

### Storefront Issues

**Problem**: Cannot connect to backend
**Solution**: Ensure backend is running at `http://localhost:8000/graphql/` and check `.env.local` configuration

**Problem**: GraphQL errors
**Solution**: Run `npm run codegen` to regenerate GraphQL types

### Dashboard Issues

**Problem**: Cannot connect to backend
**Solution**: Ensure backend is running and check `.env.local` configuration

**Problem**: GraphQL types missing
**Solution**: Run `pnpm run generate` to regenerate GraphQL types

### Backend Issues

**Problem**: Database connection errors
**Solution**: Check PostgreSQL is running and credentials in `.env` are correct

**Problem**: GraphQL schema not loading
**Solution**: Ensure all migrations have been run and custom apps are installed

## Development Tips

1. **Hot Reload**: Both storefront and dashboard support hot reload during development
2. **GraphQL Playground**: Access at `http://localhost:8000/graphql/` to test queries
3. **Polling**: Delivery tracking uses 5-second polling for real-time updates
4. **Error Handling**: All components include error handling with user-friendly messages

## Security Considerations

- All mutations require appropriate permissions
- OTP verification for delivery completion
- Wallet transactions are logged with audit trail
- Khata records include due date tracking for overdue payments

## Support

For issues or questions:
1. Check the Saleor documentation at https://docs.saleor.io
2. Review the backend models in `delivery/`, `wallet/`, and `khata/` apps
3. Test GraphQL queries in the GraphQL Playground
4. Check browser console for frontend errors

## License

This project extends Saleor, which is BSD-3-Clause licensed.
