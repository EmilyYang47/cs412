# File: forms.py
# Author: Emily Yang (eyang4@bu.edu), 6/18/2025
# Description: The forms python file which creates the forms to add new model objects to the database.   

from django import forms
from .models import *  

## Forms for Task Description  
class UpdateTaskDescriptionForm(forms.ModelForm): 
    '''A form to update the task description. ''' 

    class Meta: 
        '''associate this form with the TaskDescription model from our database. ''' 
        model = TaskDescription 
        fields = ['task', 'tag', 'is_complete', 'due_time'] 

    def __init__(self, *args, **kwargs): 
        '''Only allow users to select task tags associated with their own account. ''' 

        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user is not None:
            self.fields['tag'].queryset = TaskTag.objects.filter(user=user) 


class CreateTaskDescriptionForm(forms.ModelForm): 
    '''A form to create the task description. ''' 

    class Meta: 
        '''associate this form with the TaskDescription model from our database. ''' 
        model = TaskDescription 
        fields = ['task', 'tag', 'due_time'] 

    def __init__(self, *args, **kwargs): 
        '''Only allow users to select task tags associated with their own account. ''' 
        
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user is not None:
            self.fields['tag'].queryset = TaskTag.objects.filter(user=user) 


## Forms for Timer 
class CreateTimerForm(forms.ModelForm): 
    '''A form to create the timer. ''' 

    class Meta: 
        '''associate this form with the Timer model from our database. ''' 
        model = Timer 
        fields = ['duration', 'task'] 

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user is not None:
            self.fields['task'].queryset = TaskDescription.objects.filter(user=user)


## Forms for Task Tag 
class UpdateTaskTagForm(forms.ModelForm): 
    '''A form to update the task tag. ''' 

    class Meta: 
        '''associate this form with the TaskTag model from our database. ''' 
        model = TaskTag 
        fields = ['tag'] 

class CreateTaskTagForm(forms.ModelForm): 
    '''A form to create the task tag. ''' 

    class Meta: 
        '''associate this form with the TaskTag model from our database. ''' 
        model = TaskTag 
        fields = ['tag'] 


## Forms for UserProfile 
class CreateUserProfileForm(forms.ModelForm): 
    '''A form to create a new UserProfile object. ''' 

    class Meta: 
        '''associate this form with the UserProfile model from our database. ''' 
        model = UserProfile 
        fields = ['first_name', 'last_name', 'profile_image_file'] 


class UpdateUserProfileForm(forms.ModelForm): 
    '''A form to update the UserProfile object. ''' 

    class Meta: 
        '''associate this form with the UserProfile model from our database. ''' 
        model = UserProfile 
        fields = ['first_name', 'last_name', 'profile_image_file'] 

