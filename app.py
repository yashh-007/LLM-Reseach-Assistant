import streamlit as st
from utils.journal_filter import search_scholar, get_quartile
import PyPDF2
from transformers import pipeline
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss

st.set_page_config(page_title="LLM Research Assistant", layout="wide")
st.title("LLM Research Assistant")

# ---------------- Journal Search ----------------
query = st.text_input("Enter your research topic:")

start_year, end_year = st.slider(
    "Select publication year range", 2000, 2025, (2020, 2025)
)

filter_q1_q2 = st.checkbox("Show only Q1/Q2 journals")
limit = st.number_input("Number of papers to fetch", min_value=1, max_value=50, value=10)

if st.button("Search Papers"):
    if not query:
        st.warning("Please enter a research topic.")
    else:
        with st.spinner("Fetching papers..."):
            papers = search_scholar(query, max_results=limit, year_range=(start_year, end_year))
            
            if filter_q1_q2:
                papers = [p for p in papers if p["quartile"] in ["Q1", "Q2"]]
            
            if papers:
                for p in papers:
                    st.markdown(f"**{p['title']}** ({p['quartile']})")
                    st.markdown(f"*Authors:* {p.get('authors','N/A')}")
                    st.markdown(f"*Journal:* {p.get('journal','N/A')}, *Year:* {p.get('year','N/A')}")
                    st.markdown(f"[Link to Paper]({p['link']})")
                    st.write("---")
            else:
                st.info("No papers found for this query.")

# ---------------- PDF Upload & Q&A ----------------
st.header("Upload a PDF to ask questions")
uploaded_file = st.file_uploader("Upload PDF", type="pdf")

if uploaded_file:
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text_chunks = []

    # Extract text and split into chunks (~500 words each)
    for page in pdf_reader.pages:
        text = page.extract_text()
        if text:
            words = text.split()
            for i in range(0, len(words), 500):
                chunk = " ".join(words[i:i+500])
                text_chunks.append(chunk)

    st.success(f"PDF loaded with {len(text_chunks)} chunks!")

    question = st.text_input("Ask a question based on the PDF:")

    if st.button("Get Answer") and question:
        with st.spinner("Generating answer..."):
            # ---------------- Embed PDF chunks ----------------
            embed_model = SentenceTransformer('all-MiniLM-L6-v2')
            chunk_embeddings = embed_model.encode(text_chunks, convert_to_numpy=True)
            
            # Build FAISS index
            dim = chunk_embeddings.shape[1]
            index = faiss.IndexFlatL2(dim)
            index.add(chunk_embeddings)
            
            # Embed the question and retrieve top 3 chunks
            q_emb = embed_model.encode([question], convert_to_numpy=True)
            D, I = index.search(q_emb, k=min(3, len(text_chunks)))
            relevant_chunks = [text_chunks[i] for i in I[0]]

            # ---------------- Hugging Face LLM ----------------
            # You can change model to any Hugging Face LLM, e.g., google/flan-t5-xl
            llm = pipeline("text2text-generation", model="google/flan-t5-large")
            context = " ".join(relevant_chunks)
            prompt = f"Answer the following question in 3-5 clear points based on this text:\n\nText: {context}\n\nQuestion: {question}\nAnswer:"

            result = llm(prompt, max_length=512, do_sample=False)
            answer = result[0]['generated_text']

            st.markdown("### Answer:")
            st.markdown(answer)
