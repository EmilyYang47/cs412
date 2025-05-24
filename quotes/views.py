# File: views.py
# Author: Emily Yang (eyang4@bu.edu), 5/22/2025
# Description: The views python file which creates the views to handle each page request.   

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

import random 

# the images of Marie Curie 
IMAGES = ["https://upload.wikimedia.org/wikipedia/commons/c/c8/Marie_Curie_c._1920s.jpg", 
          "https://upload.wikimedia.org/wikipedia/commons/9/93/Marie_Curie_1903.jpg", 
          "https://upload.wikimedia.org/wikipedia/commons/3/3d/Marie_Curie_-_Mobile_X-Ray-Unit.jpg", 
          "https://upload.wikimedia.org/wikipedia/commons/a/aa/Irene_and_Marie_Curie_1925.jpg" 
        ] 
# the quotes of Marie Curie 
QUOTES = ["Nothing in life is to be feared, it is only to be understood", 
          "Have no fear of perfection - you'll never reach it", 
          "Be less curious about people and more curious about ideas" 
        ] 

def quote_page(request):
    '''
    Define a view to handle the 'quote' request.
    '''
    template_name = "quotes/quote.html"
    context = { 
        "image": random.choice(IMAGES), 
        "quote": random.choice(QUOTES), 
    }
    return render(request, template_name, context) 

def show_all_page(request):
    '''
    Define a view to handle the 'show_all' request.
    '''
    template_name = "quotes/show_all.html"
    context = { 
        "quotes": QUOTES, 
        "images": IMAGES, 

    }
    return render(request, template_name, context) 

def about_page(request):
    '''
    Define a view to handle the 'about' request.
    '''
    template_name = "quotes/about.html"
    return render(request, template_name) 
