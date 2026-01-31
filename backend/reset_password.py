from django.contrib.auth.models import User

# Reset admin password
try:
    admin_user = User.objects.get(username='admin')
    admin_user.set_password('password123')
    admin_user.save()
    print("✅ Password reset successfully for 'admin' user")
    print("Username: admin")
    print("Password: password123")
except User.DoesNotExist:
    print("❌ Admin user not found. Creating new admin user...")
    User.objects.create_superuser('admin', 'admin@example.com', 'password123')
    print("✅ Admin user created successfully")
    print("Username: admin")
    print("Password: password123")
