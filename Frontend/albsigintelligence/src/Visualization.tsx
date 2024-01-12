import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Grid, TextField, Button, InputAdornment, Dialog, DialogTitle, DialogContent, DialogActions, Typography, makeStyles, Table, TableHead, TableRow, TableCell, TableBody } from '@material-ui/core';
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
import SearchIcon from '@mui/icons-material/Search';
import Link from '@mui/material/Link';

const defaultTheme = createTheme();

export default function Visualization() {
  const navigate = useNavigate();
  const classes = useStyles();
  const { promiseInProgress } = usePromiseTracker();
  const [isDialogOpen, setDialogOpen] = useState(false);
  const [snackbarOpen, setSnackbarOpen] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState('');
  const [measurements, setMeasurements] = useState([]);
  const [timestamps, setTimestamps] = useState([]);
  const [openDialog, setOpenDialog] = useState(false);
  const [searchedString, setSearchedString] = useState('');
  const [searchValue, setSearchValue] = useState('');


  var today = new Date();

  const [endDate, setEndDate] = useState<number>(today.setHours(0, 0, 0, 0).valueOf());
  const [startDate, setStartDate] = useState<number>(today.setDate(today.getDate() + 1));
  const [dateType, setDateType] = useState<string>('');

  var currentDate: Date = new Date()
  var yesterday: Date = new Date()

  yesterday.setDate(currentDate.getDate() - 1)

  function getMonday(d: Date) {
    d = new Date(d);
    var day = d.getDay(),
      diff = d.getDate() - day + (day === 0 ? -6 : 1); // adjust when day is sunday

    d.setHours(0, 0, 0, 0);
    return new Date(d.setDate(diff));
  }

  function Copyright() {
    return (
      <Typography variant="body2" align="center" style={{ marginTop: '100px' }}>
        {'Copyright © '}
        <Link color="inherit" href="https://www.hs-albsig.de/">
          AlbSigIntelligence
        </Link>{' '}
        {new Date().getFullYear()}
        {'.'}
      </Typography>
    );
  }

  const [dateRange, setDateRange] = useState({
    from: new Date(),
    to: new Date(),
  });

  useEffect(() => {
    const isLoggedIn = sessionStorage.getItem('isLoggedIn');
    if (!isLoggedIn) {
      setDialogOpen(true);
    }

    const fetchData = async () => {
      const startTimestamp = Math.floor(startDate.valueOf() / 1000);
      const endTimestamp = Math.floor(endDate.valueOf() / 1000);
      await fetchMeasurements(startTimestamp, endTimestamp);
    };

    fetchData();

  }, [dateType, startDate, endDate]);

  const handleDialogClose = () => {
    setDialogOpen(false);
    navigate('/');
  };

  const handleSnackbarClose = (event: React.SyntheticEvent, reason?: string) => {
    if (reason === 'clickaway') {
      return;
    }

    setSnackbarOpen(false);
  }

  const handleDateChange = (date, field) => {
    setDateRange((prevDateRange) => ({
      ...prevDateRange,
      [field]: date,
    }));
  };

  const fetchMeasurements = async (fromUtcInSeconds, toUtcInSeconds) => {
    // Check if fromUtcInSeconds and toUtcInSeconds are the same
    if (fromUtcInSeconds === toUtcInSeconds) {
      console.log("From and To value equal");
      // Set fromUtcInSeconds to the beginning of the current day
      const startOfDay = new Date();
      startOfDay.setHours(0, 0, 0, 0);
      fromUtcInSeconds = Math.floor(startOfDay.getTime() / 1000);

      // Set toUtcInSeconds to the end of the current day
      const endOfDay = new Date();
      endOfDay.setHours(23, 59, 59, 999);
      toUtcInSeconds = Math.floor(endOfDay.getTime() / 1000);
    }

    try {
      const requestBody = {
        time_stamp_from: fromUtcInSeconds,
        time_stamp_to: toUtcInSeconds
      };

      const response = await fetch("https://localhost:5000/GetGraphDataFromTo", {
        headers: { 'Content-Type': 'application/json' },
        method: 'POST',
        mode: 'cors',
        body: JSON.stringify(requestBody)
      });

      if (response.status === 200) {
        const responseData = await response.json();

        if (responseData && responseData.data && responseData.data.length > 0) {
          if (dateType === "tag" || dateType === "week" || dateType === "month") {
            calculateMeasurements(responseData);
          } else {
            setMeasurements(responseData.data);
          }
        } else {
          setSnackbarMessage("Could not find any measurements in the given timespan.");
          setSnackbarOpen(true);
          resetGraph();
        }

      } else if (response.status === 404) {
        setSnackbarMessage("Could not read measurements from the database.");
        setSnackbarOpen(true);
        resetGraph();
      } else {
        throw new Error(`Request failed with status: ${response.status}`);
      }
    } catch (error) {
      console.error("Error fetching Measurements:", error);
      resetGraph();
      throw error;
    }
  };

  const calculateMeasurements = (responseData) => {
    //console.log(responseData);
    //console.log(responseData.data.length);

    // Group measurements by day
    const measurementsByDay = responseData.data.reduce((result, measurement) => {
      const timestamp = measurement.time_stamp;

      // Check if the timestamp is a valid number and greater than the Unix epoch
      if (!isNaN(timestamp) && timestamp > 0) {
        const day = new Date(timestamp * 1000).toISOString().split('T')[0]; // Convert timestamp to ISO date

        if (!result[day]) {
          result[day] = [];
        }

        result[day].push(measurement);
      }

      return result;
    }, {});

    // Calculate the average for each day and create a new array with the calculated averages
    let idCounter = 1;
    const newArrayWithAverages = Object.keys(measurementsByDay).map((day) => {
      const measurementsForDay = measurementsByDay[day];
      const sumOfQuantities = measurementsForDay.reduce((sum, measurement) => sum + measurement.quantity, 0);
      const average = (sumOfQuantities / measurementsForDay.length).toFixed(0); // Round to two decimal places

      const dayInUtcSeconds = Math.floor(new Date(day).getTime() / 1000); // Convert to UTC seconds

      return {
        id: idCounter++,
        time_stamp: dayInUtcSeconds,
        quantity: average,
      };
    });

    //console.log(newArrayWithAverages);
    setMeasurements(newArrayWithAverages);
  };


  const fetchTimeStamps = async (mac) => {
    console.log("Fetching URL:", "https://localhost:5000/GetTimeStampsByMac");

    try {
      const requestBody = {
        mac_address: mac
      };

      const response = await fetch("https://localhost:5000/GetTimeStampsByMac", {
        headers: { 'Content-Type': 'application/json' },
        method: 'POST',
        mode: 'cors',
        body: JSON.stringify(requestBody)
      });

      if (response.status === 200) {
        const responseData = await response.json();

        if (responseData && responseData.entries && Array.isArray(responseData.entries)) {
          console.log(responseData.entries);
          setTimestamps(responseData.entries);
          setOpenDialog(true);
          return;
        } else {
          setSnackbarMessage("Could not find any timestamps for the given mac-address");
          setSnackbarOpen(true);
          setOpenDialog(false);
        }
      } else if (response.status === 404) {
        setSnackbarMessage("Could not read timestamps from the database.");
        setSnackbarOpen(true);
        setOpenDialog(false);
      } else {
        throw new Error(`Request failed with status: ${response.status}`);
      }
    } catch (error) {
      console.error("Error fetching timestamps:", error);
      setOpenDialog(false);
      throw error;
    }
  };

  const handleDateTypeChange = async (dateType: string) => {
    var date = new Date();
    //console.log("Function handleDateTypeChange: date=" + date);

    switch (dateType) {
      case "day":
        setDateType("day");
        setStartDate(new Date(date.getFullYear(), date.getMonth(), date.getDate(), 0, 0, 0, 0).valueOf());
        setEndDate(new Date(date.getFullYear(), date.getMonth(), date.getDate() + 0, 0, 0, 0, 0).valueOf());
        //console.log(new Date(startDate).toLocaleString());
        //console.log(new Date(endDate).toLocaleString());
        break;

      case "week":
        setDateType("week");
        let monday = getMonday(new Date());
        setStartDate(monday.valueOf())
        setEndDate(new Date(monday.getFullYear(), monday.getMonth(), monday.getDate() + 7, 0, 0, 0, 0).valueOf())
        //console.log(new Date(startDate).toLocaleString());
        //console.log(new Date(endDate).toLocaleString());
        break;

      case "month":
        setDateType("month");
        setStartDate(new Date(date.getFullYear(), date.getMonth(), 1).valueOf());
        setEndDate(new Date(date.getFullYear(), date.getMonth() + 1, 1, 0, 0, 0, 0).valueOf());
        //console.log(new Date(startDate).toLocaleString());
        //console.log(new Date(endDate).toLocaleString());
        break;

      default:
        setDateType("");
        console.warn("Chart : handleDateTypeChange : wrong type!")
        setStartDate(0);
        break;
    }

    setDateType(dateType);

    const startTimestamp = Math.floor(startDate.valueOf() / 1000);
    const endTimestamp = Math.floor(endDate.valueOf() / 1000);

    await fetchMeasurements(startTimestamp, endTimestamp);
  };

  const resetGraph = () => {
    console.log("Reseting graph...");
    setMeasurements([]);
  };

  const handleSearch = () => {
    if (searchValue.trim() === '') {
      setSnackbarMessage("Input of MAC-address is empty!");
      setSnackbarOpen(true);
      return;
    }
    const searchString = searchValue;
    setSearchedString(searchString);
    fetchTimeStamps(searchString);
    setOpenDialog(true);
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
  };

  function formatTimestamp(utcTimestampInSeconds) {
    const timestampInMilliseconds = utcTimestampInSeconds * 1000;
    const date = new Date(timestampInMilliseconds);
    const formattedDate = `${date.getDate()}-${padZero(date.getMonth() + 1)}-${padZero(date.getFullYear())} ${padZero(date.getHours())}:${padZero(date.getMinutes())}:${padZero(date.getSeconds())}`;
    return formattedDate;
  }

  function padZero(number) {
    return number.toString().padStart(2, '0');
  }

  return (
    <div>
      <h1 style={{
        backgroundColor: defaultTheme.palette.primary.main,
        padding: '10px',
        color: 'black',
        border: '2px solid black',
        borderRadius: '5px',
        margin: '0 2px',
      }}>Visualization</h1>
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

      <Accordion defaultExpanded style={{ border: '2px solid black', borderRadius: '5px', marginTop: '-1px', marginBottom: '20px', marginLeft: '2px', marginRight: '2px' }}>
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
                      value={moment(dateRange.from).format("YYYY-MM-DD") || ''}
                      onChange={(e) => handleDateChange(new Date(e.target.value), 'from')}
                      type="date"

                      disabled={promiseInProgress}
                    />
                  </Grid>
                  <Grid item>
                    <TextField
                      variant="outlined"
                      label="To"
                      type="date"
                      value={moment(dateRange.to).format("YYYY-MM-DD") || ''}
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
                      onClick={() => fetchMeasurements(dateRange.from.getTime() / 1000, dateRange.to.getTime() / 1000)}
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
                      onClick={resetGraph}
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
                      value={searchValue}
                      onChange={(e) => setSearchValue(e.target.value)}
                      InputProps={{
                        endAdornment: (
                          <InputAdornment position="end">
                            <Button
                              variant="contained"
                              color="primary"
                              onClick={handleSearch}
                              style={{ marginBottom: '18px' }}
                              className={classes.buttonSend}
                            >
                              <SearchIcon />
                            </Button>
                          </InputAdornment>
                        ),
                      }}
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
              margin={{ top: 0, right: 10, bottom: 0, left: 0 }}
            >
              <CartesianGrid strokeDasharray="6 6" />
              <XAxis
                dataKey="time_stamp"
                allowDataOverflow={true}
                stroke={defaultTheme.palette.text.primary}
                tickFormatter={(unixTime) => dateType === "day" ? moment.unix(unixTime).format('HH:mm') : dateType === "week" ? moment.unix(unixTime).format('ddd') : moment.unix(unixTime).format('DD.MM')}
                domain={[startDate, endDate]}
              />
              <YAxis
                orientation="left"
                width={100}
                stroke={defaultTheme.palette.text.primary}
              />
              <Tooltip
                labelFormatter={(unixTime) =>
                  moment.unix(unixTime).format('DD.MM.YY HH:mm')
                }
                isAnimationActive={false}
              />
              <Bar
                dataKey="quantity"
                fill={defaultTheme.palette.primary.main}
                name="Number of Clients in Network"
                isAnimationActive={true}
              />
              <Legend align="center" verticalAlign="top" height={36} />
            </BarChart>
          </ResponsiveContainer>
        </Box>
      </Paper>

      <Box
        sx={{
          display: 'flex',
          justifyContent: 'center',
          marginTop: 5,
        }}
      >
        <Button
          className={classes.buttonSend}
          variant="contained"
          color="primary"
          style={{ marginRight: '20px' }}
          size='large'
          onClick={() => handleDateTypeChange('day')}
        >
          Day
        </Button>
        <Button
          className={classes.buttonSend}
          variant="contained"
          color="primary"
          style={{ marginRight: '20px' }}
          size='large'
          onClick={() => handleDateTypeChange('week')}
        >
          Week
        </Button>
        <Button
          className={classes.buttonSend}
          variant="contained"
          color="primary"
          size='large'
          onClick={() => handleDateTypeChange('month')}
        >
          Month
        </Button>
      </Box>

      <Copyright />

      <Snackbar open={snackbarOpen} onClose={handleSnackbarClose} autoHideDuration={2000}>
        <MuiAlert elevation={6} variant="filled" severity="error">
          {snackbarMessage}
        </MuiAlert>
      </Snackbar>

      <Dialog open={openDialog} onClose={handleCloseDialog}>
        <DialogTitle>MAC-Address: {searchedString} <br></br> Subnet: 192.168.1.0/255</DialogTitle>
        <DialogContent>
          <Table>
            <TableHead>
              <TableRow style={{ backgroundColor: '#f0f0f0' }}>
                <TableCell align='center'>Device connection time stamps</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {timestamps.map((timestamp, index) => (
                <TableRow key={index} style={{ backgroundColor: index % 2 === 1 ? '#f0f0f0' : 'white' }}>
                  <TableCell align='center'>{formatTimestamp(timestamp.time_stamps)}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog} color="primary">
            Close
          </Button>
        </DialogActions>
      </Dialog>

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