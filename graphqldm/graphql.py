# graphqldm/graphql.py

import requests
import json

from requests.exceptions import RequestException
from graphqldm.constants import DEFAULT_GRAPHQL_ENDPOINT

class GraphQLClient:
    def __init__(self, endpoint=DEFAULT_GRAPHQL_ENDPOINT, headers=None):
        self.endpoint = endpoint
        self.headers = headers or {}
    
    def execute_query(self, query, variables):
        payload = {"query": query, "variables": variables}
        return self._execute(payload)
    
    def execute_mutation(self, mutation, variables):
        payload = {"query": mutation, "variables": variables}
        return self._execute(payload)
    
    def _execute(self, payload):
        try:
            response = requests.post(self.endpoint, json=payload, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except RequestException as e:
            return {"Error" : str(e)}   