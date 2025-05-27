# File: models.py 
# Author: Emily Yang (eyang4@bu.edu), 5/27/2025
# Description: The models python file which defines the database. 

from django.db import models

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