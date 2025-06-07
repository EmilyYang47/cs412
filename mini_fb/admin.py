# File: admin.py 
# Author: Emily Yang (eyang4@bu.edu), 5/27/2025
# Description: The admin python file which registers the models to admin. 

from django.contrib import admin 

# Register your models here.
from .models import Profile, StatusMessage, Image, StatusImage, Friend 
admin.site.register(Profile) 
admin.site.register(StatusMessage) 
admin.site.register(Image) 
admin.site.register(StatusImage) 
admin.site.register(Friend) 