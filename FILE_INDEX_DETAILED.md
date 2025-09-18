# Training Management System - Detailed File Index

## 📁 Root Directory Structure

```
training-management-system/
├── 📄 CODEBASE_ANALYSIS_SUMMARY.md (7.4KB) - Previous analysis summary
├── 📄 CODEBASE_INDEX_COMPREHENSIVE.md (20KB) - Comprehensive codebase analysis
├── 📄 FILE_INDEX_DETAILED.md (This file) - Detailed file index
├── 📄 CODEBASE_INDEX_ANALYZED.md (20KB) - Analyzed codebase index
├── 📄 VERTICAL_BAR_CHART_ANALYSIS.md (13KB) - Chart analysis documentation
├── 📄 CODEBASE_INDEX_UPDATED.md (17KB) - Updated codebase index
├── 📄 DYNAMIC_COLUMN_ANALYSIS.md (6.0KB) - Dynamic column analysis
├── 📄 PRE_ASSESSMENT_BAR_CHART_ANALYSIS.md (7.5KB) - Pre-assessment analysis
├── 📄 CODEBASE_INDEX_COMPLETE.md (20KB) - Complete codebase index
├── 📄 CODEBASE_INDEX.md (18KB) - Basic codebase index
├── 📄 CIRO I Feedback Form(1-50).xlsx (23KB) - Feedback form data
├── 📄 codeviz_report_*.md (28KB each) - Code visualization reports
├── 📄 tsconfig.json (756B) - TypeScript configuration
├── 📄 .gitignore (14B) - Git ignore rules
├── 📄 package-lock.json (684KB) - Node.js dependency lock
├── 📄 package.json (513B) - Frontend dependencies
├── 📄 requirements.txt (1.5KB) - Python dependencies
├── 📄 mor 01022025.XLSX (1.1MB) - Monthly Operating Report data
├── 📄 106122029.pdf (149KB) - PDF document
├── 📄 Copy of training_data(1).xlsx (12KB) - Training data
├── 📄 another training data.xlsx (9.8KB) - Additional training data
├── 📄 Tata_Motors_logo.png (1.1MB) - Company logo
├── 📁 training_mgmt/ - Django project root
├── 📁 src/ - React/TypeScript frontend
├── 📁 onedrive_data/ - OneDrive sync data
├── 📁 media/ - Uploaded media files
└── 📁 dashboard/ - Additional dashboard files
```

---

## 🐍 Django Backend Structure

### 📁 training_mgmt/ (Django Project Root)
```
training_mgmt/
├── 📄 db.sqlite3 (1.8GB) - Main database file
├── 📄 backup_restore.py (6.7KB) - Database backup/restore utilities
├── 📄 manage.py (691B) - Django management script
├── 📁 training_mgmt/ - Django settings & configuration
├── 📁 dashboard/ - Main Django application
├── 📁 media/ - Uploaded files storage
├── 📁 staticfiles/ - Collected static files
├── 📁 static/ - Static files source
└── 📁 local_storage/ - Local file storage
```

### 📁 training_mgmt/training_mgmt/ (Django Settings)
```
training_mgmt/training_mgmt/
├── 📄 __init__.py (0B) - Python package marker
├── 📄 urls.py (1.2KB) - Main URL configuration
├── 📄 settings.py (5.4KB) - Django settings configuration
├── 📄 wsgi.py (419B) - WSGI application entry point
├── 📄 asgi.py (419B) - ASGI application entry point
└── 📁 dashboard/ - Additional dashboard configuration
```

