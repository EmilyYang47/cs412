# File: forms.py
# Author: Emily Yang (eyang4@bu.edu), 5/29/2025
# Description: The forms python file which creates the forms to add new model objects to the database.   

from django import forms
from .models import Profile, StatusMessage 

class CreateProfileForm(forms.ModelForm): 
    '''A form to add an Profile to the database. ''' 

    class Meta: 
        '''associate this form with a model from our database. ''' 
        model = Profile 
        fields = ['first_name', 'last_name', 'city', 'email_address', 'profile_image_url'] 
        

class CreateStatusMessageForm(forms.ModelForm): 
    '''A form to add a status message to the database. ''' 

    class Meta: 
        '''associate this form with a model from our database. ''' 
        model = StatusMessage 
        fields = ['message'] 
