import React, { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';

const AuthResult = () => {
  const location = useLocation();
  const [message, setMessage] = useState('');
  const [messageType, setMessageType] = useState('');

  useEffect(() => {
    const queryParams = new URLSearchParams(location.search);
    setMessage(queryParams.get('message') ?? '');    
    setMessageType(queryParams.get('message_type') ?? '');  
    }, [location]);

  return (
    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
      <div style={{ textAlign: 'center', padding: '20px', border: '1px solid #ddd', borderRadius: '5px' }}>
        <h1>Authentication Result</h1>
        <p style={{ color: messageType === 'success' ? 'green' : 'red' }}>{message}</p>
      </div>
    </div>
  );
};

export default AuthResult;
