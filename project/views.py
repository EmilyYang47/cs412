# File: views.py
# Author: Emily Yang (eyang4@bu.edu), 6/18/2025
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


# the images of pets  
IMAGES = ["https://upload.wikimedia.org/wikipedia/en/f/fd/Pusheen_the_Cat.png", 
          "https://media.istockphoto.com/id/1097490360/vector/vector-illustration-of-cute-black-cat.jpg?s=612x612&w=0&k=20&c=Ef0qYl79aZJ6NJXJVbJ0onjXVNnSyqrN_TKPjieAIGE=", 
          "https://pngfre.com/wp-content/uploads/cat-74.png",           

          "https://media.istockphoto.com/id/1372997793/vector/cute-pembroke-welsh-corgi-dog-waving-paw-vector-illustration.jpg?s=612x612&w=0&k=20&c=T_GXRG6RG5Oy07rHGrR6XvKDQGY9mjeCmxjJ_oIVTGM=", 
          "https://as1.ftcdn.net/jpg/05/74/10/42/1000_F_574104298_h1KToZ3sdIuMhaFHvyChHDdODMy1YB27.webp", 
          "https://banner2.cleanpng.com/lnd/20240505/zxt/av80ljpty.webp" 
        ]  

NAMES = ['Popcorn', 'Bread', 'Banana', 'Ice Cream', 'Hummus', 'Pasta']


## Views to manage the todo-list: 

class ShowAllTaskDescriptionsView(LoginRequiredMixin, ListView): 
    '''Define a view class to show all task descriptions. ''' 

    model = TaskDescription 
    template_name = "project/todo_list.html" 
    context_object_name = 'todo_list' 

    def get_login_url(self): 
        '''return the URL required for login. ''' 
        return reverse('project_login') 

    def get_queryset(self):
        '''show only the task descriptions of current user. ''' 
        return TaskDescription.objects.filter(user=self.request.user) 


class TaskCompleteStatusUpdate(LoginRequiredMixin, View): 
    '''A view to handle the task complete status modification request. ''' 

    def get_login_url(self): 
        '''return the URL required for login. ''' 
        return reverse('project_login') 

    def post(self, request, *args, **kwargs): 
        '''Modify the status. ''' 
        print(request.POST)
        all_tasks = TaskDescription.objects.all()

        completed_task_ids = request.POST.getlist('completed_tasks')

        for task in all_tasks:
            task.is_complete = str(task.id) in completed_task_ids
            task.save()

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self): 
        '''Provide a URL to redirect to after modifying the complete status. ''' 
        return reverse('todo_list') 
    

class ShowTaskDescriptionView(LoginRequiredMixin, DetailView): 
    '''Define a view class to show a Task Description. ''' 

    model = TaskDescription  
    template_name = "project/show_task_description.html" 
    context_object_name = 'task_description' 

    def get_login_url(self): 
        '''return the URL required for login. ''' 
        return reverse('project_login') 


class UpdateTaskDescriptionView(LoginRequiredMixin, UpdateView): 
    '''A view to update a task description and save it to the database.'''

    model = TaskDescription  
    form_class = UpdateTaskDescriptionForm
    template_name = "project/update_task_description_form.html" 
    context_object_name = 'task_description' 

    def get_login_url(self): 
        '''return the URL required for login. ''' 
        return reverse('project_login') 

    def get_success_url(self): 
        '''Provide a URL to redirect to after updating this task description. ''' 
        
        # create and return a URL: 
        # retrieve the PK from the URL pattern 
        pk = self.kwargs['pk'] 

        # call reverse to generate the URL for this Profile 
        return reverse('show_task_description', kwargs={'pk': pk}) 
    

class DeleteTaskDescriptionView(LoginRequiredMixin, DeleteView): 
    '''A view to delete a task. ''' 

    model = TaskDescription 
    template_name = "project/delete_task_form.html" 
    context_object_name = 'task_description' 

    def get_login_url(self): 
        '''return the URL required for login. ''' 
        return reverse('login') 

    def get_success_url(self): 
        '''Provide a URL to redirect to after deleting this task. ''' 
        return reverse('todo_list') 