### 📁 training_mgmt/dashboard/ (Main Django App)
```
training_mgmt/dashboard/
├── 📄 __init__.py (6B) - Python package marker
├── 📄 apps.py (156B) - Django app configuration
├── 📄 models.py (23KB) - Database models (557 lines)
├── 📄 views.py (190KB) - Main views file (4,328 lines) ⚠️ NEEDS REFACTORING
├── 📄 views_original.py (6.9KB) - Original views backup
├── 📄 analysis_view.py (22KB) - Analysis views (405 lines)
├── 📄 assessment_views.py (5.7KB) - Assessment views (138 lines)
├── 📄 idi_views.py (7.4KB) - IDI analysis views (174 lines)
├── 📄 urls.py (8.1KB) - URL patterns (101 lines)
├── 📄 admin.py (6.5KB) - Django admin configuration (142 lines)
├── 📄 forms.py (866B) - Form definitions (26 lines)
├── 📄 serializers.py (1.0KB) - API serializers (19 lines)
├── 📄 tests.py (2.5KB) - Basic tests (49 lines)
├── 📄 assessment_models.py (5.2KB) - Assessment models (109 lines)
├── 📁 views/ - Additional view modules
├── 📁 migrations/ - Database migrations
├── 📁 templates/ - HTML templates
├── 📁 static/ - Static files
└── 📁 management/ - Custom management commands
```

### 📁 training_mgmt/dashboard/views/ (View Modules)
```
training_mgmt/dashboard/views/
├── 📄 __init__.py - Package marker
└── [Additional view modules - needs exploration]
```

### 📁 training_mgmt/dashboard/migrations/ (Database Migrations)
```
training_mgmt/dashboard/migrations/
├── 📄 __init__.py - Package marker
└── [Migration files - needs exploration]
```

### 📁 training_mgmt/dashboard/templates/ (HTML Templates)
```
training_mgmt/dashboard/templates/
├── [HTML template files - needs exploration]
└── [Template directories - needs exploration]
```

### 📁 training_mgmt/dashboard/static/ (Static Files)
```
training_mgmt/dashboard/static/
├── [CSS, JS, image files - needs exploration]
└── [Static file directories - needs exploration]
```

### 📁 training_mgmt/dashboard/management/ (Management Commands)
```
training_mgmt/dashboard/management/
├── [Custom Django management commands - needs exploration]
└── [Command directories - needs exploration]
```

---

## ⚛️ React/TypeScript Frontend Structure

### 📁 src/ (Frontend Source)
```
src/
├── 📁 components/ - React components
├── 📁 hooks/ - Custom React hooks
├── 📁 filters/ - Filter utilities
└── 📁 types/ - TypeScript type definitions
```

### 📁 src/components/ (React Components)
```
src/components/
├── 📄 FilterBar.tsx (1.2KB) - Filter bar component (40 lines)
├── 📄 FilterModal.tsx (3.2KB) - Filter modal component (91 lines)
└── 📄 mountFilterBar.tsx (3.0KB) - Filter bar mounting utility (75 lines)
```

### 📁 src/hooks/ (Custom React Hooks)
```
src/hooks/
├── [Custom React hooks - needs exploration]
└── [Hook files - needs exploration]
```

### 📁 src/filters/ (Filter Utilities)
```
src/filters/
├── [Filter utility functions - needs exploration]
└── [Filter helper files - needs exploration]
```

### 📁 src/types/ (TypeScript Types)
```
src/types/
└── 📄 filters.ts (763B) - Filter type definitions (30 lines)
```

---

## 📊 Configuration Files

