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
import plotly
import plotly.graph_objs as go 

from django.views.generic import TemplateView
from django.utils.timezone import localtime

from zoneinfo import ZoneInfo 
import datetime 


# the images of pets  
IMAGES = ["https://upload.wikimedia.org/wikipedia/en/f/fd/Pusheen_the_Cat.png", 
          "https://media.istockphoto.com/id/1097490360/vector/vector-illustration-of-cute-black-cat.jpg?s=612x612&w=0&k=20&c=Ef0qYl79aZJ6NJXJVbJ0onjXVNnSyqrN_TKPjieAIGE=", 
          "https://pngfre.com/wp-content/uploads/cat-74.png",           

          "https://media.istockphoto.com/id/1372997793/vector/cute-pembroke-welsh-corgi-dog-waving-paw-vector-illustration.jpg?s=612x612&w=0&k=20&c=T_GXRG6RG5Oy07rHGrR6XvKDQGY9mjeCmxjJ_oIVTGM=", 
          "https://as1.ftcdn.net/jpg/05/74/10/42/1000_F_574104298_h1KToZ3sdIuMhaFHvyChHDdODMy1YB27.webp", 
          "https://banner2.cleanpng.com/lnd/20240505/zxt/av80ljpty.webp" 
        ]  

# the name of pets  
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
        return TaskDescription.objects.filter(user=self.request.user).order_by('is_complete', 'due_time') 


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
    
    def get_form_kwargs(self): 
        '''get form keyword arguments'''
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs 
    
    def form_valid(self, form):
        '''
        Handle the form submission to update this TaskDescription object. 
        '''
        print(f'CreateArticleView: form.cleaned_data={form.cleaned_data}') 

        # find the logged in user
        user = self.request.user
        print(f"CreateArticleView user={user} article.user={user}") 
        # attach user to form instance:
        form.instance.user = user 

        # delegate work to the superclass version of this method
        return super().form_valid(form) 

    def get_success_url(self): 
        '''Provide a URL to redirect to after updating this task description. ''' 
        
        # create and return a URL: 
        # retrieve the PK from the URL pattern 
        pk = self.kwargs['pk'] 

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
    
    def get_form_kwargs(self): 
        '''get form keyword arguments'''
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs 
    
    def form_valid(self, form):
        '''
        Handle the form submission to create a new TaskDescription. 
        '''
        print(f'CreateArticleView: form.cleaned_data={form.cleaned_data}') 

        # find the logged in user
        user = self.request.user
        print(f"CreateArticleView user={user} article.user={user}") 
        # attach user to form instance: 
        form.instance.user = user 
        form.instance.is_complete = False 

        # delegate work to the superclass version of this method
        return super().form_valid(form) 


## Views to manage the timer: 

class CreateTimerView(LoginRequiredMixin, CreateView): 
    '''A view to handle creation of a new Timer. ''' 
    
    form_class = CreateTimerForm 
    template_name = "project/create_timer_form.html" 

    def get_login_url(self): 
        '''return the URL required for login. ''' 
        return reverse('login') 
    
    def get_form_kwargs(self): 
        '''get form keyword arguments'''
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs 

    def form_valid(self, form):
        ''' Handle the form submission to create a new Timer object. ''' 
        form.instance.time_spent = 0 
        
        # find the logged in user
        user = self.request.user
        print(f"CreateArticleView user={user} article.user={user}") 
        # attach user to form instance: 
        form.instance.user = user 

        # delegate work to the superclass version of this method
        return super().form_valid(form) 

    def get_success_url(self): 
        '''Provide a URL to redirect to after creating this Timer. ''' 

        # update the time_spent field of corresponding tag 
        tag = self.object.task.tag 
        start_of_today = datetime.datetime.now(ZoneInfo("America/New_York")).replace(
        hour=0, minute=0, second=0, microsecond=0 ) 
        
        if localtime(tag.timestamp) < start_of_today: 
            tag.time_spent = self.object.duration 
        else: 
            tag.time_spent += self.object.duration 

        tag.save()  

        # update the current_number_of_snacks field of the corresponding user profile  
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
    
    def form_valid(self, form):
        ''' Handle the form submission to create a new TaskTag object. ''' 
        form.instance.time_spent = 0 
        
        # find the logged in user
        user = self.request.user
        print(f"CreateArticleView user={user} article.user={user}") 
        # attach user to form instance: 
        form.instance.user = user 

        # delegate work to the superclass version of this method
        return super().form_valid(form) 

    def get_success_url(self): 
        '''Provide a URL to redirect to after creating this tag. ''' 
        return reverse('show_all_tags') 


## Views to manage the user profiles: 

class ShowAllUserProfileView(ListView): 
    '''Define a view class to show all user profiles. ''' 

    model = UserProfile  
    template_name = "project/show_all_profiles.html" 
    context_object_name = 'all_profiles' 


class ShowUserProfileView(DetailView): 
    '''Define a view class to show a single user profile. ''' 

    model = UserProfile  
    template_name = "project/show_profile.html" 
    context_object_name = 'profile' 


class ShowMyUserProfileView(DetailView): 
    '''Define a view class to show the logged-in user's profile. ''' 

    model = UserProfile  
    template_name = "project/show_profile.html" 
    context_object_name = 'profile' 
    
    def get_object(self):
        '''Return the Profile object for the currently logged-in user.'''
        return UserProfile.objects.get(user=self.request.user) 
    

