from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_cloud_sdk_core import ApiException
from ibmcloudant.cloudant_v1 import CloudantV1
import json

import requests

def main(param_dict):
    if "selector" in param_dict.keys() and isinstance(param_dict["selector"], str):
        #selector could be get (url encoded, e.g. selector=%7B%22dealership%22%3A%2046%7D or post {"selector": {"dealership": 46}})
        param_dict["selector"] = json.loads(param_dict["selector"]);
    elif not "selector" in param_dict.keys():
        #any review
        param_dict["selector"] = {"review": {"$regex": ".*"}};
    
    try:
        authenticator = IAMAuthenticator('API_KEY')
        service = CloudantV1(authenticator=authenticator)
        service.set_service_url('URL')
        return {"reviews": service.post_find(db='reviews',  selector=param_dict["selector"]).get_result()["docs"]}
    except ApiException as cloudant_exception:
        print("unable to connect")
        return {"error": cloudant_exception}
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return {"error": err}