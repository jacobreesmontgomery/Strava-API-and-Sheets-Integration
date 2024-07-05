import React, { useEffect, useState } from 'react';
import axios from 'axios';
import styled from 'styled-components';
import Table from '../Table/Table.tsx';
import "../../App.css"

// CAVEAT TO THIS: Must be updated any time an update is made to the .env file for these two variables
const ATHLETE_DATA_FIELDNAMES = ["ATHLETE", "ACTIVITY ID", "RUN", "MOVING TIME", "DISTANCE (MI)", "PACE (MIN/MI)", "FULL DATE", "TIME", "DAY", "MONTH", "DATE", "YEAR", "SPM AVG", "HR AVG", "WKT TYPE", "DESCRIPTION", "TOTAL ELEV GAIN (FT)", "MANUAL", "MAX SPEED (FT/S)", "CALORIES", "ACHIEVEMENT COUNT", "KUDOS COUNT", "COMMENT COUNT", "ATHLETE COUNT", "FULL DATETIME"]
const ATHLETE_DATA_FILTERED_FIELDNAMES = ["ATHLETE", "RUN", "MOVING TIME", "DISTANCE (MI)", "PACE (MIN/MI)", "SPM AVG", "HR AVG", "WKT TYPE", "DESCRIPTION", "TOTAL ELEV GAIN (FT)", "FULL DATETIME"]
const INDICES_TO_FILTER = ATHLETE_DATA_FILTERED_FIELDNAMES.map(field => ATHLETE_DATA_FIELDNAMES.indexOf(field));

function Database() {
    const [headerStats, setHeaderStats] = useState<string[]>([]);
    const [rowData, setRowData] = useState<string[][]>([]);
    const [sortConfig, setSortConfig] = useState<{ key: string; direction: 'ascending' | 'descending' } | null>(null);
    const [filters, setFilters] = useState<string[]>([]);

    useEffect(() => {
        axios.get('http://127.0.0.1:5000/api/database')
        .then(response => {
            setHeaderStats(filterHeaderStats(response.data.headerStats));
            setRowData(filterRowData(response.data.rowData));
            setFilters(new Array(response.data.headerStats.length).fill(''));
        })
        .catch(error => {
            console.error("There was an error fetching the data!", error);
        });
    }, []);

    const filterHeaderStats = (headerStats: string[]) => {
        return headerStats.filter(header => ATHLETE_DATA_FILTERED_FIELDNAMES.includes(header));
    }

    const filterRowData = (rowData: string[][]) => {
        return rowData.map(row => INDICES_TO_FILTER.map(index => row[index]));
    }

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
        <div className='stats-container'>
            <h2>Database</h2>
            <Table
                headers={headerStats}
                rowData={rowData}
                sortConfig={sortConfig}
                handleSort={handleSort}
                filters={filters}
                handleFilterChange={handleFilterChange}
            />
        </div>
    );
}

export default Database