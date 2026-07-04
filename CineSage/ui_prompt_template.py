import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

# Load environment variables
load_dotenv()

# ---------------- UI CONFIG ----------------
st.set_page_config(
    page_title="Info Extraction Engine",
    page_icon="🧠",
    layout="centered"
)

st.title("🧠 Information Extraction & Summarization Engine")
st.write("Paste your text below and get structured AI-powered extraction.")

# ---------------- PROMPT ----------------
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
Write a concise 3–5 sentence summary.
"""),
    ("human", "Extract all structured information from the following text:\n\n{text}")
])

# ---------------- MODEL ----------------
model = ChatGroq(model="llama-3.3-70b-versatile")

# ---------------- INPUT ----------------
text = st.text_area(
    "📄 Enter your text here:",
    height=250,
    placeholder="Paste movie, series, article or any paragraph..."
)

# ---------------- BUTTON ----------------
if st.button("🚀 Extract Information"):
    if text.strip() == "":
        st.warning("Please enter some text first.")
    else:
        with st.spinner("Analyzing text..."):
            final_prompt = prompt.invoke({"text": text})
            response = model.invoke(final_prompt)

        st.success("Extraction Completed!")

        st.subheader("📊 Extracted Output")
        st.markdown(response.content)

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("Built with Streamlit + LangChain + Groq 🚀")