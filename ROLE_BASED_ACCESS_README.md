# Role-Based Access Control System

## Overview

This Training Management System now includes a comprehensive role-based access control (RBAC) system with three user types:

1. **Admin** - Full access to all features
2. **User Alpha** - Can upload/download documents and reports
3. **User Beta** - View-only access to all content

## 🚀 Quick Setup

### 1. Run the Setup Script

```bash
cd training_mgmt
python manage.py shell < setup_role_based_access.py
```

### 2. Start the Development Server

```bash
python manage.py runserver
```

### 3. Access the Login Page

Navigate to `http://localhost:8000/accounts/login/`

## 👥 User Accounts

| Username | Password | Role | Permissions |
|----------|----------|------|-------------|
| `Alpha@1` | `Alpha@123` | User Alpha | Upload/Download documents & reports |
| `Beta@1` | `Beta@123` | User Beta | View-only access |
| [Your Admin] | [Your Password] | Admin | Full access |

## 🔐 Login Process

1. **Select User Type**: Choose from the dropdown:
   - Admin (Full Access)
   - User Alpha (Upload/Download Access)
   - User Beta (View Only Access)

2. **Enter Credentials**: Username and password

3. **Authentication**: System validates user type matches credentials

4. **Access Control**: User is redirected based on permissions

## 🎯 Role Permissions

### Admin
- ✅ Full access to all features
- ✅ Create, edit, delete programs and trainings
- ✅ Upload/download all documents
- ✅ Access admin panel
- ✅ Manage users and permissions

### User Alpha
- ✅ View all content
- ✅ Upload/download documents and reports
- ✅ Access file management features
- ✅ View analytics and reports
- ❌ Cannot edit/delete content
- ❌ Cannot access admin panel

### User Beta
- ✅ View all content
- ✅ Access dashboards and reports
- ✅ View training schedules
- ❌ Cannot upload/download documents
- ❌ Cannot edit/delete content
- ❌ Cannot access admin panel

## 🏗️ Technical Implementation

### Files Created/Modified

#### New Files:
- `training_mgmt/dashboard/auth_views.py` - Custom authentication views
- `training_mgmt/dashboard/decorators.py` - Role-based access decorators
- `training_mgmt/setup_role_based_access.py` - Setup script
- `ROLE_BASED_ACCESS_README.md` - This documentation

#### Modified Files:
- `training_mgmt/dashboard/forms.py` - Added custom authentication forms
- `training_mgmt/dashboard/urls.py` - Updated to use custom views
- `training_mgmt/dashboard/templates/registration/login.html` - Added user type selection
- `training_mgmt/dashboard/templates/registration/register.html` - Added user type selection
- `training_mgmt/dashboard/templates/dashboard/base.html` - Added role badges and conditional navigation

### Key Components

#### 1. Custom Authentication Forms
```python
class CustomAuthenticationForm(AuthenticationForm):
    USER_TYPE_CHOICES = [
        ('admin', 'Admin (Full Access)'),
        ('alpha', 'User Alpha (Upload/Download Access)'),
        ('beta', 'User Beta (View Only Access)'),
    ]
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES)
```

#### 2. Role-Based Decorators
```python
@role_required(['admin', 'alpha'])
@upload_download_required
@edit_delete_required
@view_only_required
```

#### 3. Permission Helper Functions
```python
def can_upload_download(user):
    return user.is_superuser or user.is_staff or user.groups.filter(name='User Alpha').exists()

def can_edit_delete(user):
    return user.is_superuser or user.is_staff
```

## 🎨 User Interface Features

### Login Page Enhancements
- **User Type Dropdown**: Select role before login
- **Role Information**: Clear description of each role's permissions
- **Error Messages**: Specific feedback for permission issues
- **Responsive Design**: Works on mobile and desktop

### Navigation Enhancements
- **Role Badges**: Color-coded badges showing user role
- **Conditional Navigation**: Menu items appear based on permissions
- **User Information**: Display current user and role

