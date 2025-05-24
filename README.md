<mark>setup project structures for first example/assignment</mark>
change into development directory
'cd django' 
start virtual environment
'pipenv shell'
# start a new project:
django-admin startproject cs412 .  ## note the trailing dot ##

# run the server to check that everything works!
python manage.py runserver
# stop the server with CONTROL-C 

# create a new app:
python manage.py startapp hw 

## cs412/settings.py: ## add "hw" to list of INSTALLED_APPS
INSTALLED_APPS = [
	"hw", # new app
]

## cs412/urls.py: ## add include, 'hw' path to urls file
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("hw/", include("hw.urls")),
]

## create file: hw/urls.py

from django.urls import path
from django.conf import settings
from . import views

urlpatterns = [ 
    path(r'', views.home, name="home"),
]

## modify hw/views.py 
## create template/hw to store all html files 
## create directory static/styles.css 
## modify settings.py 

