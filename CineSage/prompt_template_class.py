from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile",
    temperature=0.5,
)

prompt = ChatPromptTemplate.from_messages([   
    # system role
    ("system",
"""You are an expert text summarizer.

Your job is to summarize the given text clearly and concisely.

Follow these rules:
- Always capture the MAIN idea
- Remove unnecessary details
- Never add your own opinion
"""),

    # human role
    ("human",
"""Please summarize the following text:

{text}
""")
])

# chain  ----> pipeline(prompt -> llm -> StrOutputParser)
# StrOutputParser() is used to extract just model output text from the full response
chain = prompt | llm | StrOutputParser()

# user input
print("\n========== Text Summarizer ==========\n")

text = input("Enter the text to summarize:\n> ")


print("\n========== Summary ==========\n")

# chain invoke
result = chain.invoke({
    "text": text
})

print(result)
print("\n=====================================")