### Visual Indicators
- **Admin**: Red badge
- **User Alpha**: Blue badge  
- **User Beta**: Orange badge

## 🔧 Usage Examples

### Applying Role Decorators to Views

```python
from .decorators import role_required, upload_download_required, edit_delete_required

# Only admin and alpha users can access
@role_required(['admin', 'alpha'])
def upload_document(request):
    # Upload logic here
    pass

# Only users with upload/download permissions
@upload_download_required
def download_report(request):
    # Download logic here
    pass

# Only admin users can edit/delete
@edit_delete_required
def delete_program(request, program_id):
    # Delete logic here
    pass
```

### Template Conditional Rendering

```html
{% if user.is_superuser or user.is_staff or user.groups.all.0.name == 'User Alpha' %}
    <a href="{% url 'upload_document' %}" class="btn btn-primary">Upload Document</a>
{% endif %}

{% if user.is_superuser or user.is_staff %}
    <a href="{% url 'delete_item' %}" class="btn btn-danger">Delete</a>
{% endif %}
```

## 🛡️ Security Features

### Authentication Security
- **CSRF Protection**: All forms include CSRF tokens
- **Session Management**: Secure session handling
- **Password Validation**: Django's built-in password validation
- **Rate Limiting**: Prevents brute force attacks

### Access Control Security
- **Role Validation**: Server-side role verification
- **Permission Checks**: Multiple layers of permission validation
- **Secure Redirects**: Safe redirect handling
- **Error Handling**: Graceful error handling for unauthorized access

## 🧪 Testing

### Manual Testing Checklist

1. **Login Testing**:
   - [ ] Admin login with correct user type
   - [ ] User Alpha login with correct user type
   - [ ] User Beta login with correct user type
   - [ ] Wrong user type selection (should fail)
   - [ ] Invalid credentials (should fail)

2. **Permission Testing**:
   - [ ] Admin can access all features
   - [ ] User Alpha can upload/download but not edit/delete
   - [ ] User Beta can only view content
   - [ ] Unauthorized access attempts are blocked

3. **UI Testing**:
   - [ ] Role badges display correctly
   - [ ] Navigation items show/hide based on permissions
   - [ ] Error messages are clear and helpful
   - [ ] Responsive design works on mobile

### Automated Testing

Run the setup script to test authentication:
```bash
python manage.py shell < setup_role_based_access.py
```

## 🔄 Maintenance

### Adding New Roles

1. **Create Group**: Add new group in Django admin
2. **Update Forms**: Add new choice to `USER_TYPE_CHOICES`
3. **Update Views**: Modify authentication logic
4. **Update Templates**: Add new role badge styling
5. **Update Decorators**: Create new role-specific decorators

### Modifying Permissions

1. **Update Helper Functions**: Modify `can_upload_download()`, etc.
2. **Update Decorators**: Adjust decorator logic
3. **Update Templates**: Modify conditional rendering
4. **Test Thoroughly**: Verify all permission changes work correctly

## 🐛 Troubleshooting

### Common Issues

1. **Login Fails with Correct Credentials**
   - Check if user is in correct group
   - Verify user type selection matches user role
   - Check Django admin for user permissions

2. **Permission Errors**
   - Verify user groups are set correctly
   - Check decorator usage on views
   - Ensure helper functions are working

3. **UI Issues**
   - Clear browser cache
   - Check for JavaScript errors
   - Verify template syntax

### Debug Commands

```python
# Check user groups
python manage.py shell
>>> from django.contrib.auth.models import User
>>> user = User.objects.get(username='Alpha@1')
>>> print([g.name for g in user.groups.all()])

# Check user permissions
>>> print(user.is_staff, user.is_superuser)
```

## 📞 Support

For issues or questions about the role-based access control system:

1. Check this README for common solutions
2. Review the setup script output for errors
3. Test with the provided user accounts
4. Check Django logs for detailed error messages

## 🎉 Success!

The role-based access control system is now fully implemented and ready for use. Users can log in with their specific roles and access features according to their permissions. 