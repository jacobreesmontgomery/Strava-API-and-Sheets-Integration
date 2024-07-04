import React, { useEffect, useState } from 'react';
import axios from 'axios';
import styled from 'styled-components';
import Table from '../Table/Table.tsx';

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

function Database() {
    const [headerStats, setHeaderStats] = useState<string[]>([]);
    const [rowData, setRowData] = useState<string[][]>([]);
    const [sortConfig, setSortConfig] = useState<{ key: string; direction: 'ascending' | 'descending' } | null>(null);
    const [filters, setFilters] = useState<string[]>([]);

    useEffect(() => {
        axios.get('http://127.0.0.1:5000/api/database')
        .then(response => {
            setHeaderStats(response.data.headerStats);
            setRowData(response.data.rowData);
            setFilters(new Array(response.data.headerStats.length).fill(''));
        })
        .catch(error => {
            console.error("There was an error fetching the data!", error);
        });
    }, []);

    const handleSort = (key: string) => {
        let direction: 'ascending' | 'descending' = 'ascending';
        if (sortConfig && sortConfig.key === key && sortConfig.direction === 'ascending') {
        direction = 'descending';
        }
        setSortConfig({ key, direction });
    };

    const handleFilterChange = (index: number, value: string) => {
        const newFilters = [...filters];
        newFilters[index] = value;
        setFilters(newFilters);
    };

    return (
        <Container>
            <Title>Database</Title>
            <Table
                headers={headerStats}
                rowData={rowData}
                sortConfig={sortConfig}
                handleSort={handleSort}
                filters={filters}
                handleFilterChange={handleFilterChange}
            />
        </Container>
    );
}

export default Database