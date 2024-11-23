from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('new/', views.task_create, name='task_create'),
    path('edit/<int:pk>/', views.task_edit, name='task_edit'),
    path('delete/<int:pk>/', views.task_delete, name='task_delete'),
    # path('invite/', views.invite_user, name='invite_user'),  # Add this line
    # path('invite/success/', views.success_view, name='invite_success'),  # Success page
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    
]
