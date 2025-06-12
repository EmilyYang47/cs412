# File: views.py
# Author: Emily Yang (eyang4@bu.edu), 5/27/2025
# Description: The views python file which creates the views to handle each page request.   

from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView , View, TemplateView    
from .models import * 
from .forms import * 
from django.urls import reverse 
from django.http import HttpResponseRedirect 
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth import login 

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

    def get_context_data(self): 
        '''Return the dictionary of context variables for use in the templates. ''' 

        # calling the superclass method 
        context = super().get_context_data() 

        # find/add the profile to the context data 
        # retrieve the PK from the URL pattern 
        user_creation_form = UserCreationForm

        # add this profile into the context dictionary: 
        context['user_creation_form'] = user_creation_form 
        return context 
    
    def form_valid(self, form): 
        '''a method to handle the form submission. ''' 

        # Reconstruct the UserCreationForm instance from the self.request.POST data 
        user_form = UserCreationForm(self.request.POST) 
        user = user_form.save() 

        # log the user in 
        login(self.request, user) 
        # attach the Django User to the Profile instance object 
        form.instance.user = user 
        # delegate the rest to the super class’ form_valid method. 
        return super().form_valid(form)   
    
    
class UpdateProfileView(LoginRequiredMixin, UpdateView): 
    '''A view to update an Profile and save it to the database.'''

    model = Profile  
    form_class = UpdateProfileForm
    template_name = "mini_fb/update_profile_form.html" 

    def get_object(self):
        '''Return the Profile object for the currently logged-in user.'''
        return Profile.objects.get(user=self.request.user) 

    def get_login_url(self): 
        '''return the URL required for login. ''' 
        return reverse('login') 


class CreateStatusMessageView(LoginRequiredMixin, CreateView): 
    '''A view to create a new status message and save it to the database. ''' 

    form_class = CreateStatusMessageForm 
    template_name = "mini_fb/create_status_form.html" 

    def get_context_data(self): 
        '''Return the dictionary of context variables for use in the templates. ''' 

        # calling the superclass method 
        context = super().get_context_data() 

        # find/add the profile to the context data 
        # retrieve the PK from the URL pattern 
        profile = Profile.objects.get(user=self.request.user) 

        # add this profile into the context dictionary: 
        context['profile'] = profile 
        return context 
    
    def get_login_url(self): 
        '''return the URL required for login. ''' 
        return reverse('login') 
    
    def form_valid(self, form): 
        '''a method to handle the form submission and saves the new object to the Django database. ''' 
        
        # find the logged in user 
        user = self.request.user 
        # attach user to form instance (Profile object):   
        form.instance.user = user 

        # retrieve the PK from the URL pattern 
        profile = Profile.objects.get(user=self.request.user) 
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
        # call reverse to generate the URL for this Profile 
        return reverse('show_profile', kwargs={'pk':Profile.objects.get(user=self.request.user).pk}) 


class DeleteStatusMessageView(LoginRequiredMixin, DeleteView): 
    '''A view to delete a status message. ''' 

    model = StatusMessage 
    template_name = "mini_fb/delete_status_form.html" 
    context_object_name = 'status_message' 

    def get_login_url(self): 
        '''return the URL required for login. ''' 
        return reverse('login') 

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
    
class UpdateStatusMessageView(LoginRequiredMixin, UpdateView): 
    '''A view to update an Profile and save it to the database.'''

    model = StatusMessage  
    form_class = UpdateStatusMessageForm
    template_name = "mini_fb/update_status_form.html" 
    context_object_name = 'status_message' 

    def get_login_url(self): 
        '''return the URL required for login. ''' 
        return reverse('login') 

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
    

class AddFriendView(LoginRequiredMixin, View): 
    '''A view to handle the add friend request. ''' 
   
    def get_object(self):
        '''Return the Profile object for the currently logged-in user.'''
        return Profile.objects.get(user=self.request.user)

    def dispatch(self, request, *args, **kwargs): 
        '''call the Profile's add_friend method. '''

        # retrieve the PK from the URL pattern 
        other_pk = self.kwargs['other_pk'] 

        # Get the profiles
        self_profile = Profile.objects.get(user=self.request.user)  
        other_profile = Profile.objects.get(pk=other_pk) 
        print("self retrieved is: ",  self_profile, "other retrieved is: ",  other_profile)

        # Add friend
        self_profile.add_friend(other_profile) 
        return HttpResponseRedirect(self.get_success_url())
     
    def get_success_url(self): 
        '''Provide a URL to redirect to after adding the new friend. ''' 

        # create and return a URL: 
        # call reverse to generate the URL for this Profile 
        return reverse('show_profile', kwargs={'pk':Profile.objects.get(user=self.request.user).pk}) 


class ShowFriendSuggestionsView(DetailView): 
    '''Define a view class to show the friend suggestions for a single Profile. ''' 
    model = Profile 
    template_name = "mini_fb/friend_suggestions.html" 
    context_object_name = 'profile' 

    def get_object(self):
        '''Return the Profile object for the currently logged-in user.'''
        return Profile.objects.get(user=self.request.user)


class ShowNewsFeedView(DetailView): 
    '''Define a view class to show the news feed for a single Profile. ''' 
    model = Profile 
    template_name = "mini_fb/news_feed.html" 
    context_object_name = 'profile' 

    def get_object(self):
        '''Return the Profile object for the currently logged-in user.'''
        return Profile.objects.get(user=self.request.user)

    
class LogoutConfirmationView(TemplateView): 
    '''Define a view class to show the logout confirmation page. '''
    template_name = "mini_fb/logged_out.html" 



