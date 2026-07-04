
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel
from typing import List, Optional
from langchain_core.output_parsers import PydanticOutputParser

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="Movie Information Extractor",
    page_icon="🎬",
    layout="wide"
)

# ---------------- STYLING ---------------- #

st.markdown("""
<style>
.main-title{
    text-align:center;
    font-size:42px;
    font-weight:bold;
    color:#ff4b4b;
}

.subtitle{
    text-align:center;
    color:gray;
    margin-bottom:25px;
}

.result-card{
    padding:15px;
    border-radius:10px;
    background-color:#f5f5f5;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='main-title'>🎬 Movie Information Extractor</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Powered by LangChain + Groq + Pydantic</div>", unsafe_allow_html=True)

# ---------------- LOAD ENV ---------------- #

load_dotenv()

# ---------------- PYDANTIC MODEL ---------------- #

class Movie(BaseModel):
    title: str
    release_year: Optional[int]
    genre: List[str]
    director: Optional[str]
    cast: List[str]
    rating: Optional[float]
    summary: str

parser = PydanticOutputParser(pydantic_object=Movie)

# ---------------- PROMPT ---------------- #

prompt = ChatPromptTemplate.from_messages([
    ("system",
     """
Extract movie information from the paragraph.

{format_instructions}
"""),
    ("human", "{text}")
])

# ---------------- INPUT ---------------- #

text = st.text_area(
    "Paste Movie Paragraph",
    height=250,
    placeholder="Paste a movie description here..."
)

# ---------------- BUTTON ---------------- #

if st.button("🚀 Extract Information", use_container_width=True):

    if not text.strip():
        st.warning("Please enter some text.")
        st.stop()

    with st.spinner("Analyzing Movie Information..."):

        final_prompt = prompt.invoke(
            {
                "text": text,
                "format_instructions": parser.get_format_instructions()
            }
        )

        model = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0
        )

        response = model.invoke(final_prompt)

        movie_data = parser.parse(response.content)

    st.success("Extraction Complete!")

    # ---------------- DISPLAY ---------------- #

    col1, col2 = st.columns(2)

    with col1:
        st.metric("🎬 Title", movie_data.title)

        st.metric(
            "📅 Release Year",
            movie_data.release_year
            if movie_data.release_year
            else "N/A"
        )

        st.metric(
            "⭐ Rating",
            movie_data.rating
            if movie_data.rating
            else "N/A"
        )

    with col2:
        st.write("### 🎭 Director")
        st.info(movie_data.director or "Not Mentioned")

        st.write("### 🎬 Genres")
        st.write(", ".join(movie_data.genre))

    st.divider()

    st.write("### 👥 Cast")
    st.write(movie_data.cast)

    st.divider()

    st.write("### 📝 Summary")
    st.success(movie_data.summary)

    st.divider()

    st.write("### 📦 Raw JSON")

    st.json(movie_data.model_dump())

