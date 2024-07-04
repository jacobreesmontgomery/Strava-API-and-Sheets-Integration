import React from 'react';
import styled from 'styled-components';
import Th from '../Th/Th.tsx';

const TableStyled = styled.table`
    width: 100%;
    border-collapse: collapse;
    max-height: 18.75rem; /* Adjust max-height as needed */
`;

// TODO: Fix issue with table dimensions. When block display is on, I can
// use the scroller. But with it, the columns get out of line. Without it, 
// they are in line but then I have no scroller.
const Thead = styled.thead`
    background-color: #f4f4f9;
    /* display: block; */
`;

const Td = styled.td`
    padding: 0.75rem;
    text-align: center;
    border-bottom: 0.0625rem solid #ddd;
`;

const Tbody = styled.tbody`
    max-height: 21.875rem; /* Adjust height as needed */
    overflow-y: auto; /* Add vertical scrollbar */
    /* display: block; Ensure proper layout */
`;

interface TableProps {
    headers: string[];
    rowData: string[][];
    sortConfig: { key: string; direction: 'ascending' | 'descending' } | null;
    handleSort: (key: string) => void;
    filters: string[];
    handleFilterChange: (index: number, value: string) => void;
}

const Table: React.FC<TableProps> = ({
    headers,
    rowData,
    sortConfig,
    handleSort,
    filters,
    handleFilterChange,
}) => {
    const sortedData = React.useMemo(() => {
        if (sortConfig !== null) {
            const sorted = [...rowData].sort((a, b) => {
                const aKey = a[headers.indexOf(sortConfig.key)];
                const bKey = b[headers.indexOf(sortConfig.key)];
                if (aKey < bKey) {
                    return sortConfig.direction === 'ascending' ? -1 : 1;
                }
                if (aKey > bKey) {
                    return sortConfig.direction === 'ascending' ? 1 : -1;
                }
                return 0;
            });
            return sorted;
        }
        return rowData;
    }, [rowData, sortConfig, headers]);

    const filteredData = sortedData.filter(row =>
        row.every((cell, index) => cell.toLowerCase().includes(filters[index].toLowerCase()))
    );

    return (
        <TableStyled>
            <Thead>
                <tr>
                {headers.map((header, index) => (
                    <Th
                        key={index}
                        header={header}
                        isSorted={sortConfig?.key === header}
                        isAscending={sortConfig?.direction === 'ascending'}
                        onClick={() => handleSort(header)}
                        colCount={headers.length}
                        filterValue={filters[index]}
                        onFilterChange={(e) => handleFilterChange(index, e.target.value)}
                    />
                ))}
                </tr>
            </Thead>
            <Tbody>
                {filteredData.map((row, rowIndex) => (
                    <tr key={rowIndex}>
                        {row.map((cell, cellIndex) => (
                            <Td key={cellIndex}>{cell}</Td>
                        ))}
                    </tr>
                ))}
            </Tbody>
        </TableStyled>
    );
};

export default Table;
