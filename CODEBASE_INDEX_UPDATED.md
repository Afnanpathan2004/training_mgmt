# Training Management System - Updated Codebase Index

## Project Overview
A comprehensive Training Management System built with Django (backend) and React/TypeScript (frontend components). The system manages training programs, faculty, schedules, attendance, assessments, and provides advanced administrative features with sophisticated scheduling capabilities.

## Technology Stack

### Backend
- **Framework**: Django 4.2+ with SQLite database
- **Authentication**: Django's built-in authentication system
- **File Processing**: openpyxl and pandas for Excel operations
- **Storage**: Local file storage with OneDrive sync capability
- **API**: Django REST Framework for AJAX operations
- **Security**: Comprehensive security settings with CSRF protection

### Frontend
- **Framework**: React 18.2.0 with TypeScript 4.9.0
- **UI Framework**: Bootstrap 5 with Font Awesome icons
- **Calendar**: FullCalendar.js for advanced scheduling
- **Build Tools**: react-scripts 5.0.1

### Data Processing
- **Excel Processing**: openpyxl and pandas for data analysis
- **File Upload**: Comprehensive file handling with validation
- **Backup/Restore**: Database backup and restore functionality

## Project Structure

### Root Directory
```
/
├── training_mgmt/          # Main Django project
│   ├── training_mgmt/      # Django project settings
│   ├── dashboard/          # Main Django app
│   ├── media/              # Media files
│   ├── static/             # Static files
│   ├── staticfiles/        # Collected static files
│   ├── local_storage/      # Local file storage
│   └── db.sqlite3          # SQLite database (1.8GB)
├── src/                    # Frontend React/TypeScript components
├── dashboard/              # Additional dashboard components
├── media/                  # Media files
├── onedrive_data/         # OneDrive sync data
├── requirements.txt       # Python dependencies (50 packages)
├── package.json           # Node.js dependencies
├── tsconfig.json          # TypeScript configuration
├── .gitignore             # Git ignore rules
└── Various Excel files    # Training data files
```

## Django Application Architecture

### Core Django Files (`training_mgmt/`)
- **`manage.py`** - Django management script
- **`training_mgmt/settings.py`** - Main Django settings with comprehensive security configurations
- **`training_mgmt/urls.py`** - Main URL configuration
- **`training_mgmt/wsgi.py`** - WSGI configuration
- **`training_mgmt/asgi.py`** - ASGI configuration
- **`backup_restore.py`** - Backup and restore functionality (174 lines)

### Dashboard App (`training_mgmt/dashboard/`)

#### Models (`models.py` - 557 lines)

**Core Models:**
- **`AuditLog`** - Comprehensive audit trail with JSON field for detailed change tracking
- **`Program`** - Training programs with categories (SHE, CB, F&T, Induction) and status tracking
- **`Training`** - Individual training sessions with comprehensive metadata and faculty relationships
- **`Faculty`** - Training faculty members with extended employee information and HR data integration
- **`Employee`** - Employee information with comprehensive HR data fields
- **`Hall`** - Training venue management with capacity tracking

**Scheduling Models:**
- **`Schedule`** - Advanced training scheduling with conflict detection, status tracking, and notification management
- **`ProgramScheduleDate`** - Program-specific scheduling dates
- **`DetailedSchedule`** - Detailed schedule information with attachments and notes
- **`DetailedScheduleSnapshot`** - Schedule snapshots for historical tracking and analysis

**Attendance & Metrics:**
- **`TrainingAttendance`** - Attendance tracking per training session
- **`TrainingMetrics`** - Training performance metrics and analytics
- **`Attendance`** - Schedule-based attendance tracking with participant counts
- **`TrainingAttendanceFile`** - Attendance file uploads and processing

**Document Management:**
- **`MORUpload`** - Monthly Operating Report uploads and management
- **`ProgramDocument`** - Document management for programs
- **`Participant`** - Training participants with contact information

#### Assessment Models (`assessment_models.py` - 109 lines)
- **`Feedback`** - Training feedback with rating system (1-5 scale)
- **`PreAssessment`** - Pre-training knowledge assessment with objectives
- **`PostAssessment`** - Post-training effectiveness assessment with outcomes
- **`ManagerChecklist`** - Manager evaluation of training impact
- **`ROIData`** - Return on Investment tracking and analytics
- **`FeedbackExcelUpload`** - Excel file uploads for assessment data

#### Views (`views.py` - 4425 lines)

**Dashboard & Analytics:**
- Dashboard views with comprehensive statistics and analytics
- Home page with program, training, faculty, and participant statistics
- Calendar and scheduling interfaces

**File Management:**
- Excel file upload and processing with validation
- OneDrive synchronization capabilities
- File editing and management interfaces
- MOR (Monthly Operating Report) handling

**CRUD Operations:**
- Program and training management with full CRUD operations
- Faculty management and assignment
- Document upload and management
- Participant management

