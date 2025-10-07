from django.urls import path
from . import views

urlpatterns = [
    path('api/signup/', views.signup, name='signup'),
    path("api/login/", views.login, name="login"),
    path("api/add_class/", views.add_class, name="add_class"),
    path("api/classes/", views.get_classes, name="get_classes"),
    path('api/classes/edit/<int:class_id>/', views.edit_class, name='edit_class'),
    path('api/classes/<int:class_id>/delete/', views.delete_class, name='delete_class'),
    path('api/assignments/', views.add_assignment, name='add_assignment'),
    path("api/get_assignments/", views.get_assignments, name="get_assignments"),
    path('api/update_assignment/<int:pk>/', views.update_assignment, name='update-assignment'),
    path('api/delete_assignment/<int:assignment_id>/', views.delete_assignment, name='delete_assignment'),
    path('api/dashboard/', views.dashboard_summary, name='dashboard-summary'),
    path('api/add_student/', views.add_student, name='add_student'),
    path('api/students/', views.get_students, name='get_students'),
    path('api/edit_student/<int:student_id>/', views.edit_student, name='edit_student'),
    path('api/delete_student/<int:student_id>/', views.delete_student, name='delete_student'),
    path('api/overdue_assignments/', views.overdue_assignments, name='overdue_assignments'),
    path('api/logout/', views.api_logout, name='api_logout'),
]
