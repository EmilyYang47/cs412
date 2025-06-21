from django import forms
from .models import *  

## Forms for Task Description  
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


## Forms for Timer 
class CreateTimerForm(forms.ModelForm): 
    '''A form to create the task description. ''' 

    class Meta: 
        '''associate this form with the Timer model from our database. ''' 
        model = Timer 
        fields = ['duration', 'task'] 


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