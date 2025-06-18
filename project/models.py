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
        return f'Tag: {self.tag} User: {self.user}' 
    
    


class TaskDescription(models.Model): 
    '''Encapsulate the data of an individual TaskDescription. ''' 
    task = models.TextField(blank=False) 
    tag = models.ForeignKey(TaskTag, on_delete=models.CASCADE) 
    user = models.ForeignKey(User, on_delete=models.CASCADE) 

    def __str__(self): 
        '''return a string representation of this instance. ''' 
        return f'Task: {self.task} user: {self.user}' 
    
class Timer(models.Model):  
    '''Encapsulate the data of an individual Timer. '''  
    duration = models.IntegerField(blank=False) 
    task = models.ForeignKey(TaskDescription, on_delete=models.CASCADE)  

    def __str__(self): 
        '''return a string representation of this instance. ''' 
        return f'{self.tag} {self.duration}' 
    
class UserStatus(models.Model): 
    '''Encapsulate the data of an individual UserStatus of a user. '''  
    current_number_of_snacks = models.IntegerField(blank=False) 
    current_number_of_toys = models.IntegerField(blank=False) 
    current_number_of_foods = models.IntegerField(blank=False) 
    user = models.ForeignKey(User, on_delete=models.CASCADE) 

    def __str__(self): 
        '''return a string representation of this instance. ''' 
        return f'{self.user}' 
    


class Pet(models.Model):  
    '''Encapsulate the data of an individual Pet. '''  
    image = models.ImageField(blank=False) 
    hunger_level = models.IntegerField(blank=False) 
    happiness_level = models.IntegerField(blank=False) 

    def __str__(self): 
        '''return a string representation of this instance. ''' 
        return f'{self.name}' 
    
