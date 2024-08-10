from abc import ABC
from vertexai.language_models import TextGenerationModel, CodeGenerationModel
from vertexai.generative_models import GenerativeModel, GenerationConfig

class BuildSQLAgent(ABC):
    """
    This Agent produces the SQL query.
    """
    agentType: str = "BuildSQLAgent"

    def __init__(self, model_id: str):
        self.model_id = model_id
        if model_id == 'code-bison-32k':
            self.model = CodeGenerationModel.from_pretrained('code-bison-32k')
        elif model_id == 'text-bison-32k':
            self.model = TextGenerationModel.from_pretrained('text-bison-32k')
        elif model_id == 'gemini-1.0-pro' or model_id == 'gemini-1.5-pro':
            self.model = GenerativeModel("gemini-1.0-pro-001")
        else:
            raise ValueError("Please specify a compatible model.")

    def build_sql(self, source_type, user_question, tables_schema, tables_detailed_schema, similar_sql, max_output_tokens=2048, temperature=0.4, top_p=1, top_k=32):
        context_prompt = f"""
            You are a BigQuery SQL guru. Write a SQL-compliant query for BigQuery that answers the following question while using the provided context to correctly refer to the BigQuery tables and the needed column names.

            Guidelines:
            - Join as few tables as possible.
            - When joining tables, ensure all join columns are the same data type.
            - Analyze the database and the table schema provided as parameters and understand the relations (column and table relations).
            - Always use SAFE_CAST.
            - Generate the SQL in a single line.
            - Use fully qualified names with ticks (`project_id.owner.table_name`).
            - Use the column names mentioned in Table Schema.
            - Use SQL 'AS' statement to assign a new name temporarily to a table column or even a table wherever needed.
            - Table names are case-sensitive.
            - Refer to the examples provided: {similar_sql}

        Here are some examples of user questions and SQL queries:
        {similar_sql}

        question:
        {user_question}

        Table Schema:
        {tables_schema}

        Column Description:
        {tables_detailed_schema}
        """

        if 'gemini' in self.model_id:
            config = GenerationConfig(
                max_output_tokens=max_output_tokens, temperature=temperature, top_p=top_p, top_k=top_k
            )
            context_query = self.model.generate_content(context_prompt, generation_config=config, stream=False)
            generated_sql = str(context_query.candidates[0].text)
        else:
            context_query = self.model.predict(context_prompt, max_output_tokens=max_output_tokens, temperature=temperature)
            generated_sql = str(context_query.candidates[0])

        return generated_sql
