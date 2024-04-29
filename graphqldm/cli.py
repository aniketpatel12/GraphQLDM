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
    
    # Validate graphQL URL endpoint
    if not args.endpoint.startwith("http://") and not args.endpoint.startwith("https://"):
        print("Error: Invalid GraphQL Endpoint URL. Please Provide a valid URL starting with 'http://' or 'https://'")
        return 
    
    # Validate headers format
    if args.headers:
        try: 
            headers = json.loads(args.headers)
            if not isinstance(headers, dict):
                raise ValueError
        except ValueError:
            print("Error: Invalid headers format. Please provide headers in JSON format!")
            return

    else:
        headers = {}


    # Execute GraphQL Query
    response = execute_query(args.endpoint, headers, args.headers)

    # Check for errors in the response
    if 'error' in response:
        print(f"Error occurred: {response['error']}")
    else:
        print(json.dumps(response, indent=2))


if __name__ == "__main__":
    main()