import { gql } from "@apollo/client";

// Delivery Queries
export const liveDeliveriesQuery = gql`
  query LiveDeliveries {
    liveDeliveries {
      id
      deliveryBoy {
        id
        email
        firstName
        lastName
      }
      order {
        id
        number
      }
      latitude
      longitude
      speed
      batteryLevel
      recordedAt
    }
  }
`;

export const deliveryAssignmentsQuery = gql`
  query DeliveryAssignments {
    deliveryAssignments {
      id
      order {
        id
        number
      }
      deliveryBoy {
        id
        email
        firstName
        lastName
      }
      status
      deliveryOtp
      otpVerified
      assignedAt
      acceptedAt
      deliveredAt
    }
  }
`;

// Wallet Queries
export const allWalletsQuery = gql`
  query AllWallets($first: Int, $after: String) {
    wallets(first: $first, after: $after) {
      edges {
        node {
          id
          user {
            id
            email
            firstName
            lastName
          }
          balance
          pendingBalance
          totalEarned
          totalWithdrawn
          upiId
          isActive
          createdAt
        }
      }
      pageInfo {
        hasNextPage
        hasPreviousPage
        endCursor
        startCursor
      }
    }
  }
`;

export const walletTransactionsQuery = gql`
  query WalletTransactions($walletId: ID!) {
    walletTransactions(walletId: $walletId) {
      id
      wallet {
        id
        user {
          email
        }
      }
      amount
      transactionType
      purpose
      balanceAfter
      description
      status
      createdAt
      order {
        id
        number
      }
    }
  }
`;

// Khata Queries
export const allUdhaarQuery = gql`
  query AllUdhaar($first: Int, $after: String) {
    udhaars(first: $first, after: $after) {
      edges {
        node {
          id
          user {
            id
            email
            firstName
            lastName
          }
          shop {
            id
            name
          }
          order {
            id
            number
          }
          amount
          paidAmount
          remaining
          dueDate
          isOverdue
          status
          createdAt
          updatedAt
        }
      }
      pageInfo {
        hasNextPage
        hasPreviousPage
        endCursor
        startCursor
      }
    }
  }
`;

export const sundayCollectionsQuery = gql`
  query SundayCollections {
    sundayCollections {
      id
      deliveryBoy {
        id
        email
        firstName
        lastName
      }
      user {
        id
        email
        firstName
        lastName
      }
      udhaar {
        id
        amount
        remaining
      }
      amount
      collectedAmount
      status
      collectionDate
      collectedAt
      notes
      createdAt
    }
  }
`;
