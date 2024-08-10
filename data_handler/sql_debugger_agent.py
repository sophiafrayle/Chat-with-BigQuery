from abc import ABC
from vertexai.language_models import CodeChatModel
from vertexai.generative_models import GenerativeModel

class DebugSQLAgent(ABC):
    """
    This Chat Agent runs the debugging loop.
    """
    agentType: str = "DebugSQLAgent"

    def __init__(self, chat_model_id='gemini-1.0-pro'):
        self.chat_model_id = chat_model_id

    def init_chat(self, tables_schema, tables_detailed_schema, sql_example="-No examples provided..-"):
        context_prompt = f"""
        You are a BigQuery SQL guru. This session is troubleshooting a BigQuery SQL query. As the user provides versions of the query and the errors returned by BigQuery,
        return a new alternative SQL query that fixes the errors.

        Guidelines:
        - Join as few tables as possible.
        - Ensure all join columns are the same data type.
        - Use SAFE_CAST.
        - Generate the SQL in a single line.
        - Use fully qualified names with ticks (`project_id.owner.table_name`).
        - Table names are case-sensitive.
        - Refer to the examples provided: {sql_example}

        Parameters:
        - Table metadata: {tables_schema}
        - Column metadata: {tables_detailed_schema}
        - SQL example: {sql_example}
        """

        if self.chat_model_id == 'codechat-bison-32k':
            chat_model = CodeChatModel.from_pretrained("codechat-bison-32k")
            chat_session = chat_model.start_chat(context=context_prompt)
        elif self.chat_model_id == 'gemini-1.0-pro':
            chat_model = GenerativeModel("gemini-1.0-pro-001")
            chat_session = chat_model.start_chat(response_validation=False)
            chat_session.send_message(context_prompt)
        elif self.chat_model_id == 'gemini-ultra':
            chat_model = GenerativeModel("gemini-1.0-ultra-001")
            chat_session = chat_model.start_chat(response_validation=False)
            chat_session.send_message(context_prompt)
        else:
            raise ValueError('Invalid chat_model_id')

        return chat_session

    def rewrite_sql_chat(self, chat_session, question, error_df):
        context_prompt = f"""
            What is an alternative SQL statement to address the error mentioned below?

            Original SQL:
            {question}

            Error:
            {error_df}
            """

        if self.chat_model_id == 'codechat-bison-32k':
            response = chat_session.send_message(context_prompt)
            resp_return = (str(response.candidates[0])).replace("```sql", "").replace("```", "")
        elif self.chat_model_id == 'gemini-1.0-pro':
            response = chat_session.send_message(context_prompt, stream=False)
            resp_return = (str(response.text)).replace("```sql", "").replace("```", "")
        elif self.chat_model_id == 'gemini-ultra':
            response = chat_session.send_message(context_prompt, stream=False)
            resp_return = (str(response.text)).replace("```sql", "").replace("```", "")
        else:
            raise ValueError('Invalid chat_model_id')

        return resp_return

    def start_debugger(self, source_type, query, user_question, SQLChecker, tables_schema, tables_detailed_schema, AUDIT_TEXT, similar_sql="-No examples provided..-", DEBUGGING_ROUNDS=2, LLM_VALIDATION=True):
        i = 0
        STOP = False
        invalid_response = False
        chat_session = self.init_chat(tables_schema, tables_detailed_schema, similar_sql)
        sql = query.replace("```sql", "").replace("```", "").replace("EXPLAIN ANALYZE ", "")

        AUDIT_TEXT = AUDIT_TEXT + "\n\nEntering the debugging steps!"
        while not STOP:

            if LLM_VALIDATION:
                json_syntax_result = SQLChecker.check(user_question, tables_schema, tables_detailed_schema, sql)
            else:
                json_syntax_result['valid'] = True

            if json_syntax_result['valid'] is True:
                correct_sql, exec_result_df = connector.test_sql_plan_execution(sql)
                if not correct_sql:
                    AUDIT_TEXT = AUDIT_TEXT + "\nGenerated SQL failed on execution!"
                    rewrite_result = self.rewrite_sql_chat(chat_session, sql, exec_result_df)
                    sql = str(rewrite_result).replace("```sql", "").replace("```", "").replace("EXPLAIN ANALYZE ", "")
                else:
                    STOP = True
            else:
                syntax_err_df = pd.read_json(json.dumps(json_syntax_result))
                rewrite_result = self.rewrite_sql_chat(chat_session, sql, syntax_err_df)
                sql = str(rewrite_result).replace("```sql", "").replace("```", "").replace("EXPLAIN ANALYZE ", "")

            i += 1
            if i > DEBUGGING_ROUNDS:
                AUDIT_TEXT = AUDIT_TEXT + "Exceeded the number of iterations for correction!"
                STOP = True
                invalid_response = True

        return sql, invalid_response, AUDIT_TEXT
