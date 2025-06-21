# File: models.py 
# Author: Emily Yang (eyang4@bu.edu), 6/17/2025
# Description: The models python file which defines the database. 

from django.db import models 
from django.urls import reverse 
from django.contrib.auth.models import User 

class TaskTag(models.Model): 
    '''Encapsulate the data of an individual TaskTag. ''' 
    tag = models.TextField(blank=False) 
    time_spent = models.IntegerField(blank=False) 
    user = models.ForeignKey(User, on_delete=models.CASCADE) 

    def __str__(self): 
        '''return a string representation of this instance. ''' 
        return f'Tag: {self.tag}' 


class TaskDescription(models.Model): 
    '''Encapsulate the data of an individual TaskDescription. ''' 
    task = models.TextField(blank=False) 
    tag = models.ForeignKey(TaskTag, on_delete=models.CASCADE) 
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    is_complete = models.BooleanField(blank=False) 
    due_time = models.DateTimeField(blank=True, null=True)  

    def __str__(self): 
        '''return a string representation of this instance. ''' 
        return f'Task: {self.task} user: {self.user}' 
    

class Timer(models.Model):  
    '''Encapsulate the data of an individual Timer. '''  
    duration = models.IntegerField(blank=False) 
    task = models.ForeignKey(TaskDescription, on_delete=models.CASCADE)  
    timestamp = models.DateTimeField(auto_now=True) 
    user = models.ForeignKey(User, on_delete=models.CASCADE) 

    def __str__(self): 
        '''return a string representation of this instance. ''' 
        return f'{self.task} {self.duration}' 

    
class UserProfile(models.Model): 
    '''Encapsulate the data of an individual Profile of a user. '''  
    first_name = models.TextField(blank=True) 
    last_name = models.TextField(blank=True) 
    profile_image_file = models.ImageField(blank=True)     

    current_number_of_snacks = models.IntegerField(blank=False) 
    user = models.ForeignKey(User, on_delete=models.CASCADE) 

    def __str__(self): 
        '''return a string representation of this instance. ''' 
        return f'{self.first_name} {self.last_name}' 
    
    def get_absolute_url(self): 
        '''Return the URL to display one instance of this model. ''' 
        return reverse('profile', kwargs={'pk': self.pk}) 
    
    
    def get_all_pets(self): 
        '''return all of the pets of this profile. ''' 
        pets = Pet.objects.filter(profile=self) 
        return pets 


class Pet(models.Model):  
    '''Encapsulate the data of an individual Pet. '''  
    image_url = models.URLField(blank=False) 
    name = models.TextField(blank=True) 
    affection_level = models.IntegerField(blank=False) 
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE) 

    def __str__(self): 
        '''return a string representation of this instance. ''' 
        return f'{self.name}' 
    
