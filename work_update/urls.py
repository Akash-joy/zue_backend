from django.urls import path
from .views import TaskDeleteView, TaskStateList, TaskCreateView, TaskUpdateView

urlpatterns = [
    path('states/', TaskStateList.as_view(), name='taskstate-list'),
    path('tasks/', TaskCreateView.as_view(), name='task-create'),
    path('tasks/<int:pk>/', TaskDeleteView.as_view(), name='task-delete'),
    path('tasks/update/<int:pk>/', TaskUpdateView.as_view(), name='task-update'),

]