### Backend Configuration
```
📄 requirements.txt (1.5KB) - Python dependencies (50 lines)
├── Django>=4.2.0,<5.0.0
├── django-crispy-forms>=2.0
├── crispy-bootstrap5>=0.7
├── Pillow>=10.0.0
├── python-dateutil>=2.8.2
├── django-filter>=23.0
├── djangorestframework>=3.14.0
├── django-cors-headers>=4.0.0
├── whitenoise>=6.5.0
├── gunicorn>=21.2.0
├── psycopg2-binary>=2.9.6
├── python-dotenv>=1.0.0
├── django-storages>=1.14.0
├── boto3>=1.28.0
├── django-cleanup>=8.0.0
├── django-widget-tweaks>=1.5.0
├── django-tables2>=2.6.0
├── django-bootstrap5>=23.0
├── django-bootstrap-datepicker-plus>=5.0.0
├── django-bootstrap-modal-forms>=2.2.0
├── django-ajax-selects>=1.9.0
├── django-select2>=8.1.0
├── django-autocomplete-light>=3.9.0
├── django-bootstrap-datetimepicker>=1.0.0
├── django-bootstrap4>=22.3
├── django-bootstrap-datepicker>=1.0.0
├── django-bootstrap-timepicker>=0.1.0
├── django-bootstrap-daterangepicker>=0.1.0
├── django-bootstrap-select>=0.1.0
├── django-bootstrap-tagsinput>=0.1.0
├── django-bootstrap-typeahead>=0.1.0
├── django-bootstrap-upload>=0.1.0
├── django-bootstrap-validator>=0.1.0
├── django-bootstrap-vue>=0.1.0
├── django-bootstrap-wysiwyg>=0.1.0
├── django-bootstrap3>=23.0
├── django-bootstrap4-datetimepicker>=0.1.0
├── django-bootstrap4-tagsinput>=0.1.0
├── django-bootstrap4-typeahead>=0.1.0
├── django-bootstrap4-upload>=0.1.0
├── django-bootstrap4-validator>=0.1.0
├── django-bootstrap4-vue>=0.1.0
├── django-bootstrap4-wysiwyg>=0.1.0
├── django-bootstrap5-datetimepicker>=0.1.0
├── django-bootstrap5-tagsinput>=0.1.0
├── django-bootstrap5-typeahead>=0.1.0
├── django-bootstrap5-upload>=0.1.0
├── django-bootstrap5-validator>=0.1.0
├── django-bootstrap5-vue>=0.1.0
└── allpairspy>=2.5.0
```

### Frontend Configuration
```
📄 package.json (513B) - Node.js dependencies (21 lines)
├── name: "training-management-system"
├── version: "1.0.0"
├── description: "Training Management System Frontend"
├── scripts:
│   ├── build: "tsc"
│   ├── start: "react-scripts start"
│   ├── test: "react-scripts test"
│   └── eject: "react-scripts eject"
├── dependencies:
│   ├── react: "^18.2.0"
│   └── react-dom: "^18.2.0"
└── devDependencies:
    ├── @types/react: "^18.2.0"
    ├── @types/react-dom: "^18.2.0"
    ├── typescript: "^4.9.0"
    └── react-scripts: "5.0.1"

📄 tsconfig.json (756B) - TypeScript configuration (28 lines)
├── target: "es5"
├── lib: ["dom", "dom.iterable", "esnext"]
├── allowJs: true
├── skipLibCheck: true
├── esModuleInterop: true
├── allowSyntheticDefaultImports: true
├── strict: true
├── forceConsistentCasingInFileNames: true
├── noFallthroughCasesInSwitch: true
├── module: "esnext"
├── moduleResolution: "node"
├── resolveJsonModule: true
├── isolatedModules: true
├── noEmit: true
├── jsx: "react-jsx"
├── baseUrl: "."
├── paths: { "*": ["node_modules/*", "src/*"] }
├── typeRoots: ["./node_modules/@types"]
├── outDir: "./dist"
├── rootDir: "./src"
├── include: ["src/**/*"]
└── exclude: ["node_modules", "build", "dist"]
```

---

## 📁 Data Files

### Excel Data Files
```
📄 CIRO I Feedback Form(1-50).xlsx (23KB) - Feedback form data (89 lines)
📄 mor 01022025.XLSX (1.1MB) - Monthly Operating Report data
📄 Copy of training_data(1).xlsx (12KB) - Training data (55 lines)
📄 another training data.xlsx (9.8KB) - Additional training data (24 lines)
```

### Document Files
```
📄 106122029.pdf (149KB) - PDF document (1,144 lines)
📄 Tata_Motors_logo.png (1.1MB) - Company logo
```

