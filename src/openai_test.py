

'''
openai → lets Python communicate with the OpenAI API
python-dotenv → lets our Python code securely read the API key from .env
'''


from openai import OpenAI
from dotenv import load_dotenv


# Load environment variables from .env
load_dotenv()


# Create OpenAI client
client = OpenAI()


# Send a simple request
response = client.responses.create(
    model="gpt-5.6-luna",
    input="Explain RAG in one simple sentence."
)


print(response.output_text)