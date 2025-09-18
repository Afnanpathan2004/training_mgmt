#!/usr/bin/env python
"""
Setup script for Role-Based Access Control System
This script will:
1. Create User Alpha and User Beta accounts
2. Set up user groups and permissions
3. Verify the setup

Run this script using: python manage.py shell < setup_role_based_access.py
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'training_mgmt.settings')
django.setup()

from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from dashboard.models import *

def setup_role_based_access():
    print("🚀 Setting up Role-Based Access Control System...")
    print("=" * 60)
    
    # Step 1: Create User Groups
    print("\n📋 Step 1: Creating User Groups...")
    
    try:
        alpha_group, created = Group.objects.get_or_create(name='User Alpha')
        if created:
            print("✓ Created 'User Alpha' group")
        else:
            print("✓ 'User Alpha' group already exists")
        
        beta_group, created = Group.objects.get_or_create(name='User Beta')
        if created:
            print("✓ Created 'User Beta' group")
        else:
            print("✓ 'User Beta' group already exists")
            
    except Exception as e:
        print(f"✗ Error creating groups: {e}")
        return False
    
    # Step 2: Create User Alpha
    print("\n👤 Step 2: Creating User Alpha...")
    
    try:
        # Check if User Alpha already exists
        if User.objects.filter(username='Alpha@1').exists():
            user_alpha = User.objects.get(username='Alpha@1')
            print("✓ User Alpha already exists, updating permissions...")
        else:
            user_alpha = User.objects.create_user(
                username='Alpha@1',
                password='Alpha@123',
                first_name='User',
                last_name='Alpha',
                email='alpha@example.com',
                is_staff=True,  # Give staff access for document operations
                is_superuser=False
            )
            print("✓ Created User Alpha: Alpha@1")
        
        # Add to User Alpha group
        user_alpha.groups.add(alpha_group)
        print("✓ Added User Alpha to 'User Alpha' group")
        
    except Exception as e:
        print(f"✗ Error creating User Alpha: {e}")
        return False
    
    # Step 3: Create User Beta
    print("\n👤 Step 3: Creating User Beta...")
    
    try:
        # Check if User Beta already exists
        if User.objects.filter(username='Beta@1').exists():
            user_beta = User.objects.get(username='Beta@1')
            print("✓ User Beta already exists, updating permissions...")
        else:
            user_beta = User.objects.create_user(
                username='Beta@1',
                password='Beta@123',
                first_name='User',
                last_name='Beta',
                email='beta@example.com',
                is_staff=False,  # No staff access - view only
                is_superuser=False
            )
            print("✓ Created User Beta: Beta@1")
        
        # Add to User Beta group
        user_beta.groups.add(beta_group)
        print("✓ Added User Beta to 'User Beta' group")
        
    except Exception as e:
        print(f"✗ Error creating User Beta: {e}")
        return False
    
    # Step 4: Verify Setup
    print("\n🔍 Step 4: Verifying Setup...")
    
    try:
        # Verify User Alpha
        alpha_user = User.objects.get(username='Alpha@1')
        alpha_in_group = alpha_user.groups.filter(name='User Alpha').exists()
        print(f"✓ User Alpha verification: {'PASS' if alpha_in_group else 'FAIL'}")
        
        # Verify User Beta
        beta_user = User.objects.get(username='Beta@1')
        beta_in_group = beta_user.groups.filter(name='User Beta').exists()
        print(f"✓ User Beta verification: {'PASS' if beta_in_group else 'FAIL'}")
        
        # Verify groups exist
        alpha_group_exists = Group.objects.filter(name='User Alpha').exists()
        beta_group_exists = Group.objects.filter(name='User Beta').exists()
        print(f"✓ Groups verification: {'PASS' if alpha_group_exists and beta_group_exists else 'FAIL'}")
        
    except Exception as e:
        print(f"✗ Error during verification: {e}")
        return False
    
    # Step 5: Display Summary
    print("\n📊 Step 5: Setup Summary...")
    print("=" * 60)
    print("🎯 Role-Based Access Control Setup Complete!")
    print("\n📋 User Accounts Created:")
    print("┌─────────────────┬─────────────────┬─────────────────┬─────────────────┐")
    print("│ Username        │ Password        │ Role            │ Permissions     │")
    print("├─────────────────┼─────────────────┼─────────────────┼─────────────────┤")
    print("│ Alpha@1         │ Alpha@123       │ User Alpha      │ Upload/Download │")
    print("│ Beta@1          │ Beta@123        │ User Beta       │ View Only       │")
    print("│ [Admin User]    │ [Your Password] │ Admin           │ Full Access     │")
    print("└─────────────────┴─────────────────┴─────────────────┴─────────────────┘")
    
    print("\n🔐 Login Instructions:")
    print("1. Go to /accounts/login/")
    print("2. Select your user type from the dropdown")
    print("3. Enter your username and password")
    print("4. Click 'Login'")
    
    print("\n🎨 Features Added:")
    print("✓ User type selection dropdown in login form")
    print("✓ Role-based access control")
    print("✓ User role badges in navigation")
    print("✓ Conditional navigation based on permissions")
    print("✓ Custom authentication views")
    print("✓ Permission decorators for views")
    
    print("\n🚀 Next Steps:")
    print("1. Test login with each user type")
    print("2. Verify permissions work correctly")
    print("3. Apply role decorators to specific views as needed")
    
    return True

def test_authentication():
    """Test the authentication system"""
    print("\n🧪 Testing Authentication System...")
    
    from django.contrib.auth import authenticate
    
    # Test User Alpha
    alpha_user = authenticate(username='Alpha@1', password='Alpha@123')
    if alpha_user:
        print("✓ User Alpha authentication: PASS")
        print(f"  - Staff access: {alpha_user.is_staff}")
        print(f"  - Groups: {[g.name for g in alpha_user.groups.all()]}")
    else:
        print("✗ User Alpha authentication: FAIL")
    
    # Test User Beta
    beta_user = authenticate(username='Beta@1', password='Beta@123')
    if beta_user:
        print("✓ User Beta authentication: PASS")
        print(f"  - Staff access: {beta_user.is_staff}")
        print(f"  - Groups: {[g.name for g in beta_user.groups.all()]}")
    else:
        print("✗ User Beta authentication: FAIL")

if __name__ == '__main__':
    success = setup_role_based_access()
    if success:
        test_authentication()
        print("\n✅ Setup completed successfully!")
    else:
        print("\n❌ Setup failed. Please check the errors above.") 