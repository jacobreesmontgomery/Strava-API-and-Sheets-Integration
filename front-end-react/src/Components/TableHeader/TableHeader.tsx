import React from 'react';
import styled from 'styled-components';
import ArrowIcon from '../ArrowIcon/ArrowIcon.tsx';

const ThStyled = styled.div<{ $colCount: number }>`
    background-color: #333;
    color: #fff;
    padding: 0.75rem;
    text-align: center;
    cursor: pointer;
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    box-sizing: border-box;
`;

const ThContent = styled.div`
    display: flex;
    align-items: center;
    justify-content: center;
`;

const FilterInput = styled.input`
    width: 100%;
    margin-top: 0.5rem;
    padding: 0.25rem;
    box-sizing: border-box;
`;

interface ThProps {
    header: string;
    isSorted: boolean;
    isAscending: boolean;
    onClick: () => void;
    colCount: number;
    filterValue: string;
    onFilterChange: (event: React.ChangeEvent<HTMLInputElement>) => void;
}

const TableHeader: React.FC<ThProps> = ({
    header,
    isSorted,
    isAscending,
    onClick,
    colCount,
    filterValue,
    onFilterChange,
}) => (
    <ThStyled onClick={onClick} $colCount={colCount}>
        <ThContent>
            {header}
            <ArrowIcon isSorted={isSorted} isAscending={isAscending} />
        </ThContent>
        <FilterInput
            type="text"
            value={filterValue}
            onChange={onFilterChange}
            placeholder="Filter..."
        />
    </ThStyled>
);

export default TableHeader;