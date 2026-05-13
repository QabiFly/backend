import { gql } from "@apollo/client";

// Delivery Mutations
export const updateDeliveryLocationMutation = gql`
  mutation UpdateDeliveryLocation($input: DeliveryLocationUpdateInput!) {
    updateDeliveryLocation(input: $input) {
      id
      latitude
      longitude
      speed
      batteryLevel
      recordedAt
    }
  }
`;

export const acceptDeliveryAssignmentMutation = gql`
  mutation AcceptDeliveryAssignment($input: DeliveryAssignmentAcceptInput!) {
    acceptDeliveryAssignment(input: $input) {
      id
      status
      acceptedAt
    }
  }
`;

export const verifyDeliveryOtpMutation = gql`
  mutation VerifyDeliveryOtp($input: DeliveryAssignmentVerifyOTPInput!) {
    verifyDeliveryOtp(input: $input) {
      id
      status
      otpVerified
    }
  }
`;

// Wallet Mutations
export const topupWalletMutation = gql`
  mutation TopupWallet($walletId: ID!, $input: WalletTopupInput!) {
    topupWallet(walletId: $walletId, input: $input) {
      id
      balance
      pendingBalance
    }
  }
`;

export const withdrawWalletMutation = gql`
  mutation WithdrawWallet($walletId: ID!, $input: WalletWithdrawInput!) {
    withdrawWallet(walletId: $walletId, input: $input) {
      id
      balance
      pendingBalance
    }
  }
`;

export const transferWalletMutation = gql`
  mutation TransferWallet($walletId: ID!, $input: WalletTransferInput!) {
    transferWallet(walletId: $walletId, input: $input) {
      id
      balance
      pendingBalance
    }
  }
`;

// Khata Mutations
export const createUdhaarMutation = gql`
  mutation CreateUdhaar($input: UdhaarCreateInput!) {
    createUdhaar(input: $input) {
      id
      amount
      remaining
      status
      dueDate
    }
  }
`;

export const payUdhaarMutation = gql`
  mutation PayUdhaar($input: UdhaarPayInput!) {
    payUdhaar(input: $input) {
      id
      amount
      paidAmount
      remaining
      status
    }
  }
`;

export const createSundayCollectionMutation = gql`
  mutation CreateSundayCollection($input: SundayCollectionCreateInput!) {
    createSundayCollection(input: $input) {
      id
      amount
      status
      collectionDate
    }
  }
`;

export const collectSundayCollectionMutation = gql`
  mutation CollectSundayCollection($input: SundayCollectionCollectInput!) {
    collectSundayCollection(input: $input) {
      id
      amount
      collectedAmount
      status
      collectedAt
    }
  }
`;
