import requests
import json
# import related models here
from requests.auth import HTTPBasicAuth
from rest_framework import status
from rest_framework.response import Response

watson_api_key = os.getenv['WATSON_API_KEY']
watson_url = os.getenv['WATSON_URL']
#HTTPBasicAuth('apikey', api_key)
# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, params=params, headers={'Content-Type': 'application/json'}, auth=None):
    try:
        response = requests.get(url, headers=headers, params=params, auth=auth)
    except Exception as e:
        print("Exception occurred {}".format(e))
        return Response({error: e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
    
    status_code = response.status_code
    return Response(json.loads(response.text), status=response.status_code)

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, params=kwargs, json=payload):
    try:
        response = requests.post(url, params=kwargs, json=json)
        return Response(json.loads(response.text), status=response.status_code)
    except Exception as e:
        print("Exception occurred {}".format(e))
        return Response({error: e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR

# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    json_result = get_request(url, params=kwargs)
    if json_result:
        dealers = json_result
        for dealership in dealerships:
            dealer = CarDealer(id=dealership["id"], state=dealership["state"], st=dealership["st"], 
                                   address=dealership["address"], zip=dealership["zip"], lat=dealership["lat"],
                                   long=dealership["long"], short_name=dealership["short_name"], full_name=dealership["full_name"])
            results.append(dealer)
    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(url, dealerId):
    results = []
    json_result = get_request(url, params={dealership: dealerId})
    if json_result:
        reviews = json_result
        for review in reviews:
            id, name, dealership, purchase, review, purchase_date, car_make, car_model, car_year, sentiment
            results.append( DealerReview(id=reviews["id"], state=name["name"], dealership=reviews["dealership"], 
                                   purchase=reviews["purchase"], review=reviews["review"], purchase_date=reviews["purchase_date"],
                                   car_make=reviews["car_make"], car_model=reviews["car_model"], car_year=reviews["car_year"], analyze_review_sentiments(reviews["review"]))
            results.append(dealer)
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



