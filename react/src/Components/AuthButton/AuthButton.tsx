import React from 'react';
import styled from 'styled-components';

const Button = styled.a`
    background-color: orange;
    color: black;
    padding: 0.625rem 1.25rem;
    font-size: 1rem;
    border: none;
    cursor: pointer;
    border-radius: 0.3125rem;
    transition: background-color 0.3s ease;
    text-decoration: none;
    
    &:hover {
        background-color: #e88317; /* Darker shade of orange on hover */
    }
`;

function AuthButton() {
    return (
        <Button href="http://localhost:5001/api/strava_auth">
            Authenticate with my app
        </Button>
    );
}

export default AuthButton;
