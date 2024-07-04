import React from 'react';
import styled from 'styled-components';
import ArrowIcon from '../ArrowIcon/ArrowIcon.tsx';

const ThStyled = styled.th<{ $colCount: number }>`
    background-color: #f4f4f9;
    color: #333;
    padding: 0.75rem;
    text-align: center;
    cursor: pointer;
    width: ${props => `calc(100% / ${props.$colCount})`};
    position: relative;
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

const Th: React.FC<ThProps> = ({
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

export default Th;
