# File: urls.py
# Author: Emily Yang (eyang4@bu.edu), 6/18/2025
# Description: The urls python file which matches urls to their corresponding pages.  

from django.urls import path
from . import views

# generic view for authentication/authorization 
from django.contrib.auth import views as auth_views 

urlpatterns = [ 
    path('', views.ShowAllUserProfileView.as_view(), name='home'), 
    path('todo_list/', views.ShowAllTaskDescriptionsView.as_view(), name='todo_list'), 
    path('tasks/update/', views.TaskCompleteStatusUpdate.as_view(), name='update_complete_status'), 
    path('task/<int:pk>', views.ShowTaskDescriptionView.as_view(), name='show_task_description'), 
    path('task/<int:pk>/update', views.UpdateTaskDescriptionView.as_view(), name='update_task_description'), 
    path('task/<int:pk>/delete', views.DeleteTaskDescriptionView.as_view(), name='delete_task_description'), 
    path('task/create_task', views.CreateTaskDescriptionView.as_view(), name="create_task"), 

    path('timer/create', views.CreateTimerView.as_view(), name='create_timer'), 
    path('timer/<int:pk>', views.ShowTimerView.as_view(), name='timer'), 

    path('tags/', views.ShowAllTaskTagsView.as_view(), name='show_all_tags'), 
    path('tag/<int:pk>/update', views.UpdateTaskTagView.as_view(), name='update_task_tag'), 
    path('tag/<int:pk>/delete', views.DeleteTaskTagView.as_view(), name='delete_task_tag'), 
    path('tag/create_task_tag', views.CreateTaskTagView.as_view(), name='create_task_tag'), 

    path('profiles/', views.ShowAllUserProfileView.as_view(), name='all_profiles'),    
    path('profile/<int:pk>', views.ShowUserProfileView.as_view(), name='profile'), 
    path('my_profile/', views.ShowMyUserProfileView.as_view(), name='my_profile'),    
    path('profile/update', views.UpdateUserProfileView.as_view(), name='update_user_profile'),  
    path('feed_pet/<int:pk>', views.FeedPetView.as_view(), name="feed_pet"), 
    path('my_profile/adopt_pet/', views.AdoptPetView.as_view(), name="adopt_pet"), 
    path('my_profile/adopt_pet_confirmation/', views.AdoptPetConfirmationView.as_view(), name="adopt_pet_confirmation"), 
    path('daily_focus_time_chart/', views.FocusTimeChartView.as_view(), name="daily_focus_time_chart"), 


    # authorization-related URLs: 
    path('project_login/', auth_views.LoginView.as_view(template_name='project/login.html'), name='project_login'), 
    path('project_logout/', auth_views.LogoutView.as_view(next_page='project_logout_confirmation'), name='project_logout'), 
    path('project_logged_out/', views.ProjectLogoutConfirmationView.as_view(), name='project_logout_confirmation'), 
    path('create_user_profile/', views.CreateUserProfileView.as_view(), name="create_user_profile"), 



]