class CreateTaskDescriptionView(LoginRequiredMixin, CreateView): 
    '''A view to handle creation of a new TaskDescription. ''' 
    
    form_class = CreateTaskDescriptionForm 
    template_name = "project/create_task_description_form.html" 

    def get_login_url(self): 
        '''return the URL required for login. ''' 
        return reverse('login') 

    def get_success_url(self): 
        '''Provide a URL to redirect to after creating this task. ''' 
        return reverse('todo_list') 
    
    def form_valid(self, form):
        '''
        Handle the form submission to create a new TaskDescription. 
        '''
        print(f'CreateArticleView: form.cleaned_data={form.cleaned_data}') 

        # find the logged in user
        user = self.request.user
        print(f"CreateArticleView user={user} article.user={user}") 
        # attach user to form instance (Article object):
        form.instance.user = user 
        form.instance.is_complete = False 

        # delegate work to the superclass version of this method
        return super().form_valid(form) 


## Views to manage the timer: 

class CreateTimerView(LoginRequiredMixin, CreateView): 
    '''A view to handle creation of a new TaskDescription. ''' 
    
    form_class = CreateTimerForm 
    template_name = "project/create_timer_form.html" 

    def get_login_url(self): 
        '''return the URL required for login. ''' 
        return reverse('login') 

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs 

    def form_valid(self, form):
        ''' Handle the form submission to create a new TaskTag object. ''' 
        form.instance.time_spent = 0 
        
        # find the logged in user
        user = self.request.user
        print(f"CreateArticleView user={user} article.user={user}") 
        # attach user to form instance (Article object):
        form.instance.user = user 

        # delegate work to the superclass version of this method
        return super().form_valid(form) 

    def get_success_url(self): 
        '''Provide a URL to redirect to after creating this task. ''' 

        # update the time_spent field of corresponding tag 
        tag = self.object.task.tag 
        tag.time_spent += self.object.duration 
        tag.save()  

        # update the current_number_of_snacks field of corresponding user profile  
        user = self.request.user 
        profile = UserProfile.objects.get(user=user)  
        profile.current_number_of_snacks += self.object.duration 
        profile.save()  

        return reverse('timer', kwargs={'pk': self.object.pk})


class ShowTimerView(DetailView): 
    '''Define a view class to show a single Timer object. ''' 
    
    model = Timer  
    template_name = "project/show_timer.html" 
    context_object_name = 'timer' 

    


## Views to manage the tags: 

class ShowAllTaskTagsView(LoginRequiredMixin, ListView): 
    '''Define a view class to show all task tags. ''' 

    model = TaskTag 
    template_name = "project/show_all_tags.html" 
    context_object_name = 'all_tags' 

    def get_login_url(self): 
        '''return the URL required for login. ''' 
        return reverse('login') 

    def get_queryset(self):
        '''show only the task tags of current user. ''' 
        return TaskTag.objects.filter(user=self.request.user) 


class UpdateTaskTagView(LoginRequiredMixin, UpdateView): 
    '''A view to update a task tag and save it to the database.'''

    model = TaskTag  
    form_class = UpdateTaskTagForm
    template_name = "project/update_task_tag_form.html" 
    context_object_name = 'task_tag' 

    def get_login_url(self): 
        '''return the URL required for login. ''' 
        return reverse('login') 

    def get_success_url(self): 
        '''Provide a URL to redirect to after updating this task tag. ''' 
        
        # create and return a URL: 
        # retrieve the PK from the URL pattern 

        # call reverse to generate the URL for this Profile 
        return reverse('show_all_tags') 
    

class DeleteTaskTagView(LoginRequiredMixin, DeleteView): 
    '''A view to delete a task tag. ''' 

    model = TaskTag 
    template_name = "project/delete_task_tag_form.html" 
    context_object_name = 'task_tag' 

    def get_login_url(self): 
        '''return the URL required for login. ''' 
        return reverse('login') 

    def get_success_url(self): 
        '''Provide a URL to redirect to after deleting this task tag. ''' 
        return reverse('show_all_tags') 


