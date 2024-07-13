import React from 'react';
import styled from 'styled-components';

const Arrow = styled.span<{ isSorted: boolean; isAscending: boolean }>`
    margin-left: 0.5rem;
    display: inline-block;
    transition: transform 0.3s;
    transform: ${props => (props.isSorted ? (props.isAscending ? 'rotate(0deg)' : 'rotate(180deg)') : 'rotate(90deg)')};
`;

interface ArrowIconProps {
    isSorted: boolean;
    isAscending: boolean;
}

const ArrowIcon: React.FC<ArrowIconProps> = ({ isSorted, isAscending }) => {
    return (
        <Arrow isSorted={isSorted} isAscending={isAscending}>
        ▲
        </Arrow>
    );
};

export default ArrowIcon;
