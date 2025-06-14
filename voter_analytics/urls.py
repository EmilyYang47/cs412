# File: urls.py
# Author: Emily Yang (eyang4@bu.edu), 6/14/2025
# Description: The urls python file which matches urls to their corresponding pages.  

from django.urls import path
from . import views 

urlpatterns = [
    # map the URL (empty string) to the view
	path(r'', views.VotersListView.as_view(), name='voters'), 
    path(r'voter/<int:pk>', views.VoterDetailView.as_view(), name='voter'), 
    path(r'graphs', views.GraphsListView.as_view(), name='graphs'), 
] 