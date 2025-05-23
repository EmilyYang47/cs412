from django.shortcuts import render 
from django.http import HttpResponse 

# Create your views here.

def show_form(request):
    '''Show the web page with the form.'''

    template_name = "formdata/show_form.html"
    return render(request, template_name)

def submit(request): 
    '''Process the form submission, and generate a result. ''' 

    template_name = "formdata/confirmation.html" 
    print(request.POST) 

    # check if POST data was sent with the HTTP POST message: 
    if request.POST: 

        # extract form fields into variables: 
        name = request.POST['name'] 
        favorite_color = request.POST['favorite_color'] 

        context = {
            'name': name, 
            'favorite_color': favorite_color, 
        }



    return render(request, template_name, context = context) 