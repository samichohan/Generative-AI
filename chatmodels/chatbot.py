from dotenv import load_dotenv
load_dotenv()
import os

from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage,HumanMessage,AIMessage

model = ChatGroq(
    api_key=os.getenv('GROQ_API_KEY'),
    model_name= 'llama-3.3-70b-versatile',
    temperature= 0.8,

)
print('choose Your Ai Mode')
print('Press 1 for Angry mode')
print('Press 2 for funny mode')
print('Press 3 for Sad mode')
print('Press 4 for Normal mode')
print('Press 5 for Intelligent mode')


choice = int(input('tell your Response :-'))

if choice == 1:
    mode = 'You are an angry Ai Agent,You respond aggressively and impatiently'
elif choice == 2:
    mode = 'you are a very funny Ai Agent,you respond with humor  and jokes'

elif choice == 3:
    mode = 'you are sad Ai Agent,you respond with sad way'

elif choice == 4:
    mode = 'you are a normal Ai Agent,you respond with normal way'

elif choice == 5:
    mode = 'you are a Inteligent Ai Agent, you respond with Intelligent way'
messages = [
    SystemMessage(content=mode)
]

print('--------------- Welcome type exit to exit the application-------------------')

while True:
    prompt = input('You :')
    messages.append(HumanMessage(content=prompt))
    
    if prompt == 'exit':
        break
    
    response = model.invoke(messages)
    messages.append(AIMessage(content=response.content))
    
    print('Bot :',response.content)

print(messages)