class CreateUserProfileView(CreateView): 
    '''A view to handle creation of a new UserProfile. ''' 
    
    form_class = CreateUserProfileForm 
    template_name = "project/create_user_profile_form.html" 

    def get_context_data(self): 
        '''Return the dictionary of context variables for use in the templates. ''' 

        # calling the superclass method 
        context = super().get_context_data() 

        # add the UserCreationForm into the context dictionary: 
        user_creation_form = UserCreationForm 
        context['user_creation_form'] = user_creation_form 
        return context 
    
    def form_valid(self, form): 
        '''a method to handle the form submission. ''' 

        # Reconstruct the UserCreationForm instance from the self.request.POST data 
        user_form = UserCreationForm(self.request.POST) 
        user = user_form.save() 

        # log the user in 
        login(self.request, user) 
        # attach the Django User to the UserProfile instance object 
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
    '''A view to update a user profile and save it to the database.'''

    model = UserProfile  
    form_class = UpdateUserProfileForm
    template_name = "project/update_user_profile_form.html" 
    context_object_name = 'profile' 

    def get_login_url(self): 
        '''return the URL required for login. ''' 
        return reverse('login') 
    
    def get_object(self):
        '''Return the UserProfile object for the currently logged-in user.'''
        return UserProfile.objects.get(user=self.request.user) 
    

## Views to manage the pets: 

class FeedPetView(LoginRequiredMixin, View): 
    '''A view to handle feed pet request. ''' 

    def get_login_url(self): 
        '''return the URL required for login. ''' 
        return reverse('project_login') 

    def post(self, request, *args, **kwargs): 
        '''Handle the post request, feed the pet. ''' 

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
        '''Provide a URL to redirect to after feeding the pet. ''' 

        user = self.request.user 
        # attach user to form instance:
        profile = UserProfile.objects.get(user=user)  
        return reverse('profile', kwargs={'pk': profile.pk}) 


class AdoptPetConfirmationView(LoginRequiredMixin, TemplateView): 
    '''Define a view class to show the adopt_pet_confirmation page. '''      
    template_name = 'project/adopt_pet_confirmation_form.html' 

    def get_login_url(self): 
        '''return the URL required for login. ''' 
        return reverse('project_login')     
    
    def get_context_data(self): 
        '''Return the dictionary of context variables for use in the templates. ''' 

        # calling the superclass method 
        context = super().get_context_data() 
        user = self.request.user
        # attach the profile into the context dictionary  
        profile = UserProfile.objects.get(user=user)  

        context['profile'] = profile 
        return context 


class AdoptPetView(LoginRequiredMixin, View): 
    '''A view to handle the adopt pet request. ''' 

    def get_login_url(self): 
        '''return the URL required for login. ''' 
        return reverse('project_login') 
    
    def post(self, request, *args, **kwargs): 
        '''Handle the post request, adopt a new pet. ''' 

        image_url = random.choice(IMAGES)
        name = random.choice(NAMES)
        user = request.user
        profile = UserProfile.objects.get(user=user)

        if profile.current_number_of_snacks >= 7500:
            pet = Pet(image_url=image_url, name=name, affection_level=0, profile=profile)
            pet.save()
            profile.current_number_of_snacks -= 7500
            profile.save()

        return HttpResponseRedirect(self.get_success_url()) 

    def get_success_url(self): 
        '''Provide a URL to redirect to after adopting the pet. ''' 
        return reverse('my_profile') 


## View to analyze time spent distribution 

class FocusTimeChartView(TemplateView): 
    '''Define a view class to show the focus time chart page. ''' 
    template_name = 'project/show_daily_focus_time_chart.html'

    def get_context_data(self, **kwargs): 
        '''Return the dictionary of context variables for use in the templates. '''  

        context = super().get_context_data(**kwargs)
        user = self.request.user

        start_of_today = datetime.datetime.now(ZoneInfo("America/New_York")).replace(
        hour=0, minute=0, second=0, microsecond=0 )

        # create graph of focus time distribution on task tags as pie chart: 
        tags = TaskTag.objects.filter(user=user, timestamp__gte=start_of_today)
        if tags.exists():
            x = [t.tag for t in tags]
            y = [t.time_spent / 60 for t in tags]  # convert to hour

            pie_fig = go.Pie(labels=x, values=y)
            pie_div = plotly.offline.plot({
                "data": [pie_fig],
                "layout_title_text": "Time Spent on Each Task Tag (hour)"
            }, auto_open=False, output_type="div")
            context['graph_div_pie'] = pie_div
        else:
            context['graph_div_pie'] = "<div>No study sessions yet</div>"              

        # create graph of focus time distribution of the day as bar chart: 
        timers = Timer.objects.filter(user=user, timestamp__gte=start_of_today)
        if timers.exists():
            x = [localtime(t.timestamp).strftime('%H:%M') for t in timers]
            y = [t.duration / 60 for t in timers]

            bar_fig = go.Bar(x=x, y=y)
            bar_div = plotly.offline.plot({
                "data": [bar_fig],
                "layout_title_text": "Focus Time Distribution of the Day (hour)"
            }, auto_open=False, output_type="div")
            context['graph_div_bar'] = bar_div
        else:
            context['graph_div_bar'] = "<div>No focus sessions yet</div>"

        return context


## Template view for logout confirmation 

class ProjectLogoutConfirmationView(TemplateView): 
    '''Define a view class to show the logout confirmation page. '''
    template_name = "project/logged_out.html" 

    