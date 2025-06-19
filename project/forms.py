from django import forms
from .models import *  

class UpdateTaskDescriptionForm(forms.ModelForm): 
    '''A form to update the task description. ''' 

    class Meta: 
        '''associate this form with the TaskDescription model from our database. ''' 
        model = TaskDescription 
        fields = ['task', 'tag', 'is_complete', 'due_time'] 


class CreateTaskDescriptionForm(forms.ModelForm): 
    '''A form to create the task description. ''' 

    class Meta: 
        '''associate this form with the TaskDescription model from our database. ''' 
        model = TaskDescription 
        fields = ['task', 'tag', 'due_time'] 


class CreateTimerForm(forms.ModelForm): 
    '''A form to create the task description. ''' 

    class Meta: 
        '''associate this form with the Timer model from our database. ''' 
        model = Timer 
        fields = ['duration', 'task'] 