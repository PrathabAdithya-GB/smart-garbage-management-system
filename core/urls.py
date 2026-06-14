from django.urls import path
from . import views

urlpatterns = [
    path('',                        views.dashboard,          name='dashboard'),
    path('login/',                  views.login_view,         name='login'),
    path('register/',               views.register_view,      name='register'),
    path('logout/',                 views.logout_view,        name='logout'),

    # Admin
    path('admin-dashboard/',        views.admin_dashboard,    name='admin_dashboard'),
    path('manage-complaints/',      views.manage_complaints,  name='manage_complaints'),
    path('complaint/<int:pk>/update/', views.update_complaint, name='update_complaint'),

    # User
    path('user-dashboard/',         views.user_dashboard,     name='user_dashboard'),
    path('report-complaint/',       views.report_complaint,   name='report_complaint'),
    path('track-complaints/',       views.track_complaints,   name='track_complaints'),
    path('complaint/<int:pk>/',     views.complaint_detail,   name='complaint_detail'),
]
