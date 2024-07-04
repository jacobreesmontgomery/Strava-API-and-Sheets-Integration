import React from 'react';
import styled from 'styled-components';

// Styled components
const Container = styled.div`
    max-width: 50rem;
    margin: 0 auto;
    padding: 1.25rem;
    background-color: #ffffff;
    box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.1);
    border-radius: 0.5rem;
`;

const Title = styled.h2`
    font-size: 150%;
    margin-bottom: 1.25rem;
    color: #333;
`;

const Content = styled.div`
    font-size: 1.1em;
    line-height: 1.6;
`;

const Table = styled.table`
    width: 100%;
    border-collapse: collapse;
    margin-top: 1.25rem;
`;

const TableHeader = styled.th`
    background-color: #333;
    color: #ffffff;
    padding: 0.75rem;
    text-align: left;
`;

const TableRow = styled.tr`
    &:nth-child(even) {
        background-color: #f4f4f9;
    }
`;

const TableData = styled.td`
    padding: 0.75rem;
    border: 1px solid #ddd;
`;

function Home() {
    return (
        <Container>
            <Title>Welcome to The Goon Squad homepage!</Title>
            <Content>
                This page is for all of my goons! Here is a rundown of each tab...
                <Table>
                    <thead>
                        <TableRow>
                            <TableHeader>Tab</TableHeader>
                            <TableHeader>Description</TableHeader>
                        </TableRow>
                    </thead>
                    <tbody>
                        <TableRow>
                            <TableData>Basic Stats</TableData>
                            <TableData>Holds basic stats on the current week of training for each athlete.</TableData>
                        </TableRow>
                        <TableRow>
                            <TableData>Database</TableData>
                            <TableData>Holds all of my goon's runs since the start of data acquisition.</TableData>
                        </TableRow>
                    </tbody>
                </Table>
            </Content>
        </Container>
    );
};

export default Home;
