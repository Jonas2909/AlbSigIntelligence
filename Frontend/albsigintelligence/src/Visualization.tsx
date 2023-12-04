import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Dialog, DialogTitle, DialogContent, DialogActions, Button, makeStyles, Typography, Grid, TextField } from '@material-ui/core';
import Box from '@mui/material/Box';
import Paper from '@mui/material/Paper';
import {
  ResponsiveContainer,
  CartesianGrid,
  XAxis,
  YAxis,
  Tooltip,
  Bar,
  BarChart,
  Legend
} from "recharts";
import Accordion from '@mui/material/Accordion';
import AccordionSummary from '@mui/material/AccordionSummary';
import AccordionDetails from '@mui/material/AccordionDetails';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import moment from "moment";
import LinearProgress from '@mui/material/LinearProgress';
import { usePromiseTracker } from "react-promise-tracker"
import { createTheme } from '@mui/material/styles';
import Snackbar from '@mui/material/Snackbar';
import MuiAlert from '@mui/material/Alert';

const defaultTheme = createTheme();

export default function Visualization() {
  const navigate = useNavigate();
  const classes = useStyles();
  const { promiseInProgress } = usePromiseTracker();
  const [isDialogOpen, setDialogOpen] = useState(false);
  const [snackbarOpen, setSnackbarOpen] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState('');
  const [measurements, setMeasurements] = useState([]);

  var currentDate: Date = new Date()
  var yesterday: Date = new Date()

  yesterday.setDate(currentDate.getDate() - 1)

  const [dateRange, setDateRange] = useState({
    from: new Date(),
    to: new Date(),
  });

  useEffect(() => {
    const isLoggedIn = sessionStorage.getItem('isLoggedIn');
    if (!isLoggedIn) {
      setDialogOpen(true);
    }
  }, []);

  const handleDialogClose = () => {
    setDialogOpen(false);
    navigate('/');
  };

  const handleSnackbarClose = (event, reason) => {
    if (reason === 'clickaway') {
      return;
    }
    setSnackbarOpen(false);
  };

  const handleDateChange = (date, field) => {
    setDateRange((prevDateRange) => ({
      ...prevDateRange,
      [field]: date,
    }));
  };

  const fetchMeasurements = async () => {
    console.log("Fetching URL:", "http://localhost:5000/GetGraphDataFromTo");

    const fromUtcInSeconds = moment.utc(dateRange.from).utc().valueOf() / 1000;
    const toUtcInSeconds = moment.utc(dateRange.to).utc().valueOf() / 1000;

    console.log('From UTC in seconds:', fromUtcInSeconds);
    console.log('To UTC in seconds:', toUtcInSeconds);

    try {
      const requestBody = {
        time_stamp_from: fromUtcInSeconds,
        time_stamp_to: toUtcInSeconds
      };

      const response = await fetch("http://localhost:5000/GetGraphDataFromTo", {
        headers: { 'Content-Type': 'application/json' },
        method: 'POST',
        mode: 'cors',
        body: JSON.stringify(requestBody)
      });

      if (response.status === 200) {
        const responseData = await response.json();

        if (responseData && responseData.data && responseData.data.length > 0) {
          console.log(responseData);
          setMeasurements(responseData.data);
        } else {
          setSnackbarMessage("Could not find any measurements in the given timespan.");
          setSnackbarOpen(true);
        }

      } else if (response.status === 404) {
        setSnackbarMessage("Could not read measurements from the database.");
        setSnackbarOpen(true);
      } else {
        throw new Error(`Request failed with status: ${response.status}`);
      }
    } catch (error) {
      console.error("Error fetching Measurements:", error);
      throw error;
    }
  };

  return (
    <div>
      <h1 style={{ backgroundColor: defaultTheme.palette.primary.main, padding: '10px', color: 'black', border: '2px solid black', borderRadius: '5px', marginBottom: '0px' }}>Visualization</h1>

      <Dialog open={isDialogOpen} onClose={handleDialogClose}>
        <DialogTitle>Error</DialogTitle>
        <DialogContent>
          <p>User not logged in!</p>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleDialogClose} color="primary">
            OK
          </Button>
        </DialogActions>
      </Dialog>

      <Accordion defaultExpanded style={{ border: '2px solid black', borderRadius: '5px', marginTop: '5px', marginBottom: '10px' }}>
        <AccordionSummary
          expandIcon={<ExpandMoreIcon />}
          aria-controls="panel1a-content"
          id="panel1a-header"
        >
          <Typography className={classes.heading} component={'span'}>Filter</Typography>
        </AccordionSummary>
        <AccordionDetails>
          <Grid
            container
            direction="row"
            justifyContent="flex-start"
            alignItems="stretch"
            spacing={2}
          >
            <Grid container
              direction="column"
              spacing={2}
            >
              <Grid item></Grid>
              <Grid item>
                <Grid container direction="row" justifyContent="flex-start" alignItems="center" spacing={2}>
                  <Grid item>
                    <TextField
                      variant="outlined"
                      label="From"
                      value={moment(dateRange.from).format("YYYY-MM-DDTHH:mm") || ''}
                      onChange={(e) => handleDateChange(new Date(e.target.value), 'from')}
                      type="datetime-local"

                      disabled={promiseInProgress}
                    />
                  </Grid>
                  <Grid item>
                    <TextField
                      variant="outlined"
                      label="To"
                      type="datetime-local"
                      value={moment(dateRange.to).format("YYYY-MM-DDTHH:mm") || ''}
                      onChange={(e) => handleDateChange(new Date(e.target.value), 'to')}
                      disabled={promiseInProgress}
                    />
                  </Grid>
                  <Grid item>
                    <Button
                      className={classes.buttonSend}
                      variant="contained"
                      color="primary"
                      disabled={promiseInProgress}
                      onClick={fetchMeasurements}
                    >
                      Send
                    </Button>
                  </Grid>
                  <Grid item>
                    <Button
                      className={classes.buttonSend}
                      variant="contained"
                      color="primary"
                      disabled={promiseInProgress}
                    >
                      Reset
                    </Button>
                  </Grid>
                  <Grid item style={{ marginLeft: 'auto', border: '2px solid #ccc', borderRadius: '5px', padding: '5px' }}>
                    <TextField
                      id="standard-search"
                      label="MAC address"
                      type="search"
                      variant="standard"
                    />
                  </Grid>
                </Grid>
              </Grid>
              <Grid item>
                <div>
                  {
                    (promiseInProgress === true) ?
                      <LinearProgress />
                      :
                      null
                  }
                </div>
              </Grid>
            </Grid>
          </Grid>
        </AccordionDetails>
      </Accordion>

      <Paper variant='outlined' sx={{
        backgroundColor: defaultTheme.palette.background.paper,
      }}>
        <Box
          sx={{
            height: "40vh",
            minWidth: 600,
            minHeight: 100,
            marginTop: 2.5,
            marginBottom: 2.5,
          }}
        >

          <ResponsiveContainer minWidth={500} height="100%" minHeight={100}>
            <BarChart
              data={measurements}
              margin={{
                top: 0, right: 10, bottom: 0, left: 0
              }}
              legend={{ fill: 'black' }}
            >
              <CartesianGrid strokeDasharray="6 6" />
              <XAxis
                dataKey="time_stamp"
                allowDataOverflow={true}
                stroke={defaultTheme.palette.text.primary}
                tickFormatter={(unixTime) => moment.unix(unixTime).format('DD.MM.YY HH:mm')}
                domain={['auto', 'auto']}
              />
              <YAxis
                orientation='left'
                width={100}
                stroke={defaultTheme.palette.text.primary}
              />
              <Tooltip labelFormatter={(unixTime) => moment.unix(unixTime).format('DD.MM.YY HH:mm')} isAnimationActive={false} />
              <Bar dataKey="quantity" fill={defaultTheme.palette.primary.main} name='Number of Clients in Network' isAnimationActive={true} />
              <Legend align="center" verticalAlign="top" height={36} />
            </BarChart>
          </ResponsiveContainer>
        </Box>
      </Paper>

      <Snackbar
        open={snackbarOpen}
        autoHideDuration={6000}
        onClose={handleSnackbarClose}
      >
        <MuiAlert
          elevation={6}
          variant="filled"
          severity="error"
          onClose={handleSnackbarClose}
        >
          {snackbarMessage}
        </MuiAlert>
      </Snackbar>

    </div>
  );
}

const useStyles = makeStyles(() => ({
  buttonSend: {
    marginTop: '5px',
    backgroundColor: defaultTheme.palette.primary.main,
    color: 'black',
    '&:hover': {
      backgroundColor: defaultTheme.palette.primary.dark,
    }
  },
  heading: {
    marginLeft: '10px',
    fontSize: '20px',
    fontWeight: 'normal',
    color: 'black',
  },
}));