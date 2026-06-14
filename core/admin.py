from django.contrib import admin
from .models import UserProfile, Complaint

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'phone']
    list_filter = ['role']

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'address', 'status', 'created_at']
    list_filter = ['status']
    search_fields = ['user__username', 'address', 'description']
