# File: views.py
# Author: Emily Yang (eyang4@bu.edu), 5/27/2025
# Description: The views python file which creates the views to handle each page request.   

from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView   
from .models import Profile 
from .forms import * 
from django.urls import reverse 

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

class CreateProfileView(CreateView): 
    '''A view to handle creation of a new Profile. ''' 
    
    form_class = CreateProfileForm 
    template_name = "mini_fb/create_profile_form.html" 

class CreateStatusMessageView(CreateView): 
    '''A view to create a new status message and save it to the database. ''' 

    form_class = CreateStatusMessageForm 
    template_name = "mini_fb/create_status_form.html" 

    def get_context_data(self): 
        '''Return the dictionary of context variables for use in the templates. ''' 

        # calling the superclass method 
        context = super().get_context_data() 

        # find/add the profile to the context data 
        # retrieve the PK from the URL pattern 
        pk = self.kwargs['pk'] 
        profile = Profile.objects.get(pk=pk) 

        # add this profile into the context dictionary: 
        context['profile'] = profile 
        return context 
    
    def form_valid(self, form): 
        '''a method to handle the form submission and saves the new object to the Django database. ''' 

        # retrieve the PK from the URL pattern 
        pk = self.kwargs['pk'] 
        profile = Profile.objects.get(pk=pk) 
        # attach this profile to the status message 
        form.instance.profile = profile # set the FK 

        # delegate the work to the superclass method form_valid: 
        return super().form_valid(form) 
    
    def get_success_url(self): 
        '''Provide a URL to redirect to after creating a new status message. ''' 

        # create and return a URL: 
        # retrieve the PK from the URL pattern 
        pk = self.kwargs['pk'] 
        # call reverse to generate the URL for this Profile 
        return reverse('show_profile', kwargs={'pk':pk}) 


        