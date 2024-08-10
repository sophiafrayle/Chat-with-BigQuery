# Chat with BigQuery (SQL)

## Overview

This project is a data processing and natural language understanding tool that integrates with Google Cloud services such as BigQuery and Vertex AI. The tool allows users to generate SQL queries based on natural language input, validate these queries, and provide human-readable responses. It also includes debugging and validation mechanisms to ensure the SQL queries are syntactically and semantically correct.

## Features

- **Natural Language to SQL Conversion**: Convert user questions in natural language into SQL queries that can be executed on BigQuery.
- **SQL Validation**: Validate the generated SQL queries for correctness and adherence to schema definitions.
- **SQL Debugging**: Automatically debug SQL queries by identifying and fixing errors based on BigQuery feedback.
- **Natural Language Responses**: Generate natural language responses from the results of SQL queries, providing easy-to-understand answers to users' questions.
- **Modular Design**: The project is structured into reusable components, making it easy to extend and maintain.

## Project Structure

```plaintext
my_project/
│
├── data_handler/
│   ├── __init__.py
│   ├── bigquery_connector.py
│   ├── embedder_agent.py
│   ├── sql_builder_agent.py
│   ├── sql_debugger_agent.py
│   ├── sql_validator_agent.py
│   ├── response_agent.py
│   └── utils.py
│
├── main.py
│
├── config/
│   ├── __init__.py
│   └── settings.py
│
├── credentials/
│   └── credentials.json  # Ensure this is in .gitignore
│
├── .gitignore
├── README.md
└── requirements.txt
```

### Directory and File Descriptions

- **`data_handler/`**: Contains all the core classes and functions used for data processing, SQL generation, validation, and response generation.
  - `bigquery_connector.py`: Contains the `BQConnector` class for interacting with BigQuery.
  - `embedder_agent.py`: Contains the `EmbedderAgent` class for generating text embeddings using Vertex AI.
  - `sql_builder_agent.py`: Contains the `BuildSQLAgent` class for generating SQL queries from natural language input.
  - `sql_debugger_agent.py`: Contains the `DebugSQLAgent` class for debugging SQL queries.
  - `sql_validator_agent.py`: Contains the `ValidateSQLAgent` class for validating SQL queries.
  - `response_agent.py`: Contains the `ResponseAgent` class for generating natural language responses from SQL results.
  - `utils.py`: Contains utility functions used across the project.

- **`config/`**: Stores configuration settings.
  - `settings.py`: Contains configurable settings such as project IDs, dataset names, and regions.

- **`main.py`**: The entry point of the application. It initializes the necessary components and runs the data processing pipeline.

- **`credentials/`**: Directory to store Google Cloud credentials (ensure this is included in `.gitignore`).

- **`.gitignore`**: Specifies files and directories to be ignored by Git, such as credentials and temporary files.

- **`requirements.txt`**: Lists the Python dependencies required to run the project.

- **`README.md`**: Provides documentation and instructions for the project.

## Installation

### Prerequisites

- Python 3.8 or higher
- A Google Cloud account with BigQuery and Vertex AI enabled
- Google Cloud SDK installed and authenticated

### Steps

1. **Clone the repository**:

   ```bash
   git clone https://github.com/your_username/your_repository.git
   cd your_repository
   ```

2. **Set up a virtual environment** (optional but recommended):

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up Google Cloud credentials**:

   - Download your service account key file from Google Cloud Console.
   - Save the key file as `credentials.json` in the `credentials/` directory.
   - Ensure that the `credentials/` directory is added to your `.gitignore` file to prevent sensitive information from being uploaded to version control.

5. **Configure project settings**:

   - Update the `config/settings.py` file with your Google Cloud project ID, BigQuery dataset names, and region.

   ```python
   PROJECT_ID = "your_project_id"
   BQ_REGION = "your_region"
   BQ_OPENDATAQNA_DATASET_NAME = "your_opendataqna_dataset_name"
   BQ_DATASET_NAME = "your_bq_dataset_name"
   ```

## Usage

### Running the Application

To run the application, simply execute the `main.py` file:

```bash
python main.py
```

The application will:

1. Initialize the necessary components (e.g., BigQuery connector, agents).
2. Generate a SQL query based on the provided user question.
3. Validate and debug the SQL query.
4. Execute the SQL query on BigQuery and retrieve the results.
5. Generate a natural language response from the SQL results and output it.

### Example Output

```plaintext
Response: The top 3 drivers in points for season 10 are...
Generated SQL: SELECT driver_name, points FROM ...
Audit Text: User Question: who are the top 3 drivers in points of season 10? ...
```

## Configuration

All configuration options are located in `config/settings.py`. This includes settings such as:

- **Project ID**: The Google Cloud project ID to use.
- **Region**: The BigQuery region.
- **Dataset Names**: The BigQuery datasets to query.
- **EXAMPLES**: If you have examples of known good sql queries, create a csv file as such as: 
prompt | sql | database_name [3 columns]

prompt ==> User Question

sql ==> SQL for the user question (Note that the sql should enclosed in quotes and only in single line. Please remove the line break)

database_name ==>This name should exactly match the SCHEMA NAME for Postgres Source or BQ_DATASET_NAME

Save it as known_good_sql.csv, update the path on the df_kqg variable and set EXAMPLES variable as True, otherwise set it as False and it will create them from scratch.

### Environment Variables

Set the environment variable for Google Cloud credentials before running the application:

```bash
export GOOGLE_APPLICATION_CREDENTIALS="path/to/credentials.json"
```

On Windows:

```cmd
set GOOGLE_APPLICATION_CREDENTIALS=path\to\credentials.json
```

## Troubleshooting

- **Credential Issues**: Ensure that the `GOOGLE_APPLICATION_CREDENTIALS` environment variable is set correctly and points to the correct service account key file.
- **BigQuery Errors**: Check the BigQuery console for any syntax or execution errors related to the generated SQL queries.
- **Dependency Issues**: Ensure that all dependencies are installed by running `pip install -r requirements.txt`.

## Extending the Project

This project is designed with modularity in mind, making it easy to extend. Here are some ideas:

- **Add More Agents**: Implement additional agents for tasks such as data preprocessing or result visualization.
- **Support More Data Sources**: Extend the project to support other databases or data sources beyond BigQuery.
- **Improve Debugging**: Enhance the debugging agent to handle more complex SQL errors or add more sophisticated validation rules.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes. Make sure to include tests for any new features or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For questions or support, please contact [your_email@example.com](mailto:your_email@example.com).
```

### Key Sections Explained

- **Overview**: Provides a high-level view of what the project does and its key features.
- **Features**: Highlights the core functionality of the project.
- **Project Structure**: Gives users an understanding of how the project is organized.
- **Installation**: Step-by-step instructions for setting up the project on a local machine.
- **Usage**: Describes how to run the application and provides an example of what to expect.
- **Configuration**: Explains where to find and how to modify configuration settings.
- **Troubleshooting**: Common issues and their solutions.
- **Extending the Project**: Suggestions for how to add new features or capabilities.
- **Contributing**: Guidelines for contributing to the project.
- **License**: The project's licensing information.
- **Contact**: How to get in touch with the project maintainers.

This detailed `README.md` will serve as a comprehensive guide for anyone looking to use, understand, or contribute to your project.
