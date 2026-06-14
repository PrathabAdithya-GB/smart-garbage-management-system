from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Count, Q
from .models import Complaint, UserProfile


# ─── 1. AUTHENTICATION MODULE ───────────────────────────────────────────────

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f'Welcome back, {user.get_full_name() or user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'core/login.html')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name  = request.POST.get('last_name', '').strip()
        username   = request.POST.get('username', '').strip()
        password   = request.POST.get('password', '')
        confirm    = request.POST.get('confirm_password', '')
        phone      = request.POST.get('phone', '').strip()

        if password != confirm:
            messages.error(request, 'Passwords do not match.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
        else:
            user = User.objects.create_user(
                username=username, password=password,
                first_name=first_name, last_name=last_name
            )
            UserProfile.objects.create(user=user, role='user', phone=phone)
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('dashboard')
    return render(request, 'core/register.html')


# ─── 8. LOGOUT / SESSION MANAGEMENT MODULE ──────────────────────────────────

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out securely.')
    return redirect('login')


# ─── DASHBOARD ROUTER ────────────────────────────────────────────────────────

@login_required
def dashboard(request):
    try:
        profile = request.user.profile
        if profile.is_admin():
            return redirect('admin_dashboard')
    except UserProfile.DoesNotExist:
        pass
    return redirect('user_dashboard')


# ─── 2. ADMIN DASHBOARD MODULE ───────────────────────────────────────────────

@login_required
def admin_dashboard(request):
    if not _is_admin(request.user):
        return redirect('user_dashboard')

    complaints = Complaint.objects.select_related('user').all()
    total      = complaints.count()
    pending    = complaints.filter(status='Pending').count()
    inprogress = complaints.filter(status='In Progress').count()
    completed  = complaints.filter(status='Completed').count()

    # Recent 5 complaints
    recent = complaints[:5]

    # Area stats
    area_stats = (
        complaints.values('address')
        .annotate(count=Count('id'))
        .order_by('-count')[:5]
    )

    context = {
        'total': total, 'pending': pending,
        'inprogress': inprogress, 'completed': completed,
        'recent': recent, 'area_stats': area_stats,
        'user_count': User.objects.count(),
    }
    return render(request, 'core/admin_dashboard.html', context)


# ─── 4. COMPLAINT MANAGEMENT MODULE (Admin) ──────────────────────────────────

@login_required
def manage_complaints(request):
    if not _is_admin(request.user):
        return redirect('user_dashboard')

    complaints = Complaint.objects.select_related('user').all()

    # Filter
    status_filter = request.GET.get('status', '')
    search = request.GET.get('search', '')
    if status_filter:
        complaints = complaints.filter(status=status_filter)
    if search:
        complaints = complaints.filter(
            Q(user__first_name__icontains=search) |
            Q(user__last_name__icontains=search) |
            Q(address__icontains=search) |
            Q(description__icontains=search)
        )

    context = {
        'complaints': complaints,
        'status_filter': status_filter,
        'search': search,
        'status_choices': ['Pending', 'In Progress', 'Completed'],
    }
    return render(request, 'core/manage_complaints.html', context)


# ─── 5. COMPLAINT STATUS UPDATE MODULE ───────────────────────────────────────

@login_required
def update_complaint(request, pk):
    if not _is_admin(request.user):
        return redirect('user_dashboard')

    complaint = get_object_or_404(Complaint, pk=pk)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        remark = request.POST.get('admin_remark', '')
        if new_status in ['Pending', 'In Progress', 'Completed']:
            complaint.status = new_status
            complaint.admin_remark = remark
            complaint.save()
            messages.success(request, f'Complaint #{pk} updated to "{new_status}".')
        return redirect('manage_complaints')

    context = {
        'complaint': complaint,
        'status_choices': ['Pending', 'In Progress', 'Completed'],
    }
    return render(request, 'core/update_complaint.html', context)


# ─── 3. COMPLAINT REPORTING MODULE (User) ────────────────────────────────────

@login_required
def report_complaint(request):
    if _is_admin(request.user):
        return redirect('admin_dashboard')

    if request.method == 'POST':
        address     = request.POST.get('address', '').strip()
        landmark    = request.POST.get('landmark', '').strip()
        description = request.POST.get('description', '').strip()
        image       = request.FILES.get('image')

        if not address or not description:
            messages.error(request, 'Address and description are required.')
        else:
            Complaint.objects.create(
                user=request.user,
                address=address,
                landmark=landmark,
                description=description,
                image=image,
            )
            messages.success(request, 'Complaint submitted successfully! We will address it soon.')
            return redirect('track_complaints')

    return render(request, 'core/report_complaint.html')


# ─── 6 & 7. USER DASHBOARD + COMPLAINT TRACKING MODULE ───────────────────────

@login_required
def user_dashboard(request):
    if _is_admin(request.user):
        return redirect('admin_dashboard')

    complaints = Complaint.objects.filter(user=request.user)
    total      = complaints.count()
    pending    = complaints.filter(status='Pending').count()
    inprogress = complaints.filter(status='In Progress').count()
    completed  = complaints.filter(status='Completed').count()

    context = {
        'complaints': complaints[:5],
        'total': total, 'pending': pending,
        'inprogress': inprogress, 'completed': completed,
    }
    return render(request, 'core/user_dashboard.html', context)


@login_required
def track_complaints(request):
    if _is_admin(request.user):
        return redirect('admin_dashboard')

    complaints = Complaint.objects.filter(user=request.user)
    status_filter = request.GET.get('status', '')
    if status_filter:
        complaints = complaints.filter(status=status_filter)

    context = {
        'complaints': complaints,
        'status_filter': status_filter,
        'status_choices': ['Pending', 'In Progress', 'Completed'],
    }
    return render(request, 'core/track_complaints.html', context)


@login_required
def complaint_detail(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk)
    # Users can only see their own; admins can see all
    if not _is_admin(request.user) and complaint.user != request.user:
        messages.error(request, 'Access denied.')
        return redirect('track_complaints')
    return render(request, 'core/complaint_detail.html', {'complaint': complaint})


# ─── HELPER ──────────────────────────────────────────────────────────────────

def _is_admin(user):
    try:
        return user.profile.is_admin()
    except UserProfile.DoesNotExist:
        return False
