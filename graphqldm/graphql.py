# graphqldm/graphql.py

import requests
import json

from requests.exceptions import RequestException
from graphqldm.constants import DEFAULT_GRAPHQL_ENDPOINT

class GraphQLClient:
    """ GraphQL Client to perform query or mutation """
    def __init__(self, endpoint=DEFAULT_GRAPHQL_ENDPOINT, headers=None):
        self.endpoint = endpoint
        self.headers = headers or {}
    
    def execute_query(self, query, variables):
        """ Method to execute GraphQL query """
        payload = {"query": query, "variables": variables}
        return self._execute(payload)
    
    def execute_mutation(self, mutation, variables):
        """ Method to execute graphQL mutation """
        payload = {"query": mutation, "variables": variables}
        return self._execute(payload)
    
    def _execute(self, payload):
        """ Method to execute graphQL query or mutation """
        try:
            response = requests.post(self.endpoint, json=payload, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"An error occured: " : str(e)}   