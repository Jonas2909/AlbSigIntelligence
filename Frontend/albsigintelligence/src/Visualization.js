import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

export default function Visualization() {
    const navigate = useNavigate();

    useEffect(() => {
        // Check session status
        const isLoggedIn = sessionStorage.getItem('isLoggedIn');
        if (!isLoggedIn) {
          // Redirect to login if not logged in
          console.log("User not logged in!");
          navigate('/');
        }
      }, [navigate]);

  return (
    <h1>Visualization</h1>
  );
}