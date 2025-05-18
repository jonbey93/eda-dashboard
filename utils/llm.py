import os
from openai import OpenAI
from dash import html, dcc
from dotenv import load_dotenv
from utils.logging import write_to_log

load_dotenv()
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"),)


def query_llm(user_message,
              columns,
              data_sample):
    write_to_log(f"data_sample: {data_sample}")
    query = build_query(user_message, columns, data_sample)
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=query,
            temperature=1,
        )
        return response.choices[0].message.content
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
    The user has provided a pandas DataFrame named 'df_global'.
    
    The user will provide a message that describes an operation they want to perform on the DataFrame.
    Your task is to generate Python code that performs the operation and displays the result using plotly.

    Interpret the following request and return ONLY Python code that performs the operation and displays the result.
    Do NOT include imports of libraries, such as (pandas as pd, matplotlib.pyplot as plt, plotly.express as px).

    The code should be formatted as a single string, and it should not include any comments or explanations.

    The provided code should be a complete and valid Python code snippet use the columns labels and data structure below.

    Columns in the DataFrame:
    {columns}

    Data sample from the first row in the DataFrame:
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