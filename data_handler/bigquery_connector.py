from google.cloud import bigquery
import google.auth
import pandas as pd
from google.cloud.exceptions import NotFound
from abc import ABC

class BQConnector(ABC):
    """
    Instantiates a BigQuery Connector.
    """
    connectorType: str = "Base"

    def __init__(self, project_id: str, region: str, dataset_name: str, opendataqna_dataset: str):
        # Initialize the connector with project details and create a BigQuery client
        self.project_id = project_id
        self.region = region
        self.dataset_name = dataset_name
        self.opendataqna_dataset = opendataqna_dataset
        self.client = self.getconn()

    def getconn(self):
        client = bigquery.Client(project=self.project_id)
        return client

    def retrieve_df(self, query):
        return self.client.query_and_wait(query).to_dataframe()

    def retrieve_matches(self, mode, schema, qe, similarity_threshold, limit):
        matches = []

        if mode == 'table':
            sql = '''select base.content as tables_content from vector_search(TABLE `{}.table_details_embeddings`, "embedding",
            (SELECT {} as qe), top_k=> {},distance_type=>"COSINE") where 1-distance > {} '''

        elif mode == 'column':
            sql = '''select base.content as columns_content from vector_search(TABLE `{}.tablecolumn_details_embeddings`, "embedding",
            (SELECT {} as qe), top_k=> {}, distance_type=>"COSINE") where 1-distance > {} '''

        elif mode == 'example':
            sql = '''select base.example_user_question, base.example_generated_sql from vector_search ( TABLE `{}.example_prompt_sql_embeddings`, "embedding",
            (select {} as qe), top_k=> {}, distance_type=>"COSINE") where 1-distance > {} '''

        else:
            ValueError("No valid mode. Must be either table, column, or example")
            name_txt = ''

        results = self.client.query_and_wait(
            sql.format('{}.{}'.format(self.project_id, self.opendataqna_dataset), qe, limit, similarity_threshold)
        ).to_dataframe()

        if len(results) == 0:
            print("Did not find any results. Adjust the query parameters.")

        if mode == 'table':
            name_txt = ''
            for _, r in results.iterrows():
                name_txt = name_txt + r["tables_content"] + "\n"

        elif mode == 'column':
            name_txt = ''
            for _, r in results.iterrows():
                name_txt = name_txt + r["columns_content"] + "\n"

        elif mode == 'example':
            name_txt = ''
            for _, r in results.iterrows():
                example_user_question = r["example_user_question"]
                example_sql = r["example_generated_sql"]
                name_txt = name_txt + "\n Example_question: " + example_user_question + "; Example_SQL: " + example_sql

        matches.append(name_txt)

        return matches

    def getSimilarMatches(self, mode, schema, qe, num_matches, similarity_threshold):
        match_result = self.retrieve_matches(mode, schema, qe, similarity_threshold, num_matches)
        return match_result[0]

    def getExactMatches(self, query):
        check_history_sql = f"""SELECT example_user_question,example_generated_sql FROM {self.project_id}.{self.opendataqna_dataset}.example_prompt_sql_embeddings
                          WHERE lower(example_user_question) = lower('{query}') LIMIT 1; """

        exact_sql_history = self.client.query_and_wait(check_history_sql).to_dataframe()

        if exact_sql_history[exact_sql_history.columns[0]].count() != 0:
            sql_example_txt = ''
            exact_sql = ''
            for index, row in exact_sql_history.iterrows():
                example_user_question = row["example_user_question"]
                example_sql = row["example_generated_sql"]
                exact_sql = example_sql
                sql_example_txt = sql_example_txt + "\n Example_question: " + example_user_question + "; Example_SQL: " + example_sql

            print("Found a matching question from the history!" + str(sql_example_txt))
            final_sql = exact_sql

        else:
            print("No exact match found for the user prompt")
            final_sql = None

        return final_sql

    def test_sql_plan_execution(self, generated_sql):
        try:
            job_config = bigquery.QueryJobConfig(dry_run=True, use_query_cache=False)
            query_job = self.client.query(generated_sql, job_config=job_config)
            exec_result_df = ("This query will process {} bytes.".format(query_job.total_bytes_processed))
            correct_sql = True
            print(exec_result_df)
            return correct_sql, exec_result_df
        except Exception as e:
            return False, str(e)
