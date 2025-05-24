# File: urls.py
# Author: Emily Yang (eyang4@bu.edu), 5/24/2025
# Description: The urls python file which matches urls to their corresponding pages.  

from django.urls import path
from django.conf import settings
from . import views

urlpatterns = [ 
    path(r'', views.main, name="main"), 
    path(r'main', views.main, name="main"), 
    path(r'order', views.order, name="order"), 
    path(r'confirmation', views.confirmation, name="confirmation"), 
]
