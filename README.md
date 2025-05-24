<mark>setup project structures for first example/assignment</mark> 

change into development directory <br />
`cd django` 

start virtual environment <br /> 
`pipenv shell`

start a new project: <br /> 
`django-admin startproject cs412 .`  ## note the trailing dot ##

run the server to check that everything works! <br />
`python manage.py runserver` 

stop the server with CONTROL-C	

create a new app: <br />
`python manage.py startapp hw` 

cs412/settings.py: ## add "hw" to list of INSTALLED_APPS <br />
```INSTALLED_APPS = [ <br />
	"hw", # new app <br />
]```

cs412/urls.py: ## add include, 'hw' path to urls file <br />
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

