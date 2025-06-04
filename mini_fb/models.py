# File: models.py 
# Author: Emily Yang (eyang4@bu.edu), 5/27/2025
# Description: The models python file which defines the database. 

from django.db import models 
from django.urls import reverse 

class Profile(models.Model): 
    '''Encapsulate the data of an individual Facebook user. ''' 
    # define the data attributes of the Profile object 
    first_name = models.TextField(blank=True) 
    last_name = models.TextField(blank=True) 
    city = models.TextField(blank=True) 
    email_address = models.TextField(blank=True) 
    profile_image_url = models.URLField(blank=True) 
    published = models.DateTimeField(auto_now=True) 

    def __str__(self): 
        '''return a string representation of this instance. ''' 
        return f'{self.first_name} {self.last_name} from {self.city}, email: {self.email_address}' 
    
    def get_status_messages(self): 
        '''return all of the status messages of this profile. ''' 

        status_messages = StatusMessage.objects.filter(profile=self) 
        return status_messages 
    
    def get_absolute_url(self): 
        '''Return the URL to display one instance of this model. ''' 
        return reverse('show_profile', kwargs={'pk': self.pk}) 

    
class StatusMessage(models.Model): 
    '''Encapsulate the status message of a profile.''' 

    # data attributes of a StatusMessage: 
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE) 
    timestamp = models.DateTimeField(auto_now=True) 
    message = models.TextField(blank=False) 

    def __str__(self): 
        '''return a string representation of this instance'''
        return f'{self.message}' 
    
    def get_images(self): 
        '''return all of the status messages of this profile. ''' 
        all_status_images = StatusImage.objects.filter(status_message=self) 
        images = [] 
        for status_image in all_status_images: 
            images.append(status_image.image) 
        return images 




class Image(models.Model): 
    '''Encapsulate the idea of an image file of a profile. ''' 

    # data attributes of an Image: 
    image_file = models.ImageField(blank=False) 
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)  
    caption = models.TextField(blank=True) 
    timestamp = models.DateTimeField(auto_now=True) 

    def __str__(self): 
        '''return a string representation of this instance'''
        return f'{self.image_file} -> {self.profile}' 

class StatusImage(models.Model): 
    '''Encapsulate the status image. ''' 
    status_message = models.ForeignKey("StatusMessage", on_delete=models.CASCADE) 
    image = models.ForeignKey("Image", on_delete=models.CASCADE) 

    def __str__(self): 
        '''return a string representation of this instance'''
        return f'{self.image} -> {self.status_message}' 
    

    