from django.urls import path, include
from .views import TaskListView, TaskDetailView, CategoryView

urlpatterns = [
    path('tasks/', TaskListView.as_view(), name='task-list'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('tasks/categories/', CategoryView.as_view(), name='categories')
]