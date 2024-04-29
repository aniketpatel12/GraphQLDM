# tests/test_graphqldm.py

import pytest
from gralphqldm.graphql import execute_query
from gralphqldm.constants import DEFAULT_GRAPHQL_ENDPOINT

@pytest.mark.parametrize("query, expected", [
    ("{ hello }", {"data":  {"hello": "world"}}),
    ("{ user(id: 1) { id name }}", {"data": {"user": {"id": "1", "name": "Test User"}}}),
])

def test_graphqldm_query(query, expected):
    response = execute_query(DEFAULT_GRAPHQL_ENDPOINT, {}, query)
    assert response == expected

def test_execute_query_with_invalid_endpoint():
    response = execute_query("invalid_endpoint", {}, "{ hello }")
    assert 'error' in response

def test_execute_query_with_invalid_headers_format():
    response = execute_query(DEFAULT_GRAPHQL_ENDPOINT, "invalid_headers", "{ hello }")
    assert 'error' in response

def test_execute_query_with_invalid_headers():
    response = execute_query(DEFAULT_GRAPHQL_ENDPOINT, {"Authorization" : "Bearer your_access_token"}, "{ hello }")
    assert 'error' in response

def test_execute_query_with_invalid_query():
    response = execute_query(DEFAULT_GRAPHQL_ENDPOINT, {}, "{ invalid_query }")
    assert 'error' in response