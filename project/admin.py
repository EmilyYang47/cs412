# File: admin.py 
# Author: Emily Yang (eyang4@bu.edu), 6/17/2025
# Description: The admin python file which registers the models to admin. 

from django.contrib import admin 

# Register your models here.
from .models import TaskTag, Timer, TaskDescription, UserProfile, Pet 
admin.site.register(TaskTag) 
admin.site.register(Timer) 
admin.site.register(TaskDescription) 
admin.site.register(UserProfile) 
admin.site.register(Pet) 