import json
import requests

def call_api_get(url, access_token, return_raw=True):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    if return_raw:
        return response
    else:
        # Check the response status
        if response.status_code == 200:
            return json.dumps(response.json(), indent=4)
        else:
            return "{}: {} {}".format("Error", response.status_code, response.text)

def call_api_post(url, data, access_token, return_raw=True):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if return_raw:
        return response
    else:
        # Check the response status
        if response.status_code == 201:
            return json.dumps(response.json(), indent=4)
        else:
            return "{}: {} {}".format("Error", response.status_code, response.text)

def call_api_delete(url, access_token, return_raw=True):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    response = requests.delete(url, headers=headers)
    if return_raw:
        return response
    else:
        # Check the response status
        if response.status_code == 204:
            return response
        else:
            return "{}: {} {}".format("Error", response.status_code, response.text)
