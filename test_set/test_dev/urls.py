from . import views
from django.urls import path

urlpatterns = [
    path('', views.task, name='task'),
    path('register/', views.register, name='register'),
    path('receive-task/', views.receive_task, name='receive_task'),
    path('process-task/', views.process_task, name='process_task'),
]