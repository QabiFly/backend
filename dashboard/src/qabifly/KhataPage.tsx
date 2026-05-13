import React, { useState } from "react";
import { useQuery, useMutation } from "@apollo/client";
import { allUdhaarQuery, sundayCollectionsQuery } from "./queries";
import { createUdhaarMutation, payUdhaarMutation, createSundayCollectionMutation, collectSundayCollectionMutation } from "./mutations";
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

const KhataPage = () => {
  const classes = useStyles();
  const [tabValue, setTabValue] = useState(0);
  const [selectedUdhaarId, setSelectedUdhaarId] = useState<string | null>(null);
  const [payAmount, setPayAmount] = useState("");

  // Create Udhaar form state
  const [createUdhaar, setCreateUdhaar] = useState({
    userId: "",
    shopId: "",
    orderId: "",
    amount: "",
    dueDate: "",
  });

  // Create Sunday Collection form state
  const [createCollection, setCreateCollection] = useState({
    deliveryBoyId: "",
    userId: "",
    udhaarId: "",
    amount: "",
    collectionDate: "",
  });

  const { data: udhaarData, loading: udhaarLoading, error: udhaarError, refetch: refetchUdhaar } = useQuery(allUdhaarQuery, {
    variables: { first: 20 },
  });
  const { data: collectionsData, loading: collectionsLoading, error: collectionsError, refetch: refetchCollections } = useQuery(sundayCollectionsQuery);

  const [payUdhaar, { loading: payLoading }] = useMutation(payUdhaarMutation, {
    onCompleted: () => {
      refetchUdhaar();
      setPayAmount("");
      setSelectedUdhaarId(null);
    },
  });

  const [createUdhaarMutationFn, { loading: createUdhaarLoading }] = useMutation(createUdhaarMutation, {
    onCompleted: () => {
      refetchUdhaar();
      setCreateUdhaar({ userId: "", shopId: "", orderId: "", amount: "", dueDate: "" });
    },
  });

  const [createSundayCollectionMutationFn, { loading: createCollectionLoading }] = useMutation(createSundayCollectionMutation, {
    onCompleted: () => {
      refetchCollections();
      setCreateCollection({ deliveryBoyId: "", userId: "", udhaarId: "", amount: "", collectionDate: "" });
    },
  });

  const handlePay = () => {
    if (!selectedUdhaarId || !payAmount) return;
    payUdhaar({
      variables: {
        input: {
          udhaarId: selectedUdhaarId,
          amount: parseFloat(payAmount),
        },
      },
    });
  };

  const handleCreateUdhaar = () => {
    if (!createUdhaar.userId || !createUdhaar.shopId || !createUdhaar.amount) return;
    createUdhaarMutationFn({
      variables: {
        input: {
          userId: createUdhaar.userId,
          shopId: createUdhaar.shopId,
          orderId: createUdhaar.orderId || undefined,
          amount: parseFloat(createUdhaar.amount),
          dueDate: createUdhaar.dueDate || undefined,
        },
      },
    });
  };

  const handleCreateCollection = () => {
    if (!createCollection.deliveryBoyId || !createCollection.userId || !createCollection.udhaarId || !createCollection.amount || !createCollection.collectionDate) return;
    createSundayCollectionMutationFn({
      variables: {
        input: {
          deliveryBoyId: createCollection.deliveryBoyId,
          userId: createCollection.userId,
          udhaarId: createCollection.udhaarId,
          amount: parseFloat(createCollection.amount),
          collectionDate: createCollection.collectionDate,
        },
      },
    });
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case "paid":
        return "default";
      case "overdue":
        return "secondary";
      case "partially_paid":
        return "primary";
      default:
        return "default";
    }
  };

  const udhaars = udhaarData?.udhaars?.edges?.map((edge: any) => edge.node) || [];
  const collections = collectionsData?.sundayCollections || [];
  const totalDue = udhaars.reduce((sum: number, u: any) => sum + parseFloat(u.remaining), 0);

  return (
    <div className={classes.root}>
      <Typography variant="h4" gutterBottom>
        Khata (Credit) Management
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Card className={classes.card}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Udhaar Records
              </Typography>
              <Box mb={2} p={2} bgcolor="primary.main" color="white" borderRadius={4}>
                <Typography variant="h6">Total Due: ₹{totalDue.toFixed(2)}</Typography>
              </Box>
              {udhaarLoading ? (
                <Box display="flex" justifyContent="center">
                  <CircularProgress />
                </Box>
              ) : udhaarError ? (
                <Alert severity="error">{udhaarError.message}</Alert>
              ) : udhaars.length === 0 ? (
                <Alert severity="info">No udhaar records found</Alert>
              ) : (
                udhaars.map((udhaar: any) => (
                  <Box
                    key={udhaar.id}
                    mb={2}
                    p={2}
                    border={1}
                    borderColor={selectedUdhaarId === udhaar.id ? "primary.main" : "grey.300"}
                    borderRadius={4}
                    onClick={() => setSelectedUdhaarId(udhaar.id)}
                    style={{ cursor: "pointer" }}
                  >
                    <Box display="flex" justifyContent="space-between" alignItems="center">
                      <Typography variant="subtitle1">{udhaar.user?.email}</Typography>
                      <Chip label={udhaar.status} color={getStatusColor(udhaar.status) as any} className={classes.statusChip} />
                    </Box>
                    <Typography variant="body2">Amount: ₹{udhaar.amount?.toFixed(2)}</Typography>
                    <Typography variant="body2">Remaining: ₹{udhaar.remaining?.toFixed(2)}</Typography>
                    <Typography variant="body2">Paid: ₹{udhaar.paidAmount?.toFixed(2)}</Typography>
                    {udhaar.dueDate && <Typography variant="body2">Due: {new Date(udhaar.dueDate).toLocaleDateString()}</Typography>}
                    {udhaar.isOverdue && <Alert severity="warning">Overdue</Alert>}
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
                Khata Actions
              </Typography>
              <Box sx={{ borderBottom: 1, borderColor: "divider" }}>
                <Tabs value={tabValue} onChange={(e, newValue) => setTabValue(newValue)}>
                  <Tab label="Sunday Collections" />
                  <Tab label="Create Udhaar" />
                  <Tab label="Create Collection" />
                  <Tab label="Pay Now" />
                </Tabs>
              </Box>

              <TabPanel value={tabValue} index={0}>
                {collectionsLoading ? (
                  <CircularProgress />
                ) : collectionsError ? (
                  <Alert severity="error">{collectionsError.message}</Alert>
                ) : collections.length === 0 ? (
                  <Alert severity="info">No Sunday collections found</Alert>
                ) : (
                  collections.map((collection: any) => (
                    <Box key={collection.id} mb={2} p={2} border={1} borderColor="grey.300" borderRadius={4}>
                      <Typography variant="subtitle1">{collection.user?.email}</Typography>
                      <Typography variant="body2">Delivery Boy: {collection.deliveryBoy?.email}</Typography>
                      <Typography variant="body2">Amount: ₹{collection.amount?.toFixed(2)}</Typography>
                      <Typography variant="body2">Collected: ₹{collection.collectedAmount?.toFixed(2)}</Typography>
                      <Typography variant="body2">Status: {collection.status}</Typography>
                      <Typography variant="body2">Date: {new Date(collection.collectionDate).toLocaleDateString()}</Typography>
                    </Box>
                  ))
                )}
              </TabPanel>

              <TabPanel value={tabValue} index={1}>
                <Box>
                  <TextField
                    fullWidth
                    label="User ID"
                    value={createUdhaar.userId}
                    onChange={(e) => setCreateUdhaar({ ...createUdhaar, userId: e.target.value })}
                    margin="normal"
                  />
                  <TextField
                    fullWidth
                    label="Shop ID"
                    value={createUdhaar.shopId}
                    onChange={(e) => setCreateUdhaar({ ...createUdhaar, shopId: e.target.value })}
                    margin="normal"
                  />
                  <TextField
                    fullWidth
                    label="Order ID (Optional)"
                    value={createUdhaar.orderId}
                    onChange={(e) => setCreateUdhaar({ ...createUdhaar, orderId: e.target.value })}
                    margin="normal"
                  />
                  <TextField
                    fullWidth
                    label="Amount (₹)"
                    type="number"
                    value={createUdhaar.amount}
                    onChange={(e) => setCreateUdhaar({ ...createUdhaar, amount: e.target.value })}
                    margin="normal"
                  />
                  <TextField
                    fullWidth
                    label="Due Date (Optional)"
                    type="date"
                    value={createUdhaar.dueDate}
                    onChange={(e) => setCreateUdhaar({ ...createUdhaar, dueDate: e.target.value })}
                    margin="normal"
                    InputLabelProps={{ shrink: true }}
                  />
                  <Button
                    variant="contained"
                    color="primary"
                    onClick={handleCreateUdhaar}
                    disabled={createUdhaarLoading || !createUdhaar.userId || !createUdhaar.shopId || !createUdhaar.amount}
                    fullWidth
                  >
                    {createUdhaarLoading ? <CircularProgress size={24} /> : "Create Udhaar"}
                  </Button>
                </Box>
              </TabPanel>

              <TabPanel value={tabValue} index={2}>
                <Box>
                  <TextField
                    fullWidth
                    label="Delivery Boy ID"
                    value={createCollection.deliveryBoyId}
                    onChange={(e) => setCreateCollection({ ...createCollection, deliveryBoyId: e.target.value })}
                    margin="normal"
                  />
                  <TextField
                    fullWidth
                    label="User ID"
                    value={createCollection.userId}
                    onChange={(e) => setCreateCollection({ ...createCollection, userId: e.target.value })}
                    margin="normal"
                  />
                  <TextField
                    fullWidth
                    label="Udhaar ID"
                    value={createCollection.udhaarId}
                    onChange={(e) => setCreateCollection({ ...createCollection, udhaarId: e.target.value })}
                    margin="normal"
                  />
                  <TextField
                    fullWidth
                    label="Amount (₹)"
                    type="number"
                    value={createCollection.amount}
                    onChange={(e) => setCreateCollection({ ...createCollection, amount: e.target.value })}
                    margin="normal"
                  />
                  <TextField
                    fullWidth
                    label="Collection Date"
                    type="date"
                    value={createCollection.collectionDate}
                    onChange={(e) => setCreateCollection({ ...createCollection, collectionDate: e.target.value })}
                    margin="normal"
                    InputLabelProps={{ shrink: true }}
                  />
                  <Button
                    variant="contained"
                    color="primary"
                    onClick={handleCreateCollection}
                    disabled={createCollectionLoading || !createCollection.deliveryBoyId || !createCollection.userId || !createCollection.udhaarId || !createCollection.amount || !createCollection.collectionDate}
                    fullWidth
                  >
                    {createCollectionLoading ? <CircularProgress size={24} /> : "Create Collection"}
                  </Button>
                </Box>
              </TabPanel>

              <TabPanel value={tabValue} index={3}>
                <Box>
                  <TextField
                    fullWidth
                    label="Selected Udhaar ID"
                    value={selectedUdhaarId || ""}
                    disabled
                    margin="normal"
                  />
                  <TextField
                    fullWidth
                    label="Payment Amount (₹)"
                    type="number"
                    value={payAmount}
                    onChange={(e) => setPayAmount(e.target.value)}
                    margin="normal"
                  />
                  <Button
                    variant="contained"
                    color="primary"
                    onClick={handlePay}
                    disabled={payLoading || !selectedUdhaarId || !payAmount}
                    fullWidth
                  >
                    {payLoading ? <CircularProgress size={24} /> : "Pay Now"}
                  </Button>
                </Box>
              </TabPanel>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </div>
  );
};

export default KhataPage;
