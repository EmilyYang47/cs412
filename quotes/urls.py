# File: urls.py
# Author: Emily Yang (eyang4@bu.edu), 5/22/2025
# Description: The urls python file which matches urls to their corresponding pages.  

from django.urls import path
from django.conf import settings
from . import views

from django.conf.urls.static import static    ## add for static files
from django.conf import settings

urlpatterns = [ 
    path(r'', views.quote_page, name="quote_page"), 
    path(r'quote/', views.quote_page, name="quote_page"), 
    path(r'show_all/', views.show_all_page, name="show_all_page"), 
    path(r'about/', views.about_page, name="about_page"), 
] 
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)