class CreateTaskTagView(LoginRequiredMixin, CreateView): 
    '''A view to handle creation of a new TaskTag. ''' 
    
    form_class = CreateTaskTagForm 
    template_name = "project/create_task_tag_form.html" 

    def get_login_url(self): 
        '''return the URL required for login. ''' 
        return reverse('login') 

    def get_success_url(self): 
        '''Provide a URL to redirect to after creating this task. ''' 
        return reverse('show_all_tags') 
    
    def form_valid(self, form):
        ''' Handle the form submission to create a new TaskTag object. ''' 
        form.instance.time_spent = 0 
        
        # find the logged in user
        user = self.request.user
        print(f"CreateArticleView user={user} article.user={user}") 
        # attach user to form instance (Article object):
        form.instance.user = user 

        # delegate work to the superclass version of this method
        return super().form_valid(form) 


## Views to manage the user profiles: 

class ShowAllUserProfileView(ListView): 
    '''Define a view class to show a Task Description. ''' 

    model = UserProfile  
    template_name = "project/show_all_profiles.html" 
    context_object_name = 'all_profiles' 


class ShowUserProfileView(DetailView): 
    '''Define a view class to show a Task Description. ''' 

    model = UserProfile  
    template_name = "project/show_profile.html" 
    context_object_name = 'profile' 


class CreateUserProfileView(CreateView): 
    '''A view to handle creation of a new Profile. ''' 
    
    form_class = CreateUserProfileForm 
    template_name = "project/create_user_profile_form.html" 

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
        form.instance.current_number_of_snacks = 0 

        tag = TaskTag(tag='Other', time_spent=0, user=user) 
        tag.save() 

        image_url = random.choice(IMAGES)  
        name = random.choice(NAMES)  
        profile = form.save()  
        
        pet = Pet(image_url=image_url, name=name, affection_level=0, profile=profile) 
        pet.save() 

        # delegate the rest to the super class’ form_valid method. 
        return super().form_valid(form)   


class UpdateUserProfileView(LoginRequiredMixin, UpdateView): 
    '''A view to update a task tag and save it to the database.'''

    model = UserProfile  
    form_class = UpdateUserProfileForm
    template_name = "project/update_user_profile_form.html" 
    context_object_name = 'profile' 

    def get_login_url(self): 
        '''return the URL required for login. ''' 
        return reverse('login') 
    
    def get_object(self):
        '''Return the Profile object for the currently logged-in user.'''
        return UserProfile.objects.get(user=self.request.user) 
    

## Views to manage the pets: 

class FeedPetView(LoginRequiredMixin, View): 
    '''A view to handle the task complete status modification request. ''' 

    def get_login_url(self): 
        '''return the URL required for login. ''' 
        return reverse('project_login') 

    def post(self, request, *args, **kwargs): 
        '''Modify the status. ''' 

        print(request.POST) 
         
        # update the affection_level field of the pet 
        pk = self.kwargs['pk']        
        pet = Pet.objects.get(pk=pk) 
        pet.affection_level += 1 
        pet.save() 
        # update the current_number_of_snacks field of the corresponding user profile   
        user = self.request.user 
        profile = UserProfile.objects.get(user=user)  
        profile.current_number_of_snacks -= 100 
        profile.save() 

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self): 
        '''Provide a URL to redirect to after modifying the complete status. ''' 
        user = self.request.user
        # attach user to form instance (Article object):
        profile = UserProfile.objects.get(user=user)  
        return reverse('profile', kwargs={'pk': profile.pk}) 


class AdoptPetView(LoginRequiredMixin, View): 
    '''A view to handle the task complete status modification request. ''' 

    def get_login_url(self): 
        '''return the URL required for login. ''' 
        return reverse('project_login') 

    def get_success_url(self): 
        '''Provide a URL to redirect to after modifying the complete status. ''' 
        image_url = random.choice(IMAGES)  
        name = random.choice(NAMES)  
        user = self.request.user
        profile = UserProfile.objects.get(user=user)  
        
        pet = Pet(image_url=image_url, name=name, affection_level=0, profile=profile) 
        pet.save() 

        profile.current_number_of_snacks -= 7500
        
        return reverse('profile', kwargs={'pk': profile.pk}) 


## Template view for logiut confirmation 

class ProjectLogoutConfirmationView(TemplateView): 
    '''Define a view class to show the logout confirmation page. '''
    template_name = "project/logged_out.html" 

    