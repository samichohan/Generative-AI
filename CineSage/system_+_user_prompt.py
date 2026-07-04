from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage,AIMessage,HumanMessage

import os
from dotenv import load_dotenv
load_dotenv()


#model setup 
llm = ChatGroq(
    api_key=os.getenv('GROQ_API_KEY'),
    model_name = 'llama-3.3-70b-versatile',
    temperature=0.8
)


# list to safe chat history
messages = [

    #Chatbot role 
    SystemMessage(content='you are a history teacher.')
]


print("------------------ Ai Bot ------------------")
print("       Type 'exit' to quit the chat         ")

# function to make a loop of the chat , until user input is exit
while True:
    prompt = input('You: ')
    messages.append(HumanMessage(content=prompt))
    if prompt == 'exit':
        break

    #response = llm.invoke(prompt)
    response = llm.invoke(messages)
    messages.append(AIMessage(content=response.content))
    print("Bot: ",response.content)
print(messages)