import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth.models import User

try:
    admin_user = User.objects.get(username='admin')
    admin_user.set_password('password123')
    admin_user.save()
    print("✅ Password successfully reset!")
    print("\n=== Credentials ===")
    print("Username: admin")
    print("Password: password123")
    print("==================\n")
except User.DoesNotExist:
    print("Creating admin user...")
    User.objects.create_superuser('admin', 'admin@example.com', 'password123')
    print("✅ Admin user created successfully!")
    print("\n=== Credentials ===")
    print("Username: admin")
    print("Password: password123")
    print("==================\n")
