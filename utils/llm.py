import os
from openai import OpenAI
from dash import html, dcc
from dotenv import load_dotenv
from utils.logging import write_to_log

client = None
openai_connect = False

def setup_llm_client():
    global client
    global openai_connect
    load_dotenv()
    api_key = os.environ.get("OPENAI_API_KEY")
    write_to_log(f"OpenAI API Key: {api_key}")
    openai_connect = False
    client = None
    if not api_key:
        return
    try:
        client = OpenAI(api_key=api_key)
        client.models.list()
        openai_connect = True
    except Exception as e:
        write_to_log(f"Failed to connect to OpenAI: {e}")
        openai_connect = False

def is_openai_connected():
    return openai_connect

def clean_llm_code(response: str) -> str:
    response = response.strip()

    # If starts and ends with triple quotes
    if response.startswith('"""') and response.endswith('"""'):
        response = response[3:-3].strip()

    # If markdown formatted
    if response.startswith("```") and response.endswith("```"):
        response = "\n".join(line for line in response.splitlines()[1:-1])

    return response

def query_llm(user_message, columns, data_sample):
    query = build_query(user_message, columns, data_sample)
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=query,
            temperature=1,
        )
        code = clean_llm_code(response.choices[0].message.content)
        write_to_log(f"LLM_CODE, {code}")
        write_to_log(f"DATA SAMPLE, {data_sample}")
        return code
    except Exception as e:
        return "(error)" + str(e)

def build_query_DEBUG(user_message, columns, data_sample):
    priming = f"""
    Columns in the DataFrame:
    {columns}
    """

    prompt = f"""
    Please tell me what columns you see above.
    """

    query = [
        {"role": "system", "content": priming},
        {"role": "user", "content": prompt}
    ]
    return query

def build_query(user_message, columns, data_sample):
    priming = f"""
    You are a Python programming assistant.
    The user has provided a pandas DataFrame named 'df_global' You can assume that it has been completely cleaned.
    
    The user will provide a message that describes an operation they want to perform on the DataFrame.
    Your task is to generate Python code that performs the operation and displays.
    ALWAYS use plotly.express or plotly.graph_objects. NEVER use iplot() or cufflinks.
    The resulting figure varible should always be named 'fig'. Do NOT include fig.show() in the code.

    Interpret the following request and return ONLY Python code that performs the operation and displays the result.
    Do NOT include import statements in the beginning.

    The code should be formatted as a Python multi-line string.
    Do NOT include any comments or explanations.

    Columns in the df_global DataFrame:
    {columns}

    Data sample from the first row with dtypes:
    {data_sample}
    """

    prompt = f"""
    User request:
    {user_message}
    """
    
    query = [
        {"role": "system", "content": priming},
        {"role": "user", "content": prompt}
    ]
    return query