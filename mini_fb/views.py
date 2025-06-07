# File: views.py
# Author: Emily Yang (eyang4@bu.edu), 5/27/2025
# Description: The views python file which creates the views to handle each page request.   

from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView , View   
from .models import * 
from .forms import * 
from django.urls import reverse 
from django.http import HttpResponseRedirect 

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


class UpdateProfileView(UpdateView): 
    '''A view to update an Profile and save it to the database.'''

    model = Profile  
    form_class = UpdateProfileForm
    template_name = "mini_fb/update_profile_form.html" 


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

        # save the status message to database
        sm = form.save() 

        # read the file from the form:
        files = self.request.FILES.getlist('files') 

        # for each file, create and store an Image object and a StatusImage object  
        for file in files: 
            # Create an Image object 
            image = Image(image_file=file, profile=profile) 
            image.save() 
            
            # Create and save a StatusImage 
            status_image = StatusImage(status_message=sm, image=image) 
            status_image.save() 


        # delegate the work to the superclass method form_valid: 
        return super().form_valid(form) 
    
    def get_success_url(self): 
        '''Provide a URL to redirect to after creating a new status message. ''' 

        # create and return a URL: 
        # retrieve the PK from the URL pattern 
        pk = self.kwargs['pk'] 
        # call reverse to generate the URL for this Profile 
        return reverse('show_profile', kwargs={'pk':pk}) 


class DeleteStatusMessageView(DeleteView): 
    '''A view to delete a status message. ''' 

    model = StatusMessage 
    template_name = "mini_fb/delete_status_form.html" 
    context_object_name = 'status_message' 

    def get_success_url(self): 
        '''Provide a URL to redirect to after deleting this status message. ''' 
        
        # create and return a URL: 
        # retrieve the PK from the URL pattern 
        pk = self.kwargs['pk'] 

        status_message = StatusMessage.objects.get(pk=pk)
        
        # find the profile to which this status is related by FK
        profile = status_message.profile 

        # call reverse to generate the URL for this Profile 
        return reverse('show_profile', kwargs={'pk':profile.pk}) 
    
class UpdateStatusMessageView(UpdateView): 
    '''A view to update an Profile and save it to the database.'''

    model = StatusMessage  
    form_class = UpdateStatusMessageForm
    template_name = "mini_fb/update_status_form.html" 
    context_object_name = 'status_message' 

    def get_success_url(self): 
        '''Provide a URL to redirect to after updating this status message. ''' 
        
        # create and return a URL: 
        # retrieve the PK from the URL pattern 
        pk = self.kwargs['pk'] 

        status_message = StatusMessage.objects.get(pk=pk)
        
        # find the profile to which this status is related by FK
        profile = status_message.profile 

        # call reverse to generate the URL for this Profile 
        return reverse('show_profile', kwargs={'pk':profile.pk}) 
    

class AddFriendView(View): 
    '''A view to handle the add friend request. ''' 

    def dispatch(self, request, *args, **kwargs): 
        '''call the Profile's add_friend method. '''

        # retrieve the PK from the URL pattern 
        pk = self.kwargs['pk']
        other_pk = self.kwargs['other_pk'] 

        # Get the profiles
        self_profile = Profile.objects.get(pk=pk) 
        other_profile = Profile.objects.get(pk=other_pk) 

        # Add friend
        self_profile.add_friend(other_profile) 
        return HttpResponseRedirect(self.get_success_url())
    
    def get_success_url(self): 
        '''Provide a URL to redirect to after adding the new friend. ''' 

        # create and return a URL: 
        # retrieve the PK from the URL pattern 
        pk = self.kwargs['pk'] 
        # call reverse to generate the URL for this Profile 
        return reverse('show_profile', kwargs={'pk':pk}) 

class ShowFriendSuggestionsView(DetailView): 
    '''Define a view class to show the friend suggestions for a single Profile. ''' 
    model = Profile 
    template_name = "mini_fb/friend_suggestions.html" 
    context_object_name = 'profile' 