# graphqldm/cli.py

import argparse
import json
import logging

from graphqldm.graphql import GraphQLClient
from graphqldm.constants import DEFAULT_GRAPHQL_ENDPOINT

def main():
    parser = argparse.ArgumentParser(description="Commind-Line tool for iterating with GraphQL APIs with very ease and efficiently")
    parser.add_argument("-E", "--endpoint", default=DEFAULT_GRAPHQL_ENDPOINT, help="GraphQL endpoint URL")
    parser.add_argument("-H", "--headers", help="Optional Headers for authentication (Format: JSON)")
    parser.add_argument("-Q", "--query", help="GraphQL query to execute!")
    parser.add_argument("-M", "--mutation", help="GraphQL Mutation to execute!")
    parser.add_argument("--variables", help="Variables to be passed with the query or mutation (Format: JSON)")
    args = parser.parse_args()

    # Setup logger
    logger = logging.getLogger(__name__)
    logging.basicConfig(format='%(levelname)s - %(asctime)s - %(message)s')

    headers = json.loads(args.headers) if args.headers else {}
    variables = json.loads(args.variables) if args.variables else {}
    
    client = GraphQLClient(args.endpoint, headers)
    
    # Validate graphQL URL endpoint
    if not args.endpoint.startswith("http://") and not args.endpoint.startswith("https://"):
        logger.error("Invalid GraphQL Endpoint URL. Please Provide a valid URL starting with 'http://' or 'https://'")
        return 
    
    # Validate headers format
    if args.headers:
        try: 
            headers = json.loads(args.headers)
            if not isinstance(headers, dict):
                raise ValueError
        except ValueError:
            logger.error("Invalid headers format. Please provide headers in JSON format!")
            return
    else:
        headers = {}

    
    # Validate variables format
    if args.variables:
        try:
            variables = json.loads(args.variables)
            if not isinstance(variables, dict):
                raise ValueError
        except ValueError as e:
            logger.error("Invalid variables format. Please provide variables in JSON Format!")
            return
    else:
        variables = {}

    # Execute GraphQL Query
    if args.query:
        response = client.execute_query(args.endpoint, headers, args.query, variables)
    elif args.mutation:
        response = client.execute_mutation(args.endpoint, headers, args.mutation, variables) # Execute GraphQL Mutation
    else:
        logger.error("Please provide either a query or a mutation to execute!")
        return

    # Check for errors in the response
    if 'error' in response:
        logger.error(f"{response['error']}")   
    else:
        logger.info(json.dumps(response, indent=2))

if __name__ == "__main__":
    main()