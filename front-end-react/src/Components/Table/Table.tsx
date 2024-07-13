import React from 'react';
import styled from 'styled-components';
import Th from '../TableHeader/TableHeader.tsx';

const TableStyled = styled.div`
    width: 100%;
    display: flex;
    flex-direction: column;
    max-height: 32rem;
`;

const TableHeaders = styled.div`
    display: flex;
    background-color: #f4f4f9;
`;

const TableBody = styled.div`
    display: flex;
    flex-direction: column;
    overflow-y: auto; /* Add vertical scrollbar */
`;

const TableRow = styled.div`
    display: flex;
    &:nth-child(even) {
        background-color: #f4f4f9;
    }
`;

const TableData = styled.div`
    padding: 0.75rem;
    flex: 1;
    text-align: left;
    border-bottom: 0.0625rem solid #ddd;
    box-sizing: border-box;
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
            <TableHeaders>
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
            </TableHeaders>
            <TableBody>
                {filteredData.map((row, rowIndex) => (
                    <TableRow key={rowIndex}>
                        {row.map((cell, cellIndex) => (
                            <TableData key={cellIndex}>{cell}</TableData>
                        ))}
                    </TableRow>
                ))}
            </TableBody>
        </TableStyled>
    );
};

export default Table;