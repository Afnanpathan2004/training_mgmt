import React, { useState } from 'react';
import { FilterField, MultiFilterState } from '../types/filters';

interface FilterModalProps {
  show: boolean;
  onClose: () => void;
  onApply: (filters: Record<string, any>) => void;
  onClear: () => void;
  fields: FilterField[];
  initialFilters?: Record<string, any>;
}

export const FilterModal: React.FC<FilterModalProps> = ({
  show,
  onClose,
  onApply,
  onClear,
  fields,
  initialFilters = {}
}) => {
  const [filters, setFilters] = useState<Record<string, any>>(initialFilters);

  const handleChange = (field: string, value: any) => {
    setFilters(prev => ({ ...prev, [field]: value }));
  };

  const handleApply = () => {
    onApply(filters);
    onClose();
  };

  const handleClear = () => {
    setFilters({});
    onClear();
    onClose();
  };

  if (!show) return null;

  return (
    <div className="modal-backdrop" style={{ position: 'fixed', top: 0, left: 0, width: '100vw', height: '100vh', background: 'rgba(0,0,0,0.3)', zIndex: 1050 }}>
      <div className="modal d-block" tabIndex={-1} style={{ zIndex: 1100, maxWidth: 500, margin: '5vh auto' }}>
        <div className="modal-dialog">
          <div className="modal-content">
            <div className="modal-header">
              <h5 className="modal-title">Filter</h5>
              <button type="button" className="btn-close" onClick={onClose}></button>
            </div>
            <div className="modal-body">
              {fields.map(field => (
                <div className="mb-3" key={field.name}>
                  <label className="form-label">{field.label}</label>
                  {field.type === 'select' ? (
                    <select
                      className="form-select"
                      value={filters[field.name] || ''}
                      onChange={e => handleChange(field.name, e.target.value)}
                    >
                      <option value="">All</option>
                      {field.options?.map(opt => (
                        <option key={opt.value} value={opt.value}>{opt.label}</option>
                      ))}
                    </select>
                  ) : field.type === 'date' ? (
                    <input
                      type="date"
                      className="form-control"
                      value={filters[field.name] || ''}
                      onChange={e => handleChange(field.name, e.target.value)}
                    />
                  ) : (
                    <input
                      type="text"
                      className="form-control"
                      value={filters[field.name] || ''}
                      onChange={e => handleChange(field.name, e.target.value)}
                    />
                  )}
                </div>
              ))}
            </div>
            <div className="modal-footer">
              <button type="button" className="btn btn-secondary" onClick={handleClear}>Clear</button>
              <button type="button" className="btn btn-primary" onClick={handleApply}>Apply</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}; 