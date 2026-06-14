"""
Run this ONCE after migrations to set up demo data:
  python setup_data.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'garbage_mgmt.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import UserProfile, Complaint

print("Creating demo users...")

# Admin
admin, created = User.objects.get_or_create(username='admin')
admin.set_password('admin123')
admin.first_name = 'Admin'
admin.last_name = 'Officer'
admin.is_staff = True
admin.save()
UserProfile.objects.get_or_create(user=admin, defaults={'role': 'admin', 'phone': '9000000000'})

# Residents
residents = [
    ('ravi', 'ravi123', 'Ravi', 'Kumar', '9111111111'),
    ('priya', 'priya123', 'Priya', 'Sharma', '9222222222'),
    ('john', 'john123', 'John', 'Peter', '9333333333'),
]

users = []
for uname, pwd, fn, ln, ph in residents:
    u, _ = User.objects.get_or_create(username=uname)
    u.set_password(pwd)
    u.first_name = fn
    u.last_name = ln
    u.save()
    UserProfile.objects.get_or_create(user=u, defaults={'role': 'user', 'phone': ph})
    users.append(u)
    print(f"  ✅ User: {uname} / {pwd}")

print("\nCreating sample complaints...")

sample = [
    (users[0], "12, Gandhi Nagar, Chennai", "Near Post Office", "Garbage overflowing near the main gate for 2 days", "Completed"),
    (users[1], "45, Anna Street, Coimbatore", "Opposite Bus Stop", "Waste not collected for 3 days, flies everywhere", "In Progress"),
    (users[2], "78, MG Road, Tiruppur", "Behind Government School", "Open dumping of construction debris on road", "Pending"),
    (users[0], "5, Nehru Colony, Salem", "Near Water Tank", "Foul smell from uncollected garbage heap", "Pending"),
    (users[1], "90, Park Road, Madurai", "Next to Park Gate", "Overflowing bin causing road blockage", "In Progress"),
]

for u, addr, lm, desc, status in sample:
    c = Complaint.objects.create(user=u, address=addr, landmark=lm, description=desc, status=status)
    print(f"  ✅ Complaint #{c.id}: {status}")

print("\n🎉 Setup complete!")
print("\n📋 Login Credentials:")
print("  🛡️  Admin  : admin / admin123")
print("  👤 User 1 : ravi / ravi123")
print("  👤 User 2 : priya / priya123")
print("  👤 User 3 : john / john123")
print("\nRun: python manage.py runserver")
