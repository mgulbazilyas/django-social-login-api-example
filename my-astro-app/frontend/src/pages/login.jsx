// src/pages/login.jsx

import React from 'react';
import { Link } from 'react-router-dom';

const LoginPage = () => (
  <div>
    <h1>Login</h1>
    <a href="/auth/google/login">Login with Google</a><br />
    <a href="/auth/facebook/login">Login with Facebook</a><br />
    <a href="/auth/tiktok/login">Login with TikTok</a>
  </div>
);

export default LoginPage;
