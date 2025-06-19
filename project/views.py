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


## Views to manage the todo-list: 

class ShowAllTaskDescriptionView(ListView): 
    '''Define a view class to show all task descriptions. ''' 

    model = TaskDescription 
    template_name = "project/todo_list.html" 
    context_object_name = 'todo_list' 


class TaskCompleteStatusUpdate(View): 
    '''A view to handle the task complete status modification request. ''' 

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
    

class ShowTaskDescriptionView(DetailView): 
    '''Define a view class to show a Task Description. ''' 

    model = TaskDescription  
    template_name = "project/show_task_description.html" 
    context_object_name = 'task_description' 


class UpdateTaskDescriptionView(UpdateView): 
    '''A view to update a task description and save it to the database.'''

    model = TaskDescription  
    form_class = UpdateTaskDescriptionForm
    template_name = "project/update_task_description_form.html" 
    context_object_name = 'task_description' 

    def get_success_url(self): 
        '''Provide a URL to redirect to after updating this task description. ''' 
        
        # create and return a URL: 
        # retrieve the PK from the URL pattern 
        pk = self.kwargs['pk'] 

        # call reverse to generate the URL for this Profile 
        return reverse('show_task_description', kwargs={'pk': pk}) 
    

class DeleteTaskDescriptionView(DeleteView): 
    '''A view to delete a task. ''' 

    model = TaskDescription 
    template_name = "project/delete_task_form.html" 
    context_object_name = 'task_description' 

    # def get_login_url(self): 
    #     '''return the URL required for login. ''' 
    #     return reverse('login') 

    def get_success_url(self): 
        '''Provide a URL to redirect to after deleting this task. ''' 
        return reverse('todo_list') 

class CreateTaskDescriptionView(CreateView): 
    '''A view to handle creation of a new TaskDescription. ''' 
    
    form_class = CreateTaskDescriptionForm 
    template_name = "project/create_task_description_form.html" 

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

class CreateTimerView(CreateView): 
    '''A view to handle creation of a new TaskDescription. ''' 
    
    form_class = CreateTimerForm 
    template_name = "project/create_timer_form.html" 

    def get_success_url(self): 
        '''Provide a URL to redirect to after creating this task. ''' 

        # update the time_spent field of corresponding tag 
        tag = self.object.task.tag 
        tag.time_spent = self.object.duration 
        tag.save() 

        return reverse('timer', kwargs={'pk': self.object.pk})


class ShowTimerView(DetailView): 
    '''Define a view class to show a single Timer object. ''' 
    
    model = Timer  
    template_name = "project/show_timer.html" 
    context_object_name = 'timer' 
