from data_handler.bigquery_connector import BQConnector
from data_handler.embedder_agent import EmbedderAgent
from data_handler.sql_builder_agent import BuildSQLAgent
from data_handler.sql_debugger_agent import DebugSQLAgent
from data_handler.sql_validator_agent import ValidateSQLAgent
from data_handler.response_agent import ResponseAgent
from config.settings import PROJECT_ID, BQ_REGION, BQ_OPENDATAQNA_DATASET_NAME, BQ_DATASET_NAME, DATA_SOURCE
import asyncio
import os

# Set the environment variable for Google Cloud credentials securely
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path_to_your_credentials.json"  # Replace with the correct path

async def main():
    user_question = "who had the most revenue?"
    EXAMPLES = True  # Set to True or False dependig on whether you have a good_known_sql.csv file
    
    # Initialize the BigQuery connector
    connector = BQConnector(PROJECT_ID, BQ_REGION, BQ_DATASET_NAME, BQ_OPENDATAQNA_DATASET_NAME)

    # Generate SQL response using the defined objects and parameters
    resp, sql, audit_text = await generate_sql_response(
        user_question, PROJECT_ID, BQ_REGION, BQ_OPENDATAQNA_DATASET_NAME, DATA_SOURCE, connector, EXAMPLES
    )

    # Print the results
    print(f"Response: {resp}")
    print(f"Generated SQL: {sql}")
    print(f"Audit Text: {audit_text}")

# Run the main function
asyncio.run(main())