**Advanced Scheduling:**
- FullCalendar.js integration for visual scheduling
- Hall/venue management with capacity tracking
- Conflict detection and resolution
- Batch scheduling operations
- Schedule document uploads
- Schedule snapshots and notifications

**API Endpoints:**
- Comprehensive REST API for AJAX operations
- Rate limiting and security measures
- Pagination and filtering capabilities
- Real-time data updates

**Attendance Management:**
- Attendance tracking and reporting
- Excel-based attendance processing
- Attendance analytics and metrics
- Attendance file management

**Assessment System:**
- Pre/post assessment functionality
- Feedback collection and management
- Manager checklist processing
- ROI data collection and analysis
- Assessment improvement analysis

**Backup & Restore:**
- Database backup and restore functionality
- File-based backup management
- Data integrity verification

#### Assessment Views (`assessment_views.py` - 138 lines)
- Assessment form handling and processing
- Feedback collection and management
- Pre/post assessment functionality
- Manager checklist processing
- ROI data collection and analysis
- Schedule table API with pagination

#### Forms (`forms.py` - 26 lines)
- Custom form classes for data validation
- File upload forms with validation
- Assessment and feedback forms

#### URLs (`urls.py` - 96 lines)
- Main dashboard routes
- API endpoints for AJAX operations
- File management routes
- Assessment and feedback routes
- Attendance management endpoints
- Scheduling and calendar routes
- Schedule-specific operations
- Backup and restore routes

#### Templates (`templates/dashboard/`)
- **`base.html`** - Base template with responsive navigation and Bootstrap 5
- **`home.html`** - Dashboard home page with comprehensive statistics
- **`programs.html`** - Program listing with advanced filtering
- **`all_programs.html`** - Comprehensive program management interface
- **`program_details.html`** - Detailed program view with document management
- **`training_details.html`** - Training details with faculty assignment
- **`scheduling.html`** - Advanced scheduling interface with FullCalendar (5127 lines)
- **`schedule_trainings.html`** - Training scheduling interface (1454 lines)
- **`schedule_program.html`** - Program-specific scheduling interface
- **`filters.html`** - Reusable filter components
- **`backup_restore.html`** - Backup and restore interface
- **`mor_upload.html`** & **`mor_list.html`** - MOR management
- **`upload_excel.html`** & **`edit_excel.html`** - Excel file management
- **`uploaded_files.html`** - File management interface
- Assessment templates in `assessment/` directory
- Component templates in `components/` directory

#### Management Commands (`management/commands/`)
- **`add_default_trainings.py`** - Bulk training creation
- **`create_trainings.py`** - Training data import
- **`load_employees.py`** - Employee data import
- **`backup_restore.py`** - Database backup/restore
- **`cleanup_db.py`** - Database cleanup utilities
- **`verify_trainings.py`** - Data validation
- **`update_schedule_end_dates.py`** - Schedule maintenance
- **`rename_idt.py`** - Data migration utilities
- **`create_test_data.py`** - Test data generation
- **`populate_detailed_schedule_snapshots.py`** - Schedule snapshot creation
- **`set_default_notification_status.py`** - Notification status management

## Frontend Components (`src/`)

### Components (`src/components/`)
- **`FilterBar.tsx`** - Reusable filter component with modal interface (40 lines)
- **`FilterModal.tsx`** - Modal for filter configuration (91 lines)
- **`mountFilterBar.tsx`** - Filter bar mounting utility (75 lines)

### Types (`src/types/`)
- **`filters.ts`** - TypeScript interfaces for filtering system (30 lines):
  - `FilterField` - Field configuration for filters
  - `FilterOperator` - Available filter operators
  - `FilterCondition` - Individual filter conditions
  - `FilterGroup` - Grouped filter conditions
  - `MultiFilterState` - Complete filter state

### Hooks (`src/hooks/`)
- Custom React hooks for state management

### Filters (`src/filters/`)
- Filter logic and utilities

## Key Features

### 1. Program Management
- Create, edit, delete training programs
- Categorize programs (SHE, CB, F&T, Induction)
- Program types (Calendar/Non-Calendar)
- Document upload and management
- Status tracking (Planned, Completed, Postpone, Cancelled)
- Program scheduling with date management
- Audit trail for all changes

### 2. Training Management
- Individual training session management
- Faculty assignment and management
- Training scheduling with venue allocation
- Content and benefits tracking
- Attendance management
- Training type management
- Comprehensive metadata tracking

### 3. Faculty Management
- Faculty profile management with extended employee data
- Department and contact information
- Training assignment tracking
- Active/inactive status management
- Employee data integration with HR systems
- Comprehensive employee information tracking

### 4. Advanced Scheduling System
- FullCalendar.js integration for visual scheduling
- Hall/venue management with capacity tracking
- Conflict detection and resolution
- Batch scheduling operations
- Schedule document uploads
- Program-specific scheduling dates
- Schedule snapshots and notifications
- Detailed schedule management with attachments
- Notification status tracking

