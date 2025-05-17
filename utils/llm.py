import openai
from dash import html, dcc
from dotenv import load_dotenv

load_dotenv()
#client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"),)

def query_llm(user_input):
    response = None
    return response