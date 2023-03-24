import os
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .models import CarModel
# from .restapis import related methods
from . import restapis
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, get_dealer_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)

get_delaership_url = os.getenv('GET_DEALERSHIP_URL')
get_review_url = os.getenv('GET_REVIEW_URL')
save_review_url = os.getenv('SAVE_REVIEW_URL')

# Create your views here.


# Create an `about` view to render a static about page
def get_about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page
def get_contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/user_login.html', context)
    else:
        return render(request, 'djangoapp/user_login.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    context["dealership_list"] = get_dealers_from_cf(get_delaership_url)
    if request.method == "GET":
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        context = {}
        context["dealership"] = get_dealer_from_cf(get_delaership_url, dealer_id)
        context['reviews'] = get_dealer_reviews_from_cf(get_review_url, dealer_id)
        return render(request,'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    if request.method == "GET":
        context = {}
        context["dealership"] = get_dealer_from_cf(get_delaership_url, dealer_id)
        context['cars'] = CarModel.objects.filter(dealer_id=int(dealer_id)).all()
        return render(request,'djangoapp/add_review.html', context)
    if request.method == "POST" and request.user.is_authenticated:
        review_id = len(get_dealer_reviews_from_cf(get_review_url, dealer_id)) + 1
        car = CarModel.objects.get(pk=int(request.POST['car']))
        json_load = {"review" : {   "id": review_id,
                                    "name": request.user.username,
                                    "dealership": dealer_id,
                                    "review": request.POST['content'],
                                    'purchase': bool(request.POST.get('purchase',False)),
                                    'car_make': car.car_make.name,
                                    'car_model': car.name,
                                    'car_year': car.year,
                                    'purchase_date': datetime.strptime(request.POST['purchasedate'], "%Y-%m-%d").strftime("%d/%m/%y")}}
        post_request(url=save_review_url, params=None, json_load=json_load)
        return redirect("djangoapp:details", dealer_id=dealer_id)
    return redirect("djangoapp:index")

