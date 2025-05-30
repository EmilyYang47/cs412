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
        