

from django.urls import path
from . import views

urlpatterns = [ 
    path('', views.ShowAllTaskDescriptionView.as_view(), name='home'), 
    path('todo_list/', views.ShowAllTaskDescriptionView.as_view(), name='todo_list'), 
    # path('task-update/<int:pk>/', views.TaskUpdate.as_view(), name='task-update'), 
    path('tasks/update/', views.TaskCompleteStatusUpdate.as_view(), name='update_complete_status'), 
    path('task/<int:pk>', views.ShowTaskDescriptionView.as_view(), name='show_task_description'), 
    path('task/<int:pk>/update', views.UpdateTaskDescriptionView.as_view(), name='update_task_description'), 
    path('task/<int:pk>/delete', views.DeleteTaskDescriptionView.as_view(), name='delete_task_description'), 
    path('task/create_task', views.CreateTaskDescriptionView.as_view(), name="create_task"), 
    path('timer/create', views.CreateTimerView.as_view(), name='create_timer'), 
    path('timer/<int:pk>', views.ShowTimerView.as_view(), name='timer'), 

]
