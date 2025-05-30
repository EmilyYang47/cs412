# File: admin.py 
# Author: Emily Yang (eyang4@bu.edu), 5/27/2025
# Description: The admin python file which registers the Profile model to admin. 

from django.contrib import admin 

# Register your models here.
from .models import Profile, StatusMessage
admin.site.register(Profile) 
admin.site.register(StatusMessage) 