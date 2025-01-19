import json
import requests
from utils.config import OPENAI_API_KEY, AI_MODEL
from utils.database_functions import ask_postgres_database, postgres_connection
from tenacity import retry, wait_exponential, stop_after_attempt
import os


@retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=4, max=10))
def send_api_request_to_openai_api(messages, functions=None, function_call=None, model=AI_MODEL, openai_api_key=OPENAI_API_KEY):
    """ Send the API request to the OpenAI API via Chat Completions endpoint """
    try:
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}"}
        json_data = {"model": "gpt-3.5-turbo-16k", "messages": messages}
        if functions: 
            json_data.update({"functions": functions})
        if function_call: 
            json_data.update({"function_call": function_call})
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=json_data)
        response.raise_for_status()

        return response.json()
    
    except requests.RequestException as e:
        raise ConnectionError(f"Failed to connect to OpenAI API due to: {e}")


def execute_function_call(message):
    """ Run the function call provided by OpenAI's API response """
    if message["function_call"]["name"] == "ask_postgres_database":
        query = json.loads(message["function_call"]["arguments"])["query"]
        print(f"SQL query: {query} \n")
        results = ask_postgres_database(postgres_connection, query)
        print(f"Results A: {results} \n")
    else:
        results = f"Error: function {message['function_call']['name']} does not exist"
    return results

