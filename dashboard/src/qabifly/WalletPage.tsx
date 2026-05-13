import React, { useState } from "react";
import { useQuery, useMutation } from "@apollo/client";
import { allWalletsQuery, walletTransactionsQuery } from "./queries";
import { topupWalletMutation, withdrawWalletMutation } from "./mutations";
import { Card, CardContent, Typography, Box, CircularProgress, Alert, Button, TextField, Grid, Tabs, Tab, Chip } from "@material-ui/core";
import { makeStyles } from "@material-ui/core/styles";

const useStyles = makeStyles((theme) => ({
  root: {
    padding: theme.spacing(3),
  },
  card: {
    marginBottom: theme.spacing(2),
  },
  statusChip: {
    marginLeft: theme.spacing(1),
  },
}));

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
  const classes = useStyles();
  const [tabValue, setTabValue] = useState(0);
  const [selectedWalletId, setSelectedWalletId] = useState<string | null>(null);
  const [topupAmount, setTopupAmount] = useState("");
  const [withdrawAmount, setWithdrawAmount] = useState("");
  const [upiId, setUpiId] = useState("");

  const { data: walletsData, loading: walletsLoading, error: walletsError, refetch: refetchWallets } = useQuery(allWalletsQuery, {
    variables: { first: 20 },
  });
  const { data: transactionsData, loading: transactionsLoading, error: transactionsError } = useQuery(walletTransactionsQuery, {
    variables: { walletId: selectedWalletId || "" },
    skip: !selectedWalletId,
  });

  const [topupWallet, { loading: topupLoading }] = useMutation(topupWalletMutation, {
    onCompleted: () => {
      refetchWallets();
      setTopupAmount("");
    },
  });

  const [withdrawWallet, { loading: withdrawLoading }] = useMutation(withdrawWalletMutation, {
    onCompleted: () => {
      refetchWallets();
      setWithdrawAmount("");
      setUpiId("");
    },
  });

  const handleTopup = () => {
    if (!selectedWalletId || !topupAmount) return;
    topupWallet({
      variables: {
        walletId: selectedWalletId,
        input: {
          amount: parseFloat(topupAmount),
          method: "UPI",
        },
      },
    });
  };

  const handleWithdraw = () => {
    if (!selectedWalletId || !withdrawAmount || !upiId) return;
    withdrawWallet({
      variables: {
        walletId: selectedWalletId,
        input: {
          amount: parseFloat(withdrawAmount),
          upiId,
        },
      },
    });
  };

  const wallets = walletsData?.wallets?.edges?.map((edge: any) => edge.node) || [];
  const transactions = transactionsData?.walletTransactions || [];

  return (
    <div className={classes.root}>
      <Typography variant="h4" gutterBottom>
        Wallet Management
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Card className={classes.card}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                All Wallets
              </Typography>
              {walletsLoading ? (
                <Box display="flex" justifyContent="center">
                  <CircularProgress />
                </Box>
              ) : walletsError ? (
                <Alert severity="error">{walletsError.message}</Alert>
              ) : wallets.length === 0 ? (
                <Alert severity="info">No wallets found</Alert>
              ) : (
                wallets.map((wallet: any) => (
                  <Box
                    key={wallet.id}
                    mb={2}
                    p={2}
                    border={1}
                    borderColor={selectedWalletId === wallet.id ? "primary.main" : "grey.300"}
                    borderRadius={4}
                    onClick={() => setSelectedWalletId(wallet.id)}
                    style={{ cursor: "pointer" }}
                  >
                    <Box display="flex" justifyContent="space-between" alignItems="center">
                      <Typography variant="subtitle1">{wallet.user?.email}</Typography>
                      <Chip label={wallet.isActive ? "Active" : "Inactive"} color={wallet.isActive ? "primary" : "default"} className={classes.statusChip} />
                    </Box>
                    <Typography variant="body2">Balance: ₹{wallet.balance?.toFixed(2)}</Typography>
                    <Typography variant="body2">Pending: ₹{wallet.pendingBalance?.toFixed(2)}</Typography>
                    <Typography variant="body2">Total Earned: ₹{wallet.totalEarned?.toFixed(2)}</Typography>
                    <Typography variant="body2">Total Withdrawn: ₹{wallet.totalWithdrawn?.toFixed(2)}</Typography>
                  </Box>
                ))
              )}
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Card className={classes.card}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Wallet Actions
              </Typography>
              {!selectedWalletId ? (
                <Alert severity="info">Select a wallet to view details and perform actions</Alert>
              ) : (
                <>
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
                      <Alert severity="info">No transactions found</Alert>
                    ) : (
                      transactions.map((transaction: any) => (
                        <Box key={transaction.id} mb={2} p={2} border={1} borderColor="grey.300" borderRadius={4}>
                          <Typography variant="subtitle1">{transaction.transactionType}</Typography>
                          <Typography variant="body2">Amount: ₹{transaction.amount?.toFixed(2)}</Typography>
                          <Typography variant="body2">Purpose: {transaction.purpose}</Typography>
                          <Typography variant="body2">Status: {transaction.status}</Typography>
                          <Typography variant="body2" color="textSecondary">
                            {new Date(transaction.createdAt).toLocaleString()}
                          </Typography>
                        </Box>
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
                </>
              )}
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </div>
  );
};

export default WalletPage;
