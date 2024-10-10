import React, { useState, useEffect } from 'react';
import axios from 'axios';

const HomePage = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState(null);
  const [error, setError] = useState('');

  // Check if access_token is in localStorage
  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (token) {
      setIsAuthenticated(true);
      // Fetch current user details
      fetchUserDetails(token);
    } else {
      setIsAuthenticated(false);
    }
  }, []);

  const fetchUserDetails = async (token) => {
	try {
	  const response = await axios.get('http://127.0.0.1:8000/api/users/me/', {
		headers: {
		  Authorization: `Bearer ${token}`,
		  "Content-Type": "application/json",
		  "X-Requested-With": "XMLHttpRequest" // Ensure this is set for DRF to recognize the XHR request
		},
		withCredentials: true // Ensures that cookies are sent along with requests if needed for CSRF protection
	  });
	  setUser(response.data); // Assuming response contains user object with name and email
	} catch (err) {
	  setError('Error fetching user details');
	}
  };
  

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    setIsAuthenticated(false);
    setUser(null); // Clear user details on logout
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
      <h1 className="text-4xl font-bold mb-6">Welcome to the Homepage</h1>
      
      {isAuthenticated ? (
        <div className="text-center">
          {user ? (
            <div className="mb-4">
              <h2 className="text-2xl">Hello, {user.name}</h2>
              <p className="text-lg">Email: {user.email}</p>
            </div>
          ) : (
            <p>Loading user details...</p>
          )}
          <button
            onClick={handleLogout}
            className="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600 transition"
          >
            Logout
          </button>
        </div>
      ) : (
        <div className="flex space-x-4">
          <a
            href="/login"
            className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 transition"
          >
            Login
          </a>
          <a
            href="/register"
            className="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600 transition"
          >
            Register
          </a>
        </div>
      )}

      {error && <p className="text-red-500 mt-4">{error}</p>}
    </div>
  );
};

export default HomePage;
