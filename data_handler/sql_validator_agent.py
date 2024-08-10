from abc import ABC
from vertexai.language_models import TextGenerationModel
from vertexai.generative_models import GenerativeModel
import json

class ValidateSQLAgent(ABC):
    """
    This Chat Agent checks the SQL for validity.
    """
    agentType: str = "ValidateSQLAgent"

    def __init__(self, model_id='gemini-1.0-pro'):
        self.model_id = model_id
        if self.model_id == 'gemini-1.0-pro':
            self.model = GenerativeModel("gemini-1.0-pro-001")
        else:
            raise ValueError("Please specify a compatible model.")

    def check(self, user_question, tables_schema, columns_schema, generated_sql):
        context_prompt = f"""
            Classify the SQL query: {generated_sql} as valid or invalid?

            Guidelines to be valid:
            - all column_name in the query must exist in the table_name.
            - all join columns must be the same data_type.
            - table relationships must be correct.
            - Use fully qualified names with table_alias.column_name.

        Parameters:
        - SQL query: {generated_sql}
        - table schema: {tables_schema}
        - column description: {columns_schema}

        Respond using a valid JSON format with two elements valid and errors:
        {{ "valid": true or false, "errors": errors }}

        Initial user question:
        {user_question}
        """

        context_query = self.model.generate_content(context_prompt, stream=False)
        generated_sql = str(context_query.candidates[0].text)

        json_syntax_result = json.loads(str(generated_sql).replace("```json", "").replace("```", ""))
        return json_syntax_result
