import React, { useState } from "react";
import { useQuery, useMutation } from "react-apollo";
import { myWalletQuery, myTransactionsQuery } from "@next/graphql/qabiflyQueries";
import { topupWalletMutation, withdrawWalletMutation } from "@next/graphql/qabiflyMutations";
import { Container, Typography, Box, Button, TextField, CircularProgress, Alert, Card, CardContent, Grid, Tabs, Tab } from "@material-ui/core";
import styled from "styled-components";

const WalletContainer = styled(Container)`
  padding: 2rem 0;
`;

const WalletCard = styled(Card)`
  margin-bottom: 2rem;
`;

const TransactionCard = styled(Card)`
  margin-bottom: 1rem;
`;

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;
  return (
    <div role="tabpanel" hidden={value !== index} {...other}>
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );
}

const WalletPage = () => {
  const [tabValue, setTabValue] = useState(0);
  const [topupAmount, setTopupAmount] = useState("");
  const [withdrawAmount, setWithdrawAmount] = useState("");
  const [upiId, setUpiId] = useState("");

  const { data: walletData, loading: walletLoading, error: walletError, refetch: refetchWallet } = useQuery(myWalletQuery);
  const { data: transactionsData, loading: transactionsLoading, error: transactionsError } = useQuery(myTransactionsQuery);

  const [topupWallet, { loading: topupLoading }] = useMutation(topupWalletMutation, {
    onCompleted: () => {
      refetchWallet();
      setTopupAmount("");
    },
  });

  const [withdrawWallet, { loading: withdrawLoading }] = useMutation(withdrawWalletMutation, {
    onCompleted: () => {
      refetchWallet();
      setWithdrawAmount("");
      setUpiId("");
    },
  });

  const handleTopup = () => {
    if (!topupAmount) return;
    topupWallet({
      variables: {
        input: {
          amount: parseFloat(topupAmount),
          method: "UPI",
        },
      },
    });
  };

  const handleWithdraw = () => {
    if (!withdrawAmount || !upiId) return;
    withdrawWallet({
      variables: {
        input: {
          amount: parseFloat(withdrawAmount),
          upiId,
        },
      },
    });
  };

  if (walletLoading) {
    return (
      <WalletContainer>
        <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
          <CircularProgress />
        </Box>
      </WalletContainer>
    );
  }

  if (walletError) {
    return (
      <WalletContainer>
        <Alert severity="error">Error loading wallet data: {walletError.message}</Alert>
      </WalletContainer>
    );
  }

  const wallet = walletData?.myWallet;
  const transactions = transactionsData?.myTransactions || [];

  return (
    <WalletContainer maxWidth="lg">
      <Typography variant="h4" gutterBottom>
        My Wallet
      </Typography>

      <WalletCard>
        <CardContent>
          <Grid container spacing={3}>
            <Grid item xs={12} sm={6}>
              <Typography variant="h6" color="primary">
                Available Balance
              </Typography>
              <Typography variant="h3">
                ₹{wallet?.availableBalance?.toFixed(2) || "0.00"}
              </Typography>
            </Grid>
            <Grid item xs={12} sm={6}>
              <Typography variant="body2" color="textSecondary">
                Total Balance: ₹{wallet?.balance?.toFixed(2) || "0.00"}
              </Typography>
              <Typography variant="body2" color="textSecondary">
                Pending: ₹{wallet?.pendingBalance?.toFixed(2) || "0.00"}
              </Typography>
              <Typography variant="body2" color="textSecondary">
                Total Earned: ₹{wallet?.totalEarned?.toFixed(2) || "0.00"}
              </Typography>
              <Typography variant="body2" color="textSecondary">
                Total Withdrawn: ₹{wallet?.totalWithdrawn?.toFixed(2) || "0.00"}
              </Typography>
            </Grid>
          </Grid>
        </CardContent>
      </WalletCard>

      <Box sx={{ borderBottom: 1, borderColor: "divider" }}>
        <Tabs value={tabValue} onChange={(e, newValue) => setTabValue(newValue)}>
          <Tab label="Transactions" />
          <Tab label="Top-up" />
          <Tab label="Withdraw" />
        </Tabs>
      </Box>

      <TabPanel value={tabValue} index={0}>
        {transactionsLoading ? (
          <CircularProgress />
        ) : transactionsError ? (
          <Alert severity="error">{transactionsError.message}</Alert>
        ) : transactions.length === 0 ? (
          <Alert severity="info">No transactions yet</Alert>
        ) : (
          transactions.map((transaction: any) => (
            <TransactionCard key={transaction.id}>
              <CardContent>
                <Typography variant="h6">{transaction.transactionType}</Typography>
                <Typography variant="body2">Amount: ₹{transaction.amount.toFixed(2)}</Typography>
                <Typography variant="body2">Purpose: {transaction.purpose}</Typography>
                <Typography variant="body2">Status: {transaction.status}</Typography>
                <Typography variant="body2" color="textSecondary">
                  {new Date(transaction.createdAt).toLocaleString()}
                </Typography>
              </CardContent>
            </TransactionCard>
          ))
        )}
      </TabPanel>

      <TabPanel value={tabValue} index={1}>
        <Box>
          <TextField
            fullWidth
            label="Top-up Amount (₹)"
            type="number"
            value={topupAmount}
            onChange={(e) => setTopupAmount(e.target.value)}
            margin="normal"
          />
          <Button
            variant="contained"
            color="primary"
            onClick={handleTopup}
            disabled={topupLoading || !topupAmount}
            fullWidth
          >
            {topupLoading ? <CircularProgress size={24} /> : "Top-up Wallet"}
          </Button>
        </Box>
      </TabPanel>

      <TabPanel value={tabValue} index={2}>
        <Box>
          <TextField
            fullWidth
            label="Withdraw Amount (₹)"
            type="number"
            value={withdrawAmount}
            onChange={(e) => setWithdrawAmount(e.target.value)}
            margin="normal"
          />
          <TextField
            fullWidth
            label="UPI ID"
            value={upiId}
            onChange={(e) => setUpiId(e.target.value)}
            margin="normal"
          />
          <Button
            variant="contained"
            color="primary"
            onClick={handleWithdraw}
            disabled={withdrawLoading || !withdrawAmount || !upiId}
            fullWidth
          >
            {withdrawLoading ? <CircularProgress size={24} /> : "Withdraw"}
          </Button>
        </Box>
      </TabPanel>
    </WalletContainer>
  );
};

export default WalletPage;
