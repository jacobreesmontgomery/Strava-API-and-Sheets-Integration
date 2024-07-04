import React from 'react'
import styled from 'styled-components'

const NavbarContainer = styled.div`
    background-color: #333;
    padding: 10px;
    color: white;
    display: flex;
    justify-content: space-between;
    align-items: center;
`;

const NavbarTitle = styled.h1`
    margin: 0;
`;

const NavbarLinks = styled.div`
    display: flex;
    gap: 20px;
`;

const NavbarLink = styled.a`
    color: white;
    text-decoration: none;
    padding: 5px 10px;
    border-radius: 5px;

    &:hover {
        background-color: #575757;
    }
`;

function Navbar() {
    return (
        <NavbarContainer>
            <NavbarTitle>Strava API</NavbarTitle>
            <NavbarLinks>
                <NavbarLink href="/">Home</NavbarLink>
                <NavbarLink href="/basic-stats">Basic Stats</NavbarLink>
                <NavbarLink href="/database">Database</NavbarLink>
            </NavbarLinks>
        </NavbarContainer>
    )
}

export default Navbar
