// src/pages/auth/[provider]/login.jsx

import React, { useEffect, useState } from 'react';

const ProviderLogin = ({ params }) => {
  const [authUrl, setAuthUrl] = useState('');

  useEffect(() => {
    const getAuthUrl = async () => {
      const response = await fetch(`http://localhost:8000/api/auth/${params.provider}/login/`);
      const data = await response.json();
      setAuthUrl(data.auth_url);
    };
    getAuthUrl();
  }, [params.provider]);

  useEffect(() => {
    if (authUrl) {
      window.location.href = authUrl;
    }
  }, [authUrl]);

  return <div>Redirecting to {params.provider} login...</div>;
};

export default ProviderLogin;
