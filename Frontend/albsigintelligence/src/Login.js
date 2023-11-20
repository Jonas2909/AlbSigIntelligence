import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Avatar from '@mui/material/Avatar';
import Button from '@mui/material/Button';
import CssBaseline from '@mui/material/CssBaseline';
import TextField from '@mui/material/TextField';
import Link from '@mui/material/Link';
import Grid from '@mui/material/Grid';
import Box from '@mui/material/Box';
import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import Dialog from '@mui/material/Dialog';
import DialogContent from '@mui/material/DialogContent';
import Snackbar from '@mui/material/Snackbar';
import MuiAlert from '@mui/material/Alert';

function Copyright(props) {
  return (
    <Typography variant="body2" color="text.secondary" align="center" {...props}>
      {'Copyright © '}
      <Link color="inherit" href="https://www.hs-albsig.de/">
        AlbSigIntelligence
      </Link>{' '}
      {new Date().getFullYear()}
      {'.'}
    </Typography>
  );
}

const defaultTheme = createTheme();

export default function SignIn() {
  const [openSignupDialog, setOpenSignupDialog] = useState(false);
  const [username, setUsername] = useState();
  const [password, setPassword] = useState();
  const [snackbarOpen, setSnackbarOpen] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!username || !password) {
      setSnackbarMessage("Please fill out all fields!");
      setSnackbarOpen(true);
      return
    }
    try {
      const response = await fetch('http://localhost:5000/GetUser', {
        headers: { "Content-Type": "application/json" },
        method: "POST",
        mode: 'cors',
        redirect: 'follow',
        body: JSON.stringify({ "username": username }),
      });

      if (response.status === 404) {
        setSnackbarMessage("User not found in the database. Please sign-up.");
        setSnackbarOpen(true);
      } else if (response.status === 500) {
        setSnackbarMessage("Database connection failed");
        setSnackbarOpen(true);
      } else if (!response.ok) {
        throw new Error(`Request failed with status: ${response.status}`);
      }

      const userData = await response.json();
      console.log('User Data:', userData.user);
      if (username === userData.user.username && password === userData.user.password) {
        sessionStorage.setItem('isLoggedIn', 'true');
        navigate('/Visualization');
      } else {
        setSnackbarMessage("Password not correct! Try again!");
        setSnackbarOpen(true);
      }

    } catch (error) {
      console.error(error.message);
    }
  };

  const handleSnackbarClose = (event, reason) => {
    if (reason === 'clickaway') {
      return;
    }
    setSnackbarOpen(false);
  };

  const handleSignupSubmit = (event) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);

    console.log({
      firstnameinput: data.get('firstname'),
      lastnameinput: data.get('lastname'),
      usernameinput: data.get('username'),
      passwordinput: data.get('password'),
    });
    handleSignupClose();
  };

  const handleSignupClick = () => {
    setOpenSignupDialog(true);
  };

  const handleSignupClose = () => {
    setOpenSignupDialog(false);
  };

  return (
    <ThemeProvider theme={defaultTheme}>
      <Container component="main" maxWidth="xs">
        <CssBaseline />
        <Box
          sx={{
            border: `4px solid ${defaultTheme.palette.primary.main}`,
            borderRadius: 8,
            marginTop: 8,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            padding: 3,
          }}
        >
          <Avatar sx={{ m: 1, bgcolor: 'primary.main' }}>
            <LockOutlinedIcon />
          </Avatar>
          <Typography component="h1" variant="h5" textAlign="center">
            Dear User, Thank you for using our services. To access your account, please enter your user credentials.
          </Typography>
          <Box component="form" onSubmit={handleSubmit} noValidate sx={{ mt: 1 }}>
            <TextField
              margin="normal"
              required
              fullWidth
              id="username"
              label="Username"
              name="username"
              autoComplete="username"
              autoFocus
              onChange={(e) => setUsername(e.target.value)}
            />
            <TextField
              margin="normal"
              required
              fullWidth
              name="password"
              label="Password"
              type="password"
              id="password"
              autoComplete="current-password"
              onChange={(e) => setPassword(e.target.value)}
            />
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
            <Button
              type="submit"
              fullWidth
              variant="contained"
              sx={{ mt: 3, mb: 2 }}
            >
              Login
            </Button>
            <Button
              type="submit"
              fullWidth
              variant="contained"
              sx={{ mt: 3, mb: 2 }}
              onClick={handleSignupClick}
            >
              Sign-Up
            </Button>
            <Grid container>
              <Grid item xs>
              </Grid>
              <Grid item>
              </Grid>
            </Grid>
          </Box>
        </Box>
        <Copyright sx={{ mt: 8, mb: 4 }} />

        <Dialog open={openSignupDialog} onClose={handleSignupClose}>
          <DialogContent>
            <form onSubmit={handleSignupSubmit}>
              <TextField
                margin="normal"
                required
                fullWidth
                id="firstname"
                label="Firstname"
                name="firstname"
              />
              <TextField
                margin="normal"
                required
                fullWidth
                id="lastname"
                label="Lastname"
                name="lastname"
              />
              <TextField
                margin="normal"
                required
                fullWidth
                id="username"
                label="Username"
                name="username"
              />
              <TextField
                margin="normal"
                required
                fullWidth
                id="password"
                label="Password"
                name="password"
                type='password'
              />
              <Button type="submit" fullWidth variant="contained" sx={{ mt: 3 }}>
                Submit
              </Button>
            </form>
          </DialogContent>
        </Dialog>

      </Container>
    </ThemeProvider>
  );
}