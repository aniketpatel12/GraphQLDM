# graphqldm/graphql.py

import requests
import json

from requests.exceptions import RequestException

class GraphQLClient:
    def __init__(self, endpoint="", headers=None):
        self.endpoint = endpoint
        self.headers = headers or {}
    
    def execute_query(self, query):
        payload = {"query" : query}
        try:
            response = requests.post(self.endpoint, json=payload, headers=self.headers)
            response.raise_for_status()  # Raise an exception for non-2xx status codes  
            return response.json()
        except RequestException as e:
            return {"Error": {e}}