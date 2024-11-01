// src/pages/auth/[provider]/callback.jsx

import React, { useEffect } from 'react';

const ProviderCallback = ({ params }) => {

  useEffect(() => {
    console.log("Provider callback");
    const exchangeCodeForToken = async () => {
      const queryParams = new URLSearchParams(window.location.search);
      const code = queryParams.get('code');

      const response = await fetch('http://localhost:8000/api/auth/token/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ provider: params.provider, code }),
      });

      const data = await response.json();
      if (data.access) {
        // Store tokens in localStorage or cookies
        localStorage.setItem('access_token', data.access);
        localStorage.setItem('refresh_token', data.refresh);

        // Redirect to the home page or dashboard
        window.location.href = '/';
      } else {
        // Handle errors
        console.error('Authentication failed:', data);
      }
    };

    exchangeCodeForToken();
  }, [params.provider]);

  return <div>Authenticating with {params.provider}...</div>;
};

export default ProviderCallback;
