export interface FilterField {
  name: string;
  label: string;
  type: 'text' | 'number' | 'date' | 'select';
  options?: { label: string; value: any }[];
}

export type FilterOperator = 'equals' | 'contains' | 'startsWith' | 'endsWith' | 'greaterThan' | 'lessThan' | 'between';

export interface FilterCondition {
  field: string;
  operator: FilterOperator;
  value: any;
  value2?: any; // For 'between' operator
}

export interface FilterGroup {
  conditions: FilterCondition[];
  operator: 'AND' | 'OR';
}

export interface MultiFilterState {
  groups: FilterGroup[];
}

export interface FilterBarProps {
  fields: FilterField[];
  onFilterChange: (filterState: MultiFilterState) => void;
  initialFilters?: MultiFilterState;
} 