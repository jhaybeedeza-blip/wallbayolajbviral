#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sitenijb.settings')
django.setup()

from django.contrib.auth.models import User

# Check if user already exists
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@floraproject.com', 'admin123')
    print("✅ Superuser created successfully!")
    print("Username: admin")
    print("Password: admin123")
    print("Email: admin@floraproject.com")
    print("\nYou can now log in to the admin panel at: http://localhost:8000/admin/")
else:
    print("⚠️ Admin user already exists!")
    print("Username: admin")
