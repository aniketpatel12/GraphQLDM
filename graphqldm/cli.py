# graphqldm/cli.py

import json
import yaml
import typer
import logging
import os

from rich.console import Console 
from rich.table import Table 
from rich.logging import RichHandler
from graphqldm.graphql import GraphQLClient
from graphqldm.constants import DEFAULT_GRAPHQL_ENDPOINT, DEFAULT_OUTPUT_FORMAT, OUTPUT_FILE_FORMAT

app = typer.Typer()
console = Console()

FORMAT = "%(asctime)s: %(message)s"
logging.basicConfig(
    level = "INFO",
    format = FORMAT,
    datefmt = "%m/%d/%Y %I:%M %p",
    handlers = [RichHandler()]
)

logger = logging.getLogger("rich")

@app.command()
def main(
    endpoint: str = typer.Option(DEFAULT_GRAPHQL_ENDPOINT, "--endpoint", "-e" , help="GraphQL endpoint URL"),
    headers: str = typer.Option(None, "--headers", "-h", help="Optional Headers for authentication (Format: JSON)"),
    query: str = typer.Option(None,  "--query", "-q", help="GraphQL query to execute!"),
    mutation: str = typer.Option(None, "--mutation", "-m", help="GraphQL Mutation to execute!"),
    variables: str = typer.Option(None, "--variables", "-v",help="Variables to be passed with the query or mutation (Format: JSON)"),
    outputFormat: str = typer.Option(DEFAULT_OUTPUT_FORMAT, "--out", "-o", help="Output format: json/yaml/Table (Default Output Format: JSON)"),
):
    
    output = outputFormat.lower() if outputFormat else DEFAULT_OUTPUT_FORMAT

    # Validate output format
    if output not in ['table', 'json', 'yaml']:
        logger.error("Invalid output format. Please provide output format from (json, table, yaml)")
        logger.info("Please execute the 'gqldm --help' command to understand the usage!")
        raise typer.Abort()
    
    # Validate graphQL header
    if headers is not None and headers != "[]":
        try:
            headersDict = json.loads(headers)
        except json.JSONDecodeError:
            logger.error("Invalid headers format. Please provide headers in JSON format!", extra={"markup": True})
            logger.info("Please execute the 'gqldm --help' command to understand the usage!")
            raise typer.Abort()
    else:
        headersDict = {}

    # Validate graphQL variables
    if variables is not None and headers != "[]":
        try:
            variablesDict = json.loads(variables)
        except json.JSONDecodeError:
            logger.error("Invalid variables format. Please provide variables in JSON format!", extra={"markup": True})
            logger.info("Please execute the 'gqldm --help' command to understand the usage!")
            raise typer.Abort()
    else:
        variablesDict = {}

    outputFile = OUTPUT_FILE_FORMAT[output]
    currentDir = os.getcwd()
    resultDir = os.path.join(currentDir, r'results')
    if not os.path.exists(resultDir):
        os.makedirs(resultDir)

    client = GraphQLClient(endpoint, headersDict)
    
    # Validate graphQL URL endpoint
    if not endpoint.startswith("http://") and not endpoint.startswith("https://"):
        logger.error("Invalid GraphQL Endpoint URL. Please Provide a valid URL starting with 'http://' or 'https://'", extra={"markup": True})
        raise typer.Abort()

    # Execute GraphQL Query or Mutation
    if query:
        response = client.execute_query(query, variablesDict)
    elif mutation:
        response = client.execute_mutation(mutation, variablesDict) # Execute GraphQL Mutation
    else:
        logger.error("Please provide either a query or a mutation to execute!")
        logger.info("Please execute the 'gqldm --help' command to understand the usage!")
        raise typer.Abort()

    # Check for errors in the response
    if 'error' in response:
        logger.error(f"{response['error']}", extra={"markup": True})
    else:
        displayResponse(response, output)
        generateResultFile(response, resultDir, output, outputFile)


def generateResultFile(response, resultDir, outputFormat, outputFile):
    """ Method to generate the result file """

    try:
        with open(os.path.join(resultDir, outputFile), 'w') as file:
            if outputFormat == 'yaml':
                yaml.dump(response, file)
            elif outputFormat == 'table':
                for key, value in response.items():
                    file.write(f"{key}: {value}\n")
            else:
                json.dump(response, file, indent = 2)
            logger.info(f"Response saved to {outputFile}", extra={"markup": True})
    except Exception as e:
        logger.error(f"Error saving response to {outputFile}: {e}", extra={"markup": True})


def displayResponse(response, outputFormat):
    """ Method to display the generated response """

    if outputFormat == 'yaml':
        typer.echo(yaml.dump(response))
    elif outputFormat == 'table':
        table = Table(show_header=True, header_style="bold magenta")
        for key, value in response.items():
            table.add_row(str(key), str(value))
        console.print(table)
    else:
        typer.echo(response)

if __name__ == "__main__":
    app()