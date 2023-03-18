import os
import requests
import json
# import related models here
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

watson_api_key = os.getenv('WATSON_API_KEY')
watson_url = os.getenv('WATSON_URL')
#HTTPBasicAuth('apikey', api_key)
# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, params, headers={'Content-Type': 'application/json'}, auth=None):
    try:
        response = requests.get(url, headers=headers, params=params, auth=auth)
        return json.loads(response.text)
    except Exception as e:
        print("Exception occurred {}".format(e))
        return {"error": e}

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, params, json_load):
    try:
        response = requests.post(url, params, json_load)
        return json.loads(response.text)
    except Exception as e:
        print("Exception occurred {}".format(e))
        return {"error": e}

# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    json_result = get_request(url, params=kwargs)
    if json_result:
        dealerships = json_result
        for dealership in dealerships:
            dealer = CarDealer(id=dealership["id"], city=dealership["city"], state=dealership["state"], st=dealership["st"], 
                                   address=dealership["address"], zip=dealership["zip"], lat=dealership["lat"],
                                   long=dealership["long"], short_name=dealership["short_name"], full_name=dealership["full_name"])
            results.append(dealer)
    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(url, dealer_id):
    results = []
    json_result = get_request(url, params={"dealership": dealer_id})
    if json_result:
        reviews = json_result
        for review in reviews:
            results.append( DealerReview(id=review["id"], name=review["name"], dealership=review["dealership"], 
                                   purchase=review["purchase"], review=review["review"], purchase_date=review["purchase_date"],
                                   car_make=review["car_make"], car_model=review["car_model"], car_year=review["car_year"], sentiment=analyze_review_sentiments(review["review"])))
    return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(review):
    authenticator = IAMAuthenticator(watson_api_key)
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2023-03-18',
        authenticator=authenticator
    )
    natural_language_understanding.set_service_url(watson_url)
    return natural_language_understanding.analyze(text = review, return_analyzed_text=True, 
                                                  features = {"sentiment":{}}, language = 'en').get_result()



