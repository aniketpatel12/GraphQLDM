# graphqldm/cli.py

import json
import yaml
import typer

from graphqldm.graphql import GraphQLClient
from graphqldm.constants import DEFAULT_GRAPHQL_ENDPOINT, DEFAULT_OUTPUT_FORMAT

app = typer.Typer()

@app.command()
def main(
    endpoint: str = typer.Option(DEFAULT_GRAPHQL_ENDPOINT, help="GraphQL endpoint URL"),
    headers: str = typer.Option(None, help="Optional Headers for authentication (Format: JSON)"),
    query: str = typer.Option(None,  help="GraphQL query to execute!"),
    mutation: str = typer.Option(None, help="GraphQL Mutation to execute!"),
    variables: str = typer.Option(None, help="Variables to be passed with the query or mutation (Format: JSON)"),
    outputFormat: str = typer.Option(DEFAULT_OUTPUT_FORMAT, "--out", help="Default Output Format: JSON"),
):

    if headers is not None:
        try:
            headersDict = json.loads(headers)
        except json.JSONDecodeError:
            typer.echo("ERROR: Invalid headers format. Please provide headers in JSON format!")
            raise typer.Abort()
    else:
        headersDict = {}

    if variables is not None:
        try:
            variablesDict = json.loads(variables)
        except json.JSONDecodeError:
            typer.echo("ERROR: Invalid variables format. Please provide variables in JSON format!")
            raise typer.Abort()
    else:
        variablesDict = {}

    output = outputFormat.lower() if outputFormat else DEFAULT_OUTPUT_FORMAT

    client = GraphQLClient(endpoint, headersDict)

    # Validate graphQL URL endpoint
    if not endpoint.startswith("http://") and not endpoint.startswith("https://"):
        typer.echo("ERROR: Invalid GraphQL Endpoint URL. Please Provide a valid URL starting with 'http://' or 'https://'")
        raise typer.Abort()

    # Execute GraphQL Query or Mutation
    if query:
        response = client.execute_query(query, variablesDict)
    elif mutation:
        response = client.execute_mutation(mutation, variablesDict) # Execute GraphQL Mutation
    else:
        typer.echo("ERROR: Please provide either a query or a mutation to execute!")
        typer.echo("INFO: Please execute the 'gqldm --help' or 'gqldm -h' command to understand the usage!")
        raise typer.Abort()

    # Check for errors in the response
    if 'error' in response:
        typer.echo(f"ERROR: {response['error']}")
    else:
        if output == "yaml":
            typer.echo(yaml.dump(response))
        else:
            typer.echo(json.dumps(response, indent=2))


if __name__ == "__main__":
    app()