# Student Management API

A comprehensive Django REST Framework API for managing students, instructors, classes, and assignments in educational environments. This backend service provides secure authentication, role-based access control, and full CRUD operations for academic administration.

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![MySQL](https://img.shields.io/badge/mysql-%2300f.svg?style=for-the-badge&logo=mysql&logoColor=white)

## Features

### 🔐 Authentication & Authorization
- User registration with role selection (Student/Instructor)
- Secure login with session/token management
- Role-based access control
- User logout functionality
- Account deletion capability

### 📚 Class Management
- Create, read, update, and delete classes
- Assign instructors to classes
- Track class schedules (days and times)
- Monitor class statistics and metrics
- Support for multiple classes per instructor

### 👨‍🎓 Student Management
- Add students to classes
- Update student information
- Remove students from classes
- Query students by class
- Track student demographics (department, year level, sex)

### 📝 Assignment Management
- Create assignments with titles, instructions, and deadlines
- Update assignment details
- Delete assignments
- Query assignments by class
- Track assignment posting and submission dates

### 📊 Dashboard & Analytics
- Comprehensive dashboard statistics
- Total assignments count
- Total classes count
- Class schedules overview
- Assignment counts per class

## Tech Stack

- **Python 3.8+**: Core programming language
- **Django 4.x**: Web framework
- **MySQL**: Primary database (XAMPP compatible)
- **django-cors-headers**: CORS handling

## Database Schema

### Models

**User**
- UserID (Primary Key)
- Username
- Password (hashed)
- Role (Student/Instructor)
- Timestamps

**ClassInfo**
- ClassID (Primary Key)
- ClassName
- InstructorID (Foreign Key to User)
- ScheduleDays
- ScheduleTime
- Timestamps

**Student**
- StudentID (Primary Key)
- FirstName
- LastName
- Sex
- Department
- YearLevel
- ClassID (Foreign Key to ClassInfo)
- Timestamps

**Assignment**
- AssignmentID (Primary Key)
- ClassID (Foreign Key to ClassInfo)
- Title
- Instructions
- DatePosted
- DateOfSubmission
- Timestamps

## API Endpoints

### Authentication

| Method | Endpoint | Description | Request Body |
|--------|----------|-------------|--------------|
| POST | `/api/signup/` | Register new user | `{ "username": "string", "password": "string", "role": "Student/Instructor" }` |
| POST | `/api/login/` | Authenticate user | `{ "username": "string", "password": "string" }` |
| POST | `/api/logout/` | Logout current user | None |
| DELETE | `/api/delete_account/` | Delete user account | None |

### Classes

| Method | Endpoint | Description | Request Body |
|--------|----------|-------------|--------------|
| GET | `/api/classes/` | Get all classes | None |
| POST | `/api/add_class/` | Create new class | `{ "ClassName": "string", "InstructorID": int, "ScheduleDays": "string", "ScheduleTime": "string" }` |
| POST | `/api/classes/edit/<id>/` | Update class | `{ "ClassName": "string", "ScheduleDays": "string", "ScheduleTime": "string" }` |
| DELETE | `/api/classes/<id>/delete/` | Delete class | None |

### Students

| Method | Endpoint | Description | Request Body |
|--------|----------|-------------|--------------|
| GET | `/api/students/?class_id={id}` | Get students by class | None |
| POST | `/api/add_student/` | Add new student | `{ "FirstName": "string", "LastName": "string", "Sex": "M/F", "Department": "string", "YearLevel": int, "ClassID": int }` |
| POST | `/api/edit_student/{id}/` | Update student info | `{ "FirstName": "string", "LastName": "string", "Sex": "M/F", "Department": "string", "YearLevel": int, "ClassID": int }` |
| POST | `/api/delete_student/{id}/` | Delete student | None |

### Assignments

| Method | Endpoint | Description | Request Body |
|--------|----------|-------------|--------------|
| GET | `/api/get_assignments/?class_id={id}` | Get assignments by class | None |
| POST | `/api/assignments/` | Create assignment | `{ "ClassID": int, "Title": "string", "Instructions": "string", "DatePosted": "ISO8601", "DateOfSubmission": "ISO8601" }` |
| PUT | `/api/update_assignment/{id}/` | Update assignment | `{ "Title": "string", "Instructions": "string", "DateOfSubmission": "ISO8601" }` |
| DELETE | `/api/delete_assignment/{id}/` | Delete assignment | None |

### Dashboard

| Method | Endpoint | Description | Response |
|--------|----------|-------------|----------|
| GET | `/api/dashboard/` | Get dashboard statistics | `{ "total_assignments": int, "total_classes": int, "class_schedules": [...] }` |


### Date Format

The API uses ISO 8601 format for all datetime fields:

### Register a New User
```bash
curl -X POST http://localhost:8000/api/signup/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "password": "securepassword123",
    "role": "Instructor"
  }'
```

### Login
```bash
curl -X POST http://localhost:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "password": "securepassword123"
  }'
```

### Create a Class
```bash
curl -X POST http://localhost:8000/api/add_class/ \
  -H "Content-Type: application/json" \
  -d '{
    "ClassName": "CS101 - Introduction to Programming",
    "InstructorID": 1,
    "ScheduleDays": "MWF",
    "ScheduleTime": "10:00 AM - 11:30 AM"
  }'
```

### Add a Student
```bash
curl -X POST http://localhost:8000/api/add_student/ \
  -H "Content-Type: application/json" \
  -d '{
    "FirstName": "Jane",
    "LastName": "Smith",
    "Sex": "F",
    "Department": "Computer Science",
    "YearLevel": 2,
    "ClassID": 1
  }'
```

### Create an Assignment
```bash
curl -X POST http://localhost:8000/api/assignments/ \
  -H "Content-Type: application/json" \
  -d '{
    "ClassID": 1,
    "Title": "Python Basics Assignment",
    "Instructions": "Complete exercises 1-10 from the textbook",
    "DatePosted": "2025-10-07T10:00:00.000Z",
    "DateOfSubmission": "2025-10-14T23:59:59.000Z"
  }'
```

