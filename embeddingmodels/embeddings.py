from langchain_cohere import CohereEmbeddings
from dotenv import load_dotenv
load_dotenv()
import os


embedding_model = CohereEmbeddings(
    cohere_api_key=os.getenv('COHERE_API_KEY'),
    model="embed-english-v3.0"
)

text = 'You are going to learn Gen Ai'

result = embedding_model.embed_query(text)


print("Embedding bani!")
print(f"Numbers ki length: {len(result)}")
print(f"Pehle 5 numbers: {result[:5]}")
