import React, { useEffect, useState } from 'react';
import { createRoot } from 'react-dom/client';
import { FilterBar } from './FilterBar';
import { FilterField } from '../types/filters';

// Add type declarations for window object
declare global {
  interface Window {
    activeFilters: Record<string, any>;
    currentPage: number;
    updateScheduleTable: (schedules: any[]) => void;
    allSchedules: any[];
  }
}

// Helper to fetch options from backend endpoints
async function fetchOptions(url: string, labelKey: string, valueKey: string) {
  const res = await fetch(url);
  if (!res.ok) return [];
  const data = await res.json();
  return data.map((item: any) => ({ label: item[labelKey], value: item[valueKey] }));
}

const FilterBarWithOptions: React.FC<{ onFilterChange: (filters: Record<string, any>) => void }> = ({ onFilterChange }) => {
  const [fields, setFields] = useState<FilterField[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadOptions() {
      // Fetch options for each select field
      const [programs, trainings, faculty, halls, departments] = await Promise.all([
        fetchOptions('/api/programs/', 'name', 'name'),
        fetchOptions('/api/trainings/', 'training_name', 'training_name'),
        fetchOptions('/api/faculty/', 'name', 'name'),
        fetchOptions('/api/halls/', 'name', 'name'),
        fetchOptions('/api/departments/', 'name', 'name'),
      ]);
      setFields([
        { name: 'program', label: 'Program', type: 'select', options: programs },
        { name: 'training_name', label: 'Training Name', type: 'select', options: trainings },
        { name: 'faculty', label: 'Faculty', type: 'select', options: faculty },
        { name: 'hall', label: 'Hall', type: 'select', options: halls },
        { name: 'date', label: 'Date', type: 'date' },
        { name: 'status', label: 'Status', type: 'select', options: [
          { label: 'Planned', value: 'Planned' },
          { label: 'Completed', value: 'Completed' },
          { label: 'Cancelled', value: 'Cancelled' },
          { label: 'Incomplete', value: 'Incomplete' },
          { label: 'Postponed', value: 'Postponed' }
        ] },
        { name: 'department', label: 'Department', type: 'select', options: departments },
      ]);
      setLoading(false);
    }
    loadOptions();
  }, []);

  if (loading) return <div>Loading filters...</div>;
  return <FilterBar onFilterChange={onFilterChange} fields={fields} />;
};

const handleFilterChange = (filters: Record<string, any>) => {
  window.activeFilters = filters;
  window.currentPage = 1;
  window.updateScheduleTable(window.allSchedules);
  const clearBtnRow = document.getElementById('clearFiltersRow');
  if (clearBtnRow) {
    clearBtnRow.style.display = Object.values(filters).some(v => v) ? '' : 'none';
  }
};

const container = document.getElementById('react-filter-bar');
if (container) {
  createRoot(container).render(<FilterBarWithOptions onFilterChange={handleFilterChange} />);
} 