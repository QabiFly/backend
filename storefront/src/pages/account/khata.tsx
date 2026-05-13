import React, { useState } from "react";
import { useQuery, useMutation } from "react-apollo";
import { myUdhaarQuery, mySundayCollectionsQuery } from "@next/graphql/qabiflyQueries";
import { payUdhaarMutation } from "@next/graphql/qabiflyMutations";
import { Container, Typography, Box, Button, TextField, CircularProgress, Alert, Card, CardContent, Grid, Tabs, Tab, Chip } from "@material-ui/core";
import styled from "styled-components";

const KhataContainer = styled(Container)`
  padding: 2rem 0;
`;

const UdhaarCard = styled(Card)`
  margin-bottom: 1rem;
`;

const CollectionCard = styled(Card)`
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

const KhataPage = () => {
  const [tabValue, setTabValue] = useState(0);
  const [payAmount, setPayAmount] = useState("");
  const [selectedUdhaarId, setSelectedUdhaarId] = useState<string | null>(null);

  const { data: udhaarData, loading: udhaarLoading, error: udhaarError, refetch: refetchUdhaar } = useQuery(myUdhaarQuery);
  const { data: collectionsData, loading: collectionsLoading, error: collectionsError } = useQuery(mySundayCollectionsQuery);

  const [payUdhaar, { loading: payLoading }] = useMutation(payUdhaarMutation, {
    onCompleted: () => {
      refetchUdhaar();
      setPayAmount("");
      setSelectedUdhaarId(null);
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

  if (udhaarLoading) {
    return (
      <KhataContainer>
        <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
          <CircularProgress />
        </Box>
      </KhataContainer>
    );
  }

  if (udhaarError) {
    return (
      <KhataContainer>
        <Alert severity="error">Error loading khata data: {udhaarError.message}</Alert>
      </KhataContainer>
    );
  }

  const udhaars = udhaarData?.myUdhaar || [];
  const collections = collectionsData?.mySundayCollections || [];
  const totalDue = udhaars.reduce((sum: number, u: any) => sum + parseFloat(u.remaining), 0);

  return (
    <KhataContainer maxWidth="lg">
      <Typography variant="h4" gutterBottom>
        My Khata (Credit Book)
      </Typography>

      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Grid container spacing={3}>
            <Grid item xs={12} sm={6}>
              <Typography variant="h6" color="primary">
                Total Due Amount
              </Typography>
              <Typography variant="h3">₹{totalDue.toFixed(2)}</Typography>
            </Grid>
            <Grid item xs={12} sm={6}>
              <Typography variant="body2" color="textSecondary">
                Active Records: {udhaars.filter((u: any) => u.status !== "paid").length}
              </Typography>
              <Typography variant="body2" color="textSecondary">
                Paid Records: {udhaars.filter((u: any) => u.status === "paid").length}
              </Typography>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      <Box sx={{ borderBottom: 1, borderColor: "divider" }}>
        <Tabs value={tabValue} onChange={(e, newValue) => setTabValue(newValue)}>
          <Tab label="Udhaar Records" />
          <Tab label="Sunday Collections" />
          <Tab label="Pay Now" />
        </Tabs>
      </Box>

      <TabPanel value={tabValue} index={0}>
        {udhaars.length === 0 ? (
          <Alert severity="info">No udhaar records found</Alert>
        ) : (
          udhaars.map((udhaar: any) => (
            <UdhaarCard key={udhaar.id}>
              <CardContent>
                <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
                  <Typography variant="h6">₹{udhaar.amount.toFixed(2)}</Typography>
                  <Chip label={udhaar.status} color={getStatusColor(udhaar.status) as any} />
                </Box>
                <Typography variant="body2">Remaining: ₹{udhaar.remaining.toFixed(2)}</Typography>
                <Typography variant="body2">Paid: ₹{udhaar.paidAmount.toFixed(2)}</Typography>
                {udhaar.dueDate && (
                  <Typography variant="body2">Due Date: {new Date(udhaar.dueDate).toLocaleDateString()}</Typography>
                )}
                {udhaar.isOverdue && (
                  <Alert severity="warning" sx={{ mt: 1 }}>
                    This payment is overdue
                  </Alert>
                )}
                <Typography variant="body2" color="textSecondary">
                  Created: {new Date(udhaar.createdAt).toLocaleDateString()}
                </Typography>
              </CardContent>
            </UdhaarCard>
          ))
        )}
      </TabPanel>

      <TabPanel value={tabValue} index={1}>
        {collectionsLoading ? (
          <CircularProgress />
        ) : collectionsError ? (
          <Alert severity="error">{collectionsError.message}</Alert>
        ) : collections.length === 0 ? (
          <Alert severity="info">No Sunday collections found</Alert>
        ) : (
          collections.map((collection: any) => (
            <CollectionCard key={collection.id}>
              <CardContent>
                <Typography variant="h6">₹{collection.amount.toFixed(2)}</Typography>
                <Typography variant="body2">Collected: ₹{collection.collectedAmount.toFixed(2)}</Typography>
                <Typography variant="body2">Status: {collection.status}</Typography>
                <Typography variant="body2">
                  Collection Date: {new Date(collection.collectionDate).toLocaleDateString()}
                </Typography>
                {collection.notes && <Typography variant="body2">Notes: {collection.notes}</Typography>}
              </CardContent>
            </CollectionCard>
          ))
        )}
      </TabPanel>

      <TabPanel value={tabValue} index={2}>
        <Box>
          <TextField
            fullWidth
            select
            label="Select Udhaar Record"
            value={selectedUdhaarId || ""}
            onChange={(e) => setSelectedUdhaarId(e.target.value)}
            SelectProps={{ native: true }}
            margin="normal"
          >
            <option value="">Select a record</option>
            {udhaars
              .filter((u: any) => u.status !== "paid")
              .map((udhaar: any) => (
                <option key={udhaar.id} value={udhaar.id}>
                  ₹{udhaar.amount.toFixed(2)} - Due: {udhaar.dueDate ? new Date(udhaar.dueDate).toLocaleDateString() : "N/A"}
                </option>
              ))}
          </TextField>
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
    </KhataContainer>
  );
};

export default KhataPage;
