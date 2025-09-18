import React, { useState } from 'react';
import { FilterModal } from './FilterModal';
import { FilterField } from '../types/filters';

interface FilterBarProps {
  onFilterChange: (filters: Record<string, any>) => void;
  initialFilters?: Record<string, any>;
  fields: FilterField[];
}

export const FilterBar: React.FC<FilterBarProps> = ({ onFilterChange, initialFilters, fields }) => {
  const [showModal, setShowModal] = useState(false);
  const [filters, setFilters] = useState<Record<string, any>>(initialFilters || {});

  const handleApply = (newFilters: Record<string, any>) => {
    setFilters(newFilters);
    onFilterChange(newFilters);
  };

  const handleClear = () => {
    setFilters({});
    onFilterChange({});
  };

  return (
    <>
      <button className="btn btn-outline-primary mb-3" onClick={() => setShowModal(true)}>
        <i className="fas fa-filter"></i> Filter
      </button>
      <FilterModal
        show={showModal}
        onClose={() => setShowModal(false)}
        onApply={handleApply}
        onClear={handleClear}
        fields={fields}
        initialFilters={filters}
      />
    </>
  );
}; 