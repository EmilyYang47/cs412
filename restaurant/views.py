# File: views.py
# Author: Emily Yang (eyang4@bu.edu), 5/24/2025
# Description: The views python file which creates the views to handle each page request.   

from django.shortcuts import render 
from django.http import HttpResponse 

import time 
import random 

# the list of dictionaries of all possible daily specials 
DAILY_SPECIALS = [{'name': 'Smashed Chilies with Century Eggs', 
                    'image': 'https://thewoksoflife.com/wp-content/uploads/2022/09/roasted-peppers-pidan-13.jpg',  
                    'price': 17.00 
                    }, 
                    {'name': 'Spicy Sichuan Wontons', 
                    'image': 'https://www.seriouseats.com/thmb/w3JZBTeUtfnq_ZV3XpD8Nuy98mk=/750x0/filters:no_upscale():max_bytes(150000):strip_icc():format(webp)/__opt__aboutcom__coeus__resources__content_migration__serious_eats__seriouseats.com__recipes__images__2015__03__20150310-sichuan-wonton-chili-oil-recipe-new-1-b5d267569a64453984160aaa919fe5fc.jpg', 
                    'price': 13.00 
                    }, 
                    {'name': 'Baby Cabbage with Garlic and Vermicelli', 
                    'image': 'https://5b0988e595225.cdn.sohucs.com/images/20200327/a115a1f5bea244628d1c3cfc5504139f.jpeg', 
                    'price': 12.00 
                    }                       
                ] 

def main(request): 
    '''Define a view to handle the 'main' request. ''' 

    template_name = "restaurant/main.html" 
    return render(request, template_name) 

def order(request):
    '''Define a view to handle the 'order' request. ''' 

    template_name = "restaurant/order.html" 
    daily_special = random.choice(DAILY_SPECIALS) 

    context = {
        'daily_special_name': daily_special['name'],  
        'daily_special_image': daily_special['image'], 
        'daily_special_price': daily_special['price'], 
        } 
    return render(request, template_name, context) 

def confirmation(request): 
    '''Process the order form submission, and generate a result. ''' 

    template_name = "restaurant/confirmation.html" 
    print(request.POST) 

    # check if POST data was sent with the HTTP POST message: 
    if request.POST: 

        # the dictionary that maps input names to thei dish name 
        dishes = { 
            'Daily Special': 'daily_special', 

            'Mala Dry Pot': 'dry_pot', 
            '- Extra Vegetales': 'dry_pot_vege', 
            '- Extra Potatoes': 'dry_pot_potato', 
            '- Extra Beef': 'dry_pot_beef', 
            '- Extra Lamb': 'dry_pot_lamb', 
            '- Extra Shrimp': 'dry_pot_shrimp', 

            'Sichuan Cold Noodle': 'cold_noodle',
            'Chili and Cumin Flavored Dried Lamb': 'lamb',
            'Dan Dan Noodles': 'dan_dan_noodles',
            'Di San Xian': 'di_san_xian',
            'Tomato Egg Stir Fry': 'stir_fry',
            'Mapo Tofu': 'tofu',
        } 

        # the dictionary that maps dish names and their prices  
        prices = {
            'Mala Dry Pot': 18.00, 
            '- Extra Vegetales': 1.25, 
            '- Extra Potatoes': 1.25, 
            '- Extra Beef': 1.50, 
            '- Extra Lamb': 1.50, 
            '- Extra Shrimp': 1.75, 

            'Sichuan Cold Noodle': 9.00,
            'Chili and Cumin Flavored Dried Lamb': 20.00,
            'Dan Dan Noodles': 12.00,
            'Di San Xian': 15.00,
            'Tomato Egg Stir Fry': 15.00,
            'Mapo Tofu': 17.00, 
        } 

        # Get daily special info from POST 
        daily_special_name = request.POST.get('daily_special_name')
        daily_special_price = float(request.POST.get('daily_special_price', 0.0)) 

        # determine the ordered dishes and calculate the total_price: 
        total_price = 0 
        selected_dishes = [] 
        dry_pot_ordered = False 
        dry_pot_options = ['dry_pot_vege', 'dry_pot_potato', 'dry_pot_beef', 'dry_pot_lamb', 'dry_pot_shrimp'] 

        for name, key in dishes.items():  
            if key in request.POST: 
                if key == 'daily_special': 
                    selected_dishes.append(daily_special_name) 
                    total_price += daily_special_price 
                else:  
                    if key == 'dry_pot': 
                        dry_pot_ordered = True 
                    elif (key in dry_pot_options) and not dry_pot_ordered: 
                        selected_dishes.append('Mala Dry Pot') 
                        total_price += 18.00 
                        dry_pot_ordered = True 
                    selected_dishes.append(name) 
                    total_price += prices[name]  

        # extract form fields into variables for the special instructions and user contact info: 
        special_instructions = request.POST['instructions'] 
        name = request.POST['name'] 
        phone = request.POST['phone'] 
        email = request.POST['email'] 

        # calculate the time at which the order will be ready 
        # current_time_list is in format [weekday, month, date, hr:min:sec, year] 
        current_time_list = time.ctime().split()
        current_date = int(current_time_list[2]) 
        current_hour = int(current_time_list[3].split(':')[0])  
        current_minute = int(current_time_list[3].split(':')[1])  
        prepare_munite = random.randint(30, 60)          

        minute = (current_minute + prepare_munite) % 60 
        hour = current_hour + (current_minute + prepare_munite) // 60 
        date = current_date 
        if hour >= 24: 
            date += 1 
            hour = hour % 24   

        ready_time = current_time_list[0] + " " + current_time_list[1] + " " + str(date) + " " + str(hour) + ":" + str(minute) + ":" + current_time_list[3].split(':')[-1] + " " + current_time_list[-1]    

        # the context variable   
        context = {
            'selected_dishes':selected_dishes, 
            'total_price': total_price, 
            'ready_time': ready_time, 
            'name': name, 
            'phone': phone, 
            'email': email,  
            'special_instructions': special_instructions, 
            } 
        

    print(selected_dishes, total_price)
    return render(request, template_name, context = context) 