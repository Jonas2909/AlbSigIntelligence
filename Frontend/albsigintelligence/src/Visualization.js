import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Dialog, DialogTitle, DialogContent, DialogActions, Button } from '@material-ui/core';

export default function Visualization() {
    const navigate = useNavigate();
    const [isDialogOpen, setDialogOpen] = useState(false);

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

    return (
      <div>
        <h1>Visualization</h1>
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
      </div>
    );
  }