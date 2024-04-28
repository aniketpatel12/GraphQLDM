# graphqldm/cli.py

import argparser
import json 

from graphqldm.graphql import execute_query
from graphqldm.constants import DEFAULT_GRAPHQL_ENDPOINT

def main():
    parser = argparser.ArgumentParser(description="Commind-Line tool for iterating with GraphQL APIs with very ease and efficiently")
    parser.add_argument("-e", "--endpoint", default=DEFAULT_GRAPHQL_ENDPOINT, help="GraphQL endpoint URL")
    parser.add_argumnet("-h", "--headers", help="Optional Headers for authentication (Format: Json)")
    parser.add_argumnet("query", help="GraphQL query to execute!")
    args = parser.parse_args()

    headers = json.loads(args.headers) if args.headers else {}
    response = execute_query(args.endpoint, headers, args.query)

    if "error" in response:
        print(f"Error occurred: {response['error']}")
    else:
        print(json.dumps(response, indent=2))

if __name__ == "__main__":
    main()