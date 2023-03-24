from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_cloud_sdk_core import ApiException
from ibmcloudant.cloudant_v1 import CloudantV1
import json
import requests

def main(param_dict):
    if "review" in param_dict.keys() and isinstance(param_dict["review"], str):
        #selector could be get (url encoded, e.g. review=%7B%22review%22%3A%20%7B%22dealership%22%3A%2046,%20%22id%22%3A%207,%20%22name%22%3A%20%22San%20Jay%22,%20%22purchase%22%3A%20false,%20%22review%22%3A%20%22Are%20I%20am%20not%20kidding,%20best%22%7D%7D
        #              or post {"review": {"dealership": 46, "id": 7, "name": "San Jay", "purchase": false, "review": "Are I am not kidding, best"}}
        param_dict["review"] = json.loads(param_dict["review"]);
    elif not "review" in param_dict.keys():
       return {"error":"Review is not provided"}
    
    try:
        authenticator = IAMAuthenticator('API_KEY')
        service = CloudantV1(authenticator=authenticator)
        service.set_service_url('URL')
        return {"reviews": service.post_document(db='reviews',  document=param_dict["review"]).get_result()}
    except ApiException as cloudant_exception:
        return {"error": cloudant_exception}
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        return {"error": err}