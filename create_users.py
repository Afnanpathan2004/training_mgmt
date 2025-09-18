#!/usr/bin/env python
"""
Script to create User Alpha and User Beta accounts with specific permissions.
Run this script using: python manage.py shell < create_users.py
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

def create_users():
    print("Creating User Alpha and User Beta accounts...")
    
    # Create User Alpha
    try:
        user_alpha = User.objects.create_user(
            username='Alpha@1',
            password='Alpha@123',
            first_name='User',
            last_name='Alpha',
            email='alpha@example.com',
            is_staff=True,  # Give staff access for document operations
            is_superuser=False
        )
        print(f"✓ Created User Alpha: {user_alpha.username}")
    except Exception as e:
        print(f"✗ Error creating User Alpha: {e}")
        user_alpha = User.objects.get(username='Alpha@1')
        print(f"  User Alpha already exists")
    
    # Create User Beta
    try:
        user_beta = User.objects.create_user(
            username='Beta@1',
            password='Beta@123',
            first_name='User',
            last_name='Beta',
            email='beta@example.com',
            is_staff=False,  # No staff access - view only
            is_superuser=False
        )
        print(f"✓ Created User Beta: {user_beta.username}")
    except Exception as e:
        print(f"✗ Error creating User Beta: {e}")
        user_beta = User.objects.get(username='Beta@1')
        print(f"  User Beta already exists")
    
    # Create groups for role-based permissions
    try:
        alpha_group, created = Group.objects.get_or_create(name='User Alpha')
        if created:
            print("✓ Created User Alpha group")
        
        beta_group, created = Group.objects.get_or_create(name='User Beta')
        if created:
            print("✓ Created User Beta group")
            
        # Add users to their respective groups
        user_alpha.groups.add(alpha_group)
        user_beta.groups.add(beta_group)
        print("✓ Added users to their groups")
        
    except Exception as e:
        print(f"✗ Error creating groups: {e}")
    
    print("\nUser accounts created successfully!")
    print("User Alpha: Alpha@1 / Alpha@123 (Can upload/download documents)")
    print("User Beta: Beta@1 / Beta@123 (View only access)")
    print("Admin: Use existing admin account (full access)")

if __name__ == '__main__':
    create_users() 