from utils.llm import query_llm

# Test the query_llm function
prompt = "I havent uploaded any data yet. Can you show me a line plot of the x and y columns?"
response = query_llm(prompt)
print("Prompt:", prompt)
print("Response:", response)