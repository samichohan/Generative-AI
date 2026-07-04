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
- Length should be {length} (short = 2-3 lines, medium = 5-6 lines, detailed = 10+ lines)
- Tone should be {tone} (formal / simple / bullet points)
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

print("\n--- Settings ---")
length   = input("Length (short / medium / detailed) [default: medium]: ").strip() or "medium"
tone     = input("Tone (formal / simple / bullet points) [default: bullet points]: ").strip() or "bullet points"

print("\n========== Summary ==========\n")

# chain invoke
result = chain.invoke({
    "length": length,
    "tone": tone,
    "text": text
})

print(result)
print("\n=====================================")