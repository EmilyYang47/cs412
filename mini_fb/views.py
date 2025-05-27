# File: views.py
# Author: Emily Yang (eyang4@bu.edu), 5/27/2025
# Description: The views python file which creates the views to handle each page request.   

from django.shortcuts import render
from django.views.generic import ListView, DetailView  
from .models import Profile 
import random 

# Create your views here.

class ShowAllProfilesView(ListView): 
    '''Define a view class to show all Facebook user Profiles. ''' 

    model = Profile 
    template_name = "mini_fb/show_all_profiles.html" 
    context_object_name = 'profiles' 


class ShowProfilePageView(DetailView): 
    '''Define a view class to show a single Facebook user Profile. ''' 

    model = Profile 
    template_name = "mini_fb/show_profile.html" 
    context_object_name = 'profile' 

