from abc import ABC
from vertexai.language_models import TextGenerationModel
from vertexai.generative_models import GenerativeModel

class ResponseAgent(ABC):
    """
    A specialized Chat Agent designed to provide natural language responses to user questions based on SQL query results.
    """
    agentType: str = "ResponseAgent"

    def __init__(self, model_id='gemini-1.0-pro'):
        self.model_id = model_id
        if self.model_id == 'gemini-1.0-pro':
            self.model = GenerativeModel("gemini-1.0-pro-001")
        else:
            raise ValueError("Please specify a compatible model.")

    def run(self, user_question, sql_result):
        context_prompt = f"""
            You are a Data Assistant that helps to answer users' questions on their data within their databases.
            The user has provided the following question in natural language: "{str(user_question)}"

            The system has returned the following result after running the SQL query: "{str(sql_result)}".

            Provide a natural sounding response to the user to answer the question with the SQL result provided to you.
        """

        context_query = self.model.generate_content(context_prompt, stream=False)
        generated_sql = str(context_query.candidates[0].text)
        return generated_sql
