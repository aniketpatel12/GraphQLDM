# tests/test_graphql_query.py

import pytest 
from graphqldm.graphql import GraphQLClient
from graphqldm.constants import DEFAULT_GRAPHQL_ENDPOINT

@pytest.mark.parametrize("mutation, expected", [
    ("mutation { updateUser(id: 1, name: \"testUser\") { id name } }", {"data": {"updateUser": {"id": "1", "name": "testUser"}}}),
    ("mutation { deleteUser(id: 1) { id } }", {"data": {"deleteUser": {"id": "1"}}}),
])

def test_graphqldm_mutation(mutation, expected):
    client = GraphQLClient(DEFAULT_GRAPHQL_ENDPOINT, {})  # Create a new instance for each test case
    response = client.execute_mutation(mutation)
    assert response == expected

def test_execute_mutation_with_invalid_endpoint():  
    client = GraphQLClient(DEFAULT_GRAPHQL_ENDPOINT, {})
    response = client.execute_mutation("mutation { updateUser(id: 1, name: \"testUser\") { id name }}")

def test_execute_mutation_with_invalid_headers_format():
    client = GraphQLClient(DEFAULT_GRAPHQL_ENDPOINT, "invalid_headers")
    response = client.execute_mutation("mutation { updateUser(id: 1, name: \"testUser\") { id name } }")
    assert 'error' in response

def test_execute_mutation_with_invalid_headers():
    client = GraphQLClient(DEFAULT_GRAPHQL_ENDPOINT, {"Authorization": "Bearer your_access_token"})
    response = client.execute_mutation("mutation { updateUser(id: 1, name: \"testUser\") { id name } }")
    assert 'error' in response

def test_execute_mutation_with_invalid_mutation():
    client = GraphQLClient(DEFAULT_GRAPHQL_ENDPOINT, {})
    response = client.execute_mutation("mutation { invalidMutation(id: 1) { id } }")
    assert 'error' in response