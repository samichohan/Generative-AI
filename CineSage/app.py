import streamlit as st
from prompt import prompt
from model import load_model

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Information Extractor",
    page_icon="🧠",
    layout="centered"
)

# ---------------- HEADER ----------------
st.title("🧠 AI Information Extraction Engine")
st.write("Paste any text (movie, news, article, company, etc.) and get structured insights instantly.")

# ---------------- INPUT ----------------
text = st.text_area(
    "📄 Enter your text",
    height=250,
    placeholder="Paste your paragraph here..."
)

# ---------------- MODEL ----------------
model = load_model()

# ---------------- BUTTON ----------------
if st.button("🚀 Extract Information"):

    if text.strip() == "":
        st.warning("Please enter some text.")
    else:
        with st.spinner("Analyzing text..."):

            final_prompt = prompt.invoke({"text": text})
            response = model.invoke(final_prompt)

        st.success("Done!")

        # ---------------- OUTPUT ----------------
        st.subheader("📊 Extracted Information")

        st.markdown(response.content)

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("Built with LangChain + Groq + Streamlit 🚀")