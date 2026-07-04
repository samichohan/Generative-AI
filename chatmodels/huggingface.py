from dotenv import load_dotenv
load_dotenv()
import os

from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint

llm = HuggingFaceEndpoint(
    repo_id="deepseek-ai/DeepSeek-R1",  
    huggingfacehub_api_token=os.getenv('HUGGINGFACEHUB_ACCESS_TOKEN') 
)

model = ChatHuggingFace(llm=llm)

response = model.invoke('what is stranger things?')
print(response.content)