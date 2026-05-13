import gql from "graphql-tag";

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

// Wallet Queries
export const myWalletQuery = gql`
  query MyWallet {
    myWallet {
      id
      balance
      pendingBalance
      totalEarned
      totalWithdrawn
      upiId
      isActive
      availableBalance
    }
  }
`;

export const myTransactionsQuery = gql`
  query MyTransactions {
    myTransactions {
      id
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
export const myUdhaarQuery = gql`
  query MyUdhaar {
    myUdhaar {
      id
      amount
      paidAmount
      remaining
      dueDate
      isOverdue
      status
      createdAt
      updatedAt
      order {
        id
        number
      }
    }
  }
`;

export const mySundayCollectionsQuery = gql`
  query MySundayCollections {
    mySundayCollections {
      id
      amount
      collectedAmount
      status
      collectionDate
      collectedAt
      notes
      createdAt
      udhaar {
        id
        amount
        remaining
      }
    }
  }
`;
