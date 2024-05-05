# graphqldm/cli.py

import json
import yaml
import typer
import logging

from rich.console import Console 
from rich.table import Table 
from rich.logging import RichHandler
from graphqldm.graphql import GraphQLClient
from graphqldm.constants import DEFAULT_GRAPHQL_ENDPOINT, DEFAULT_OUTPUT_FORMAT

app = typer.Typer()
console = Console()

FORMAT = "%(message)s"
logging.basicConfig(
    level = "NOTSET",
    format = FORMAT,
    datefmt = "[%X]",
    handlers = [RichHandler(rich_tracebacks=True)]
)

logger = logging.getLogger("rich")

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
            logger.error("[bold red]ERROR:[/] Invalid headers format. Please provide headers in JSON format!", extra={"markup": True})
            raise typer.Abort()
    else:
        headersDict = {}

    if variables is not None:
        try:
            variablesDict = json.loads(variables)
        except json.JSONDecodeError:
            logger.error("[bold red]ERROR:[/] Invalid variables format. Please provide variables in JSON format!", extra={"markup": True})
            raise typer.Abort()
    else:
        variablesDict = {}

    output = outputFormat.lower() if outputFormat else DEFAULT_OUTPUT_FORMAT

    client = GraphQLClient(endpoint, headersDict)

    # Validate graphQL URL endpoint
    if not endpoint.startswith("http://") and not endpoint.startswith("https://"):
        logger.error("[bold red]ERROR:[/] Invalid GraphQL Endpoint URL. Please Provide a valid URL starting with 'http://' or 'https://'", extra={"markup": True})
        raise typer.Abort()

    # Execute GraphQL Query or Mutation
    if query:
        response = client.execute_query(query, variablesDict)
    elif mutation:
        response = client.execute_mutation(mutation, variablesDict) # Execute GraphQL Mutation
    else:
        logger.error("[bold red]ERROR:[/] Please provide either a query or a mutation to execute!", extra={"markup": True})
        logger.info("[bold green blink]INFO:[/] Please execute the 'gqldm --help' or 'gqldm -h' command to understand the usage!", extra={"markup": True})
        raise typer.Abort()

    # Check for errors in the response
    if 'error' in response:
        logger.error(f"[bold red]ERROR:[/] {response['error']}", extra={"markup": True})
    else:
        if output == "yaml":
            typer.echo(yaml.dump(response))
        else:
            table = Table(show_header=True, header_style="bold magenta")
            for key, value in response.items():
                table.add_row(str(key), str(value))
            console.print(table)

if __name__ == "__main__":
    app()