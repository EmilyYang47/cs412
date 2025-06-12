# File: urls.py
# Author: Emily Yang (eyang4@bu.edu), 5/27/2025
# Description: The urls python file which matches urls to their corresponding pages.  

from django.urls import path 
from .views import * 

# generic view for authentication/authorization 
from django.contrib.auth import views as auth_views 

urlpatterns = [           
    path('', ShowAllProfilesView.as_view(), name="show_all_profiles"), 
    path('profile/<int:pk>', ShowProfilePageView.as_view(), name="show_profile"), 
    path('create_profile', CreateProfileView.as_view(), name="create_profile"), 
    path('status/create_status', CreateStatusMessageView.as_view(), name="create_status"), 
    path('profile/update', UpdateProfileView.as_view(), name="update_profile"), 
    path('status/<int:pk>/delete', DeleteStatusMessageView.as_view(), name="delete_status"),       
    path('status/<int:pk>/update', UpdateStatusMessageView.as_view(), name="update_status"),      
    path('profile/add_friend/<int:other_pk>', AddFriendView.as_view(), name="add_friend"),   
    path('profile/friend_suggestions', ShowFriendSuggestionsView.as_view(), name="show_friend_suggestions"),  
    path('profile/news_feed', ShowNewsFeedView.as_view(), name="show_news_feed"),    
    # authorization-related URLs: 
    path('login/', auth_views.LoginView.as_view(template_name='mini_fb/login.html'), name='login'), 
    path('logout/', auth_views.LogoutView.as_view(next_page='logout_confirmation'), name='logout'), 
    path('logged_out/', LogoutConfirmationView.as_view(), name='logout_confirmation'), 
    # path('blog_register/', UserRegistrationView.as_view(), name='register') 
] 

