from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage,AIMessage,HumanMessage

import os
from dotenv import load_dotenv
load_dotenv()

llm = ChatGroq(
    api_key=os.getenv('GROQ_API_KEY'),
    model_name = 'llama-3.3-70b-versatile',
    temperature= 0.8
)


# System prompt 
# prompt=input("You: ")
# response = llm.invoke(prompt)

# # ans of llm in response
# print("Bot: ",response.content)


print('----------------------AI-Bot-----------------------------')
print("     Type 'exit' To quit The Chat            ")

# function to make a loop of the chat , until user input is exit
while True:
    prompt = input('You: ')
    if prompt == 'exit':
        break
    response = llm.invoke(prompt)
    print("Bot: ",response.content)