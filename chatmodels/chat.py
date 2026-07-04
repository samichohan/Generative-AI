
from dotenv import load_dotenv
load_dotenv()

import os
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

model = ChatGroq(
    api_key=os.getenv('GROQ_API_KEY'),
    model_name='llama-3.3-70b-versatile',
    temperature=0.8,
    max_tokens=1000
    )

response = model.invoke([HumanMessage(content='what is machine learning')])

print(response.content)


