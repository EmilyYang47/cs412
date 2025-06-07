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
    
    def get_friends(self): 
        '''Return a list of the friends' Profiles of this profile. ''' 
        friend_pairs1 = Friend.objects.filter(profile1=self) 
        friend_pairs2 = Friend.objects.filter(profile2=self) 
        all_friends = [] 

        for friend_pair in friend_pairs1: 
            all_friends.append(friend_pair.profile2) 
        for friend_pair in friend_pairs2: 
            all_friends.append(friend_pair.profile1) 

        return all_friends 
    
    def add_friend(self, other): 
        '''takes a parameter other, which refers to another Profile instance, 
        and add a Friend relation for other and self. ''' 

        if self == other: 
            print("cannot add self as friend")
            return 
        elif other in self.get_friends(): 
            print("this friend pair already exist")
            return 
        else: 
            new_friend = Friend(profile1=self, profile2=other) 
            new_friend.save() 
            return 

    def get_friend_suggestions(self): 
        '''return a list of possible friends for this Profile. ''' 
        friend_seggestions = [] 
        friends = self.get_friends() 
        all_other_profiles = Profile.objects.all().exclude(pk=self.pk) 

        for profile in all_other_profiles: 
            # if profile is not in self's friend list AND if profile has 
            # at least one common friend with self, add it to the friend_seggestions 
            if profile not in friends: 
                profile_friends = profile.get_friends() 
                for profile_friend in profile_friends: 
                    if profile_friend in friends: 
                        print("FOUND COMMON FRIEND") 
                        friend_seggestions.append(profile) 
                        break 
        return friend_seggestions 
    
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
    

class Friend(models.Model): 
    '''Encapsulate the idea of an edge connecting two nodes within the social network. '''
    # data attributes of a StatusMessage: 
    profile1 = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name="profile1") 
    profile2 = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name="profile2") 
    timestamp = models.DateTimeField(auto_now=True) 

    def __str__(self): 
        '''return a string representation of this instance'''
        return f'{self.profile1.first_name} {self.profile1.last_name} & {self.profile2.first_name} {self.profile2.last_name}' 
    
        
