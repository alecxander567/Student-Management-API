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
    path('api/activities/', views.add_activity, name='add-activity'),
    path('api/logout/', views.api_logout, name='api_logout'),
]
