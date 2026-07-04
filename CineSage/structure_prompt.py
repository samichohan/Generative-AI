from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel
from typing import List, Optional
from langchain_core.output_parsers import PydanticOutputParser


class Movie(BaseModel):
    title: str
    release_year: Optional[int]
    genre: List[str]
    director: Optional[str]
    cast: List[str]
    rating: Optional[float]
    summary: str

parser = PydanticOutputParser(pydantic_object=Movie)

prompt = ChatPromptTemplate.from_messages([
    ("system","""
Extract Movie information from the paragraph
     {format_instructions}
"""),
("human","{text}")
])

text = input("Give your text :")
final_prompt = prompt.invoke(
    {"text": text,
     "format_instructions": parser.get_format_instructions()
     }

)

model = ChatGroq(
    model = 'llama-3.3-70b-versatile'

)

response = model.invoke(final_prompt)

# movie_data = parser.parse(response.content)
print(response.content)