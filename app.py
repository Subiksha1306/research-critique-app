import streamlit as st
import fitz  # PyMuPDF
import os
from dotenv import load_dotenv
from groq import Groq

# Load Groq API Key
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

# Groq Client
client = Groq(api_key=groq_api_key)

# Function to extract text from PDF
def extract_text_from_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# Function to generate critique
def generate_critique(text):
    prompt = f"""
You are an expert academic reviewer. Read the following research paper and provide a detailed critique, including:
1. Strengths
2. Weaknesses
3. Suggestions for Improvement
4. Originality and relevance
Paper:
{text}
"""
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama3-70b-8192"
    )
    return response.choices[0].message.content

# Streamlit UI
st.title("PaperScope")
uploaded_file = st.file_uploader("Upload your research paper (.pdf)", type="pdf")

if uploaded_file:
    st.success("PDF uploaded successfully!")
    if st.button("Generate Critique"):
        with st.spinner("Reading and analyzing the paper..."):
            text = extract_text_from_pdf(uploaded_file)
            critique = generate_critique(text)
        st.subheader("📄 Generated Critique:")
        st.write(critique)
