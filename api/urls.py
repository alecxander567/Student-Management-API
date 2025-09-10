from django.urls import path
from . import views

urlpatterns = [
    path('api/signup/', views.signup, name='signup'),
    path("api/login/", views.login, name="login"),
    path("api/add_class/", views.add_class, name="add_class"),
    path("api/classes/", views.get_classes, name="get_classes"),
]
