from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system",
"""
You are a professional information extraction and summarization engine.

Analyze the provided text and extract all meaningful information.

Rules:
- Extract only information explicitly present in the text.
- Do not invent missing details.
- If information is not available, write "Not Mentioned".
- Preserve exact names as written.
- Keep output structured and clean.
- Do not add explanations outside the format.

Output Format (strictly follow this):

IDENTIFICATION
- Title:
- Alternate Names:
- Content Type:

CREATIVE DETAILS
- Genres:
- Creator(s):
- Director(s):
- Producer(s):
- Writer(s):

RELEASE INFORMATION
- Release Date:
- Release Year:
- Platform / Network:
- Country:

CHARACTERS & PEOPLE
- Main Characters:
- Supporting Characters:
- Cast Members:
- Real People Mentioned:

CONTENT DETAILS
- Plot Summary:
- Themes:
- Tone / Mood:
- Setting:
- Time Period:

ENTITIES
- Organizations:
- Companies:
- Locations:
- Important Dates:

ANALYSIS
- Key Highlights:
- Notable Features:
- Popularity / Reception:
- Keywords:

FINAL SUMMARY:
Write a concise 3–5 sentence summary covering:
what it is, creator, release info, main story, and significance.

"""),

    ("human",
"""
Extract all structured information from the following text:

{text}
""")
])

text = input("Give your text :")
final_prompt = prompt.invoke(
    {"text": text}
)

model = ChatGroq(
    model = 'llama-3.3-70b-versatile'

)

response = model.invoke(final_prompt)
print(response.content)