import React from "react";
import { useQuery } from "react-apollo";
import { liveDeliveriesQuery } from "@next/graphql/saleorQueries";
import { Container, Typography, Box, CircularProgress, Alert } from "@material-ui/core";
import styled from "styled-components";

const DeliveryContainer = styled(Container)`
  padding: 2rem 0;
`;

const DeliveryCard = styled(Box)`
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  margin-bottom: 1rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
`;

const DeliveryTrackingPage = () => {
  const { data, loading, error } = useQuery(liveDeliveriesQuery, {
    pollInterval: 5000, // Refresh every 5 seconds for real-time updates
  });

  if (loading) {
    return (
      <DeliveryContainer>
        <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
          <CircularProgress />
        </Box>
      </DeliveryContainer>
    );
  }

  if (error) {
    return (
      <DeliveryContainer>
        <Alert severity="error">Error loading delivery data: {error.message}</Alert>
      </DeliveryContainer>
    );
  }

  const deliveries = data?.liveDeliveries || [];

  return (
    <DeliveryContainer maxWidth="lg">
      <Typography variant="h4" gutterBottom>
        Live Delivery Tracking
      </Typography>
      <Typography variant="body1" color="textSecondary" paragraph>
        Real-time location updates for active deliveries
      </Typography>

      {deliveries.length === 0 ? (
        <Alert severity="info">No active deliveries at the moment</Alert>
      ) : (
        deliveries.map((delivery: any) => (
          <DeliveryCard key={delivery.id}>
            <Typography variant="h6" gutterBottom>
              Order #{delivery.order?.number || "N/A"}
            </Typography>
            <Typography variant="body2" color="textSecondary">
              Delivery Boy: {delivery.deliveryBoy?.firstName} {delivery.deliveryBoy?.lastName}
            </Typography>
            <Typography variant="body2" color="textSecondary">
              Email: {delivery.deliveryBoy?.email}
            </Typography>
            <Box mt={2}>
              <Typography variant="body2">
                <strong>Location:</strong> {delivery.latitude}, {delivery.longitude}
              </Typography>
              <Typography variant="body2">
                <strong>Speed:</strong> {delivery.speed || "N/A"} km/h
              </Typography>
              <Typography variant="body2">
                <strong>Battery:</strong> {delivery.batteryLevel || "N/A"}%
              </Typography>
              <Typography variant="body2" color="textSecondary">
                <strong>Last Updated:</strong>{" "}
                {new Date(delivery.recordedAt).toLocaleString()}
              </Typography>
            </Box>
          </DeliveryCard>
        ))
      )}
    </DeliveryContainer>
  );
};

export default DeliveryTrackingPage;
