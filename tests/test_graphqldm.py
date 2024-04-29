# tests/test_graphqldm.py

import pytest
from gralphqldm.graphql import execute_query
from gralphqldm.constants import DEFAULT_GRAPHQL_ENDPOINT

@pytest.mark.parametrize("query, expected", [
    ("{hello}", {"data":  {"hello": "world"}}),
])

def test_graphqldm_query(query, expected):
    response = execute_query(DEFAULT_GRAPHQL_ENDPOINT, {}, query)
    assert response == expected