### 5. File Management
- Excel file upload and processing
- OneDrive synchronization
- Document management for programs and schedules
- File validation and error handling
- Backup and restore functionality
- Local storage management

### 6. Attendance Management
- Comprehensive attendance tracking
- Excel-based attendance processing
- Attendance analytics and reporting
- Participant counting (with/without personnel numbers)
- Attendance file management
- Attendance metrics and statistics

### 7. Assessment & Feedback System
- Pre/post assessment functionality
- Feedback collection with rating system
- Manager checklist processing
- ROI data collection and analysis
- Assessment improvement analysis
- Excel-based assessment data processing

### 8. Analytics & Reporting
- Dashboard with comprehensive statistics
- Training metrics and analytics
- Attendance reporting
- Faculty performance tracking
- Program effectiveness analysis
- ROI calculations and reporting

### 9. Security & Authentication
- Django's built-in authentication system
- User registration and login
- Role-based access control
- CSRF protection
- Rate limiting for API endpoints
- Comprehensive audit logging

### 10. Data Management
- SQLite database with comprehensive schema
- Data import/export capabilities
- Backup and restore functionality
- Data validation and integrity checks
- Audit trail for all changes
- Historical data tracking

## API Endpoints

### Core APIs
- `/api/schedules/` - Schedule management
- `/api/programs/` - Program management
- `/api/faculty/` - Faculty management
- `/api/trainings/` - Training management
- `/api/halls/` - Hall/venue management

### Assessment APIs
- `/api/feedback/analysis/` - Feedback analysis
- `/api/schedule-table/` - Schedule table with pagination
- Assessment form endpoints

### File Management APIs
- `/api/programs/<id>/upload_document/` - Document upload
- `/api/schedules/<id>/upload-excel/` - Excel upload
- File management and processing endpoints

### Attendance APIs
- `/api/trainings/<ids>/upload_attendance/` - Attendance upload
- `/api/attendance/report/` - Attendance reporting
- Attendance management endpoints

## Database Schema

### Core Tables
- **Programs** - Training programs with categories and status
- **Trainings** - Individual training sessions
- **Faculty** - Training faculty with employee data
- **Employees** - Employee information
- **Halls** - Training venues
- **Schedules** - Training schedules with conflicts detection

### Relationship Tables
- **TrainingAttendance** - Attendance tracking
- **TrainingMetrics** - Performance metrics
- **ProgramScheduleDate** - Program scheduling
- **DetailedSchedule** - Detailed schedule information

### Audit & History
- **AuditLog** - Comprehensive change tracking
- **DetailedScheduleSnapshot** - Schedule history
- **MORUpload** - Monthly reports

## Configuration

### Django Settings
- Comprehensive security settings
- File upload configurations
- Database settings (SQLite)
- Static and media file handling
- OneDrive integration settings
- Session management

### Frontend Configuration
- TypeScript configuration
- React build settings
- Bootstrap 5 integration
- Component library setup

## Dependencies

### Python Dependencies (requirements.txt)
- Django 4.2+ with comprehensive ecosystem
- File processing libraries (openpyxl, pandas)
- Authentication and security packages
- UI enhancement packages (Bootstrap, crispy forms)
- Data analysis and processing tools

### Node.js Dependencies (package.json)
- React 18.2.0 with TypeScript 4.9.0
- Build tools and development dependencies
- UI framework integration

## Development & Deployment

### Development Setup
- Django development server
- React development server
- SQLite database
- Local file storage
- OneDrive sync capability

### Production Considerations
- Database optimization (1.8GB SQLite)
- File storage management
- Security hardening
- Performance optimization
- Backup and restore procedures

## Data Flow

### User Interaction Flow
1. User authentication and authorization
2. Dashboard access with statistics
3. Program and training management
4. Advanced scheduling with calendar interface
5. Attendance tracking and reporting
6. Assessment and feedback collection
7. Analytics and reporting

### Data Processing Flow
1. Excel file upload and validation
2. Data import and processing
3. Schedule generation and conflict detection
4. Attendance tracking and metrics calculation
5. Assessment data analysis
6. Report generation and export

## Security Features

### Authentication & Authorization
- Django's built-in user authentication
- Role-based access control
- Session management
- CSRF protection

### Data Security
- Input validation and sanitization
- File upload security
- SQL injection prevention
- XSS protection

### Audit & Compliance
- Comprehensive audit logging
- Change tracking for all models
- Data integrity verification
- Backup and restore procedures

## Performance Considerations

### Database Optimization
- Proper indexing on frequently queried fields
- Query optimization for large datasets
- Efficient relationship handling

### File Processing
- Efficient Excel file processing
- Large file handling capabilities
- Memory optimization for data processing

### Frontend Performance
- React component optimization
- TypeScript for type safety
- Efficient state management
- Responsive design with Bootstrap 5

This codebase represents a sophisticated Training Management System with comprehensive features for managing training programs, faculty, schedules, attendance, and assessments. The system provides both web-based interfaces and API endpoints for flexible integration and usage. 