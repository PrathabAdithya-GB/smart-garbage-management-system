# Smart Garbage Management System
### Built with Django + HTML + CSS + JavaScript

---

## Modules Included
1. **Authentication Module** – Login & Registration for Admin and Residents
2. **Admin Dashboard Module** – Stats overview, recent complaints, area reports
3. **Complaint Reporting Module** – Residents submit garbage complaints with photo
4. **Complaint Management Module** – Admin views & filters all complaints
5. **Complaint Status Update Module** – Admin updates Pending → In Progress → Completed
6. **Complaint Tracking Module** – Residents view their own complaint statuses
7. **Database Management Module** – SQLite via Django ORM
8. **Logout / Session Management Module** – Secure logout for all users

---

## Setup Instructions

### 1. Install Python & Django
```bash
pip install django pillow
```

### 2. Navigate to project folder
```bash
cd garbage_mgmt
```

### 3. Run database migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Load demo data (users + sample complaints)
```bash
python setup_data.py
```

### 5. Start the server
```bash
python manage.py runserver
```

### 6. Open in browser
```
http://127.0.0.1:8000/
```

---

## Demo Login Credentials

| Role    | Username | Password  |
|---------|----------|-----------|
| Admin  | admin    | admin123  |
| User 1 | ravi     | ravi123   |
| User 2 | priya    | priya123  |
| User 3 | john     | john123   |

---

## Project Structure

```
garbage_mgmt/
├── manage.py
├── setup_data.py          ← Run once to seed demo data
├── db.sqlite3             ← Auto-created after migrate
├── media/                 ← Uploaded complaint images
│   └── complaints/
├── garbage_mgmt/          ← Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── core/                  ← Main app
    ├── models.py          ← UserProfile, Complaint
    ├── views.py           ← All 8 module views
    ├── urls.py            ← URL routes
    ├── admin.py           ← Django admin panel
    ├── templates/core/
    │   ├── base.html
    │   ├── login.html
    │   ├── register.html
    │   ├── admin_dashboard.html
    │   ├── manage_complaints.html
    │   ├── update_complaint.html
    │   ├── user_dashboard.html
    │   ├── report_complaint.html
    │   ├── track_complaints.html
    │   └── complaint_detail.html
    └── static/core/
        ├── css/style.css
        └── js/main.js
```

---

## URL Routes

| URL | View | Who |
|-----|------|-----|
| `/login/` | Login page | All |
| `/register/` | Register page | New users |
| `/logout/` | Logout | Logged in |
| `/admin-dashboard/` | Admin stats | Admin |
| `/manage-complaints/` | View all complaints | Admin |
| `/complaint/<id>/update/` | Update status | Admin |
| `/user-dashboard/` | User home | Resident |
| `/report-complaint/` | Submit complaint | Resident |
| `/track-complaints/` | View own complaints | Resident |
| `/complaint/<id>/` | Complaint detail | Both |

---

## Notes
- Images are stored in `/media/complaints/`
- Use `/admin/` for Django's built-in admin panel (superuser required)
- To create a superuser: `python manage.py createsuperuser`


## Author

G.B. Prathab Adithya

Bachelor of Science (Artificial Intelligence and Machine Learning)

Email: [your-innovatorsdesk05@gmail.com]

LinkedIn: https://www.linkedin.com/in/prathab-adithya-gb-student

---

## License

This project is developed for educational and academic purposes.
