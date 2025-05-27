from django.db import models

# Create your models here.
# In the models.py file, create a model called Profile, 
# which will model the data attributes of individual Facebook users.

# This Profile model will need to include the following data attributes: 
# first name, 
# last name, 
# city, 
# email address, 
# and a profile image url.

# Use the Django admin to create 5 sample profiles, 
# with names/data of your choosing. You do NOT need to reproduce the exact data from the example above. 

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