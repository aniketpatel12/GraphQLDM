# tests/test_graphqldm.py

import pytest
from graphqldm.graphql import GraphQLClient
from graphqldm.constants import DEFAULT_GRAPHQL_ENDPOINT

client = GraphQLClient(args.endpoint, headers)

@pytest.mark.parametrize("query, expected", [
    ("{ hello }", {"data":  {"hello": "world"}}),
    ("{ user(id: 1) { id name }}", {"data": {"user": {"id": "1", "name": "Test User"}}}),
])

def test_graphqldm_query(query, expected):
    response = client.execute_query(DEFAULT_GRAPHQL_ENDPOINT, {}, query)
    assert response == expected

def test_execute_query_with_invalid_endpoint():
    response = client.execute_query("invalid_endpoint", {}, "{ hello }")
    assert 'error' in response

def test_execute_query_with_invalid_headers_format():
    response = client.execute_query(DEFAULT_GRAPHQL_ENDPOINT, "invalid_headers", "{ hello }")
    assert 'error' in response

def test_execute_query_with_invalid_headers():
    response = client.execute_query(DEFAULT_GRAPHQL_ENDPOINT, {"Authorization" : "Bearer your_access_token"}, "{ hello }")
    assert 'error' in response

def test_execute_query_with_invalid_query():
    response = client.execute_query(DEFAULT_GRAPHQL_ENDPOINT, {}, "{ invalid_query }")
    assert 'error' in response