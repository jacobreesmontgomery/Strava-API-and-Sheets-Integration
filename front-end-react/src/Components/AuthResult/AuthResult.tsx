import React, { useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import styled from 'styled-components';


const Container = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f8f9fa;
`;

const MessageBox = styled.div`
  text-align: center;
  padding: 30px;
  border: 1px solid #ddd;
  border-radius: 10px;
  background-color: #ffffff;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
`;

const Title = styled.h1`
  margin-bottom: 20px;
  font-size: 24px;
  color: #333;
`;

const Message = styled.p<{ type: string }>`
  color: ${({ type }) => (type === 'success' ? 'green' : 'red')};
  font-size: 18px;
  margin-bottom: 20px;
`;

const HomeButton = styled.button`
  padding: 10px 20px;
  font-size: 16px;
  color: #fff;
  background-color: #007bff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  &:hover {
    background-color: #0056b3;
  }
`;

const AuthResult = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [message, setMessage] = useState('');
  const [messageType, setMessageType] = useState('');

  useEffect(() => {
    const queryParams = new URLSearchParams(location.search);
    setMessage(queryParams.get('message') ?? '');
    setMessageType(queryParams.get('message_type') ?? '');
  }, [location]);

  const handleRedirect = () => {
    navigate('/');
  };

  return (
    <Container>
      <MessageBox>
        <Title>Authentication Complete</Title>
        <Message type={messageType}>{message}</Message>
        <HomeButton onClick={handleRedirect}>Go to the homepage.</HomeButton>
      </MessageBox>
    </Container>
  );
};

export default AuthResult;
