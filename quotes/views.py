from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import time
import random

# Create your views here.

QUOTES = [
    "I hate a lot of things, and I don't particularly like anything.",
    "I'm going to restore my clan and kill a certain someone.",
    "My dreams are not of the future. My dreams are of the past.",
    "It's too late Naruto, it's already too late."
]

IMAGES = [
    "https://cs-people.bu.edu/grace25/quotes_images/image1.png",
    "https://cs-people.bu.edu/grace25/quotes_images/image2.png",
    "https://cs-people.bu.edu/grace25/quotes_images/image3.png",
    "https://cs-people.bu.edu/grace25/quotes_images/image4.png"
]

# Index Page
def home(request):
    template_name = "quotes/home.html"

    selected_quote = random.choice(QUOTES)
    selected_image = random.choice(IMAGES)

    context = {
        'quote': selected_quote,
        'image': selected_image,
        'person': "Uchiha Sasuke"
    }

    return render(request, template_name, context)

# Quotes Page

def quote(request):
    template_name = "quotes/quote.html"

    selected_quote = random.choice(QUOTES)
    selected_image = random.choice(IMAGES)

    context = {
        'quote': selected_quote,
        'image': selected_image,
        'person': "Uchiha Sasuke"
    }

    return render(request, template_name, context)

# Show all page
def show_all(request):
    context = {
        'quotes': QUOTES,
        'images': IMAGES,
        'person': "Uchiha Sasuke"
    }

    return render(request, 'quotes/show_all.html', context)

# About Page
def about(request):
    # Information about Sasuke Uchiha and the app creator
    person_info = {
        'name': "Uchiha Sasuke",
        'bio': "Sasuke Uchiha is one of the last surviving members of Konohagakure's Uchiha clan. After his brother Itachi slaughtered their clan, Sasuke made it his life mission to avenge them and restore his clan's honor.",
    }
    creator_info = {
        'bio': "My name is Grace, and I am a senior studying Psychology and Computer Science at Boston University. I created this web application to display quotes from notable characters."
    }

    context = {
        'person_info': person_info,
        'creator_info': creator_info
    }
    
    return render(request, 'quote/about.html', context)