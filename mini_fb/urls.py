# File: urls.py
# Author: Emily Yang (eyang4@bu.edu), 5/27/2025
# Description: The urls python file which matches urls to their corresponding pages.  

from django.urls import path 
from .views import ShowAllProfilesView, ShowProfilePageView

urlpatterns = [
    path('', ShowAllProfilesView.as_view(), name="show_all_profiles"), 
    path('profile/<int:pk>', ShowProfilePageView.as_view(), name="show_profile"), 
] 

