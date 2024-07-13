import React from 'react';
import styled from 'styled-components';

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
        <div className='stats-container'>
            <h2>Welcome to The Goon Squad homepage!</h2>
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
        </div>
    );
};

export default Home;