---

## 📁 Additional Directories

### 📁 onedrive_data/ (OneDrive Sync)
```
onedrive_data/
├── [OneDrive synchronized files - needs exploration]
└── [Sync data - needs exploration]
```

### 📁 media/ (Uploaded Media)
```
media/
├── [Uploaded media files - needs exploration]
└── [User-uploaded content - needs exploration]
```

### 📁 dashboard/ (Additional Dashboard)
```
dashboard/
├── 📄 views.py (491B) - Additional views (7 lines)
└── 📁 templates/ - Additional templates
```

---

## 🔍 File Analysis Summary

### Critical Files (High Priority)
1. **📄 training_mgmt/dashboard/views.py (190KB, 4,328 lines)** ⚠️
   - **Status**: Needs immediate refactoring
   - **Purpose**: Main application logic
   - **Issue**: Too large, difficult to maintain

2. **📄 training_mgmt/dashboard/models.py (23KB, 557 lines)**
   - **Status**: Well-structured
   - **Purpose**: Database schema definition
   - **Assessment**: Good organization, comprehensive models

3. **📄 training_mgmt/db.sqlite3 (1.8GB)**
   - **Status**: Production database
   - **Purpose**: Data storage
   - **Note**: Substantial real-world usage

### Important Configuration Files
1. **📄 training_mgmt/training_mgmt/settings.py (5.4KB)**
   - **Purpose**: Django configuration
   - **Status**: Well-configured with environment variables

2. **📄 training_mgmt/dashboard/urls.py (8.1KB, 101 lines)**
   - **Purpose**: URL routing
   - **Status**: Comprehensive API and view routing

3. **📄 requirements.txt (1.5KB, 50 lines)**
   - **Purpose**: Python dependencies
   - **Status**: Extensive Django ecosystem usage

### Frontend Files
1. **📄 src/components/FilterBar.tsx (1.2KB, 40 lines)**
   - **Purpose**: Filter interface component
   - **Status**: Well-structured TypeScript component

2. **📄 src/types/filters.ts (763B, 30 lines)**
   - **Purpose**: TypeScript type definitions
   - **Status**: Good type safety implementation

### Documentation Files
1. **📄 CODEBASE_ANALYSIS_SUMMARY.md (7.4KB, 181 lines)**
   - **Purpose**: Previous analysis summary
   - **Status**: Comprehensive overview

2. **📄 CODEBASE_INDEX_COMPREHENSIVE.md (20KB, 523 lines)**
   - **Purpose**: Detailed codebase analysis
   - **Status**: Most comprehensive analysis

---

## 🚨 Files Requiring Attention

### 🔴 High Priority
1. **views.py** - Needs refactoring into smaller modules
2. **Database** - Consider performance optimization for 1.8GB size

### 🟡 Medium Priority
1. **Documentation** - Multiple analysis files need consolidation
2. **Frontend** - Limited React components, could be expanded
3. **Testing** - No visible test files in main structure

### 🟢 Low Priority
1. **Static files** - Need exploration and organization
2. **Templates** - Need exploration and documentation
3. **Management commands** - Need exploration

---

## 📋 Next Steps for File Exploration

### Immediate Actions
1. **Explore views/ directory** - Check for existing view modules
2. **Explore migrations/ directory** - Understand database evolution
3. **Explore templates/ directory** - Document template structure
4. **Explore static/ directory** - Document static assets

### Medium-term Actions
1. **Refactor views.py** - Break into smaller modules
2. **Add test files** - Create comprehensive test suite
3. **Consolidate documentation** - Merge analysis files

### Long-term Actions
1. **Performance optimization** - Database and query optimization
2. **Frontend expansion** - Add more React components
3. **Architecture improvements** - Consider microservices

---

*Last Updated: December 2024*
*Total Files Indexed: 50+*
*Critical Files Identified: 3*
*Files Needing Attention: 5* 