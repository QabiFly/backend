import React from "react";
import { useQuery } from "@apollo/client";
import { liveDeliveriesQuery, deliveryAssignmentsQuery } from "./queries";
import { Card, CardContent, Typography, Box, CircularProgress, Alert, Chip, Grid } from "@material-ui/core";
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

const DeliveryPage = () => {
  const classes = useStyles();
  const { data: liveData, loading: liveLoading, error: liveError } = useQuery(liveDeliveriesQuery, {
    pollInterval: 5000,
  });
  const { data: assignmentsData, loading: assignmentsLoading, error: assignmentsError } = useQuery(deliveryAssignmentsQuery);

  const getStatusColor = (status: string) => {
    switch (status) {
      case "delivered":
        return "default";
      case "in_transit":
        return "primary";
      case "failed":
        return "secondary";
      default:
        return "default";
    }
  };

  return (
    <div className={classes.root}>
      <Typography variant="h4" gutterBottom>
        Delivery Management
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Card className={classes.card}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Live Deliveries
              </Typography>
              {liveLoading ? (
                <Box display="flex" justifyContent="center">
                  <CircularProgress />
                </Box>
              ) : liveError ? (
                <Alert severity="error">{liveError.message}</Alert>
              ) : !liveData?.liveDeliveries || liveData.liveDeliveries.length === 0 ? (
                <Alert severity="info">No active deliveries</Alert>
              ) : (
                liveData.liveDeliveries.map((delivery: any) => (
                  <Box key={delivery.id} mb={2} p={2} border={1} borderColor="grey.300" borderRadius={4}>
                    <Typography variant="subtitle1">Order #{delivery.order?.number}</Typography>
                    <Typography variant="body2" color="textSecondary">
                      Delivery Boy: {delivery.deliveryBoy?.firstName} {delivery.deliveryBoy?.lastName}
                    </Typography>
                    <Typography variant="body2">Location: {delivery.latitude}, {delivery.longitude}</Typography>
                    <Typography variant="body2">Speed: {delivery.speed || "N/A"} km/h</Typography>
                    <Typography variant="body2">Battery: {delivery.batteryLevel || "N/A"}%</Typography>
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
                Delivery Assignments
              </Typography>
              {assignmentsLoading ? (
                <Box display="flex" justifyContent="center">
                  <CircularProgress />
                </Box>
              ) : assignmentsError ? (
                <Alert severity="error">{assignmentsError.message}</Alert>
              ) : !assignmentsData?.deliveryAssignments || assignmentsData.deliveryAssignments.length === 0 ? (
                <Alert severity="info">No delivery assignments</Alert>
              ) : (
                assignmentsData.deliveryAssignments.map((assignment: any) => (
                  <Box key={assignment.id} mb={2} p={2} border={1} borderColor="grey.300" borderRadius={4}>
                    <Box display="flex" justifyContent="space-between" alignItems="center">
                      <Typography variant="subtitle1">Order #{assignment.order?.number}</Typography>
                      <Chip label={assignment.status} color={getStatusColor(assignment.status) as any} className={classes.statusChip} />
                    </Box>
                    <Typography variant="body2" color="textSecondary">
                      Delivery Boy: {assignment.deliveryBoy?.firstName} {assignment.deliveryBoy?.lastName}
                    </Typography>
                    <Typography variant="body2">OTP: {assignment.deliveryOtp}</Typography>
                    <Typography variant="body2">Assigned: {new Date(assignment.assignedAt).toLocaleString()}</Typography>
                  </Box>
                ))
              )}
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </div>
  );
};

export default DeliveryPage;
