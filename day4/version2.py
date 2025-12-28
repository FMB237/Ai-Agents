#This is a more advanced version of the ai_document_reader.py
#In this version user will be able to download summarized AI analysis

#Now let's import our modules
import streamlit as st
import faiss
import numpy as np
import pypdf
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import OllamaLLM
from langchain_text_splitters import CharacterTextSplitter

#-------------------------------------------------
# Import our AI model
#-------------------------------------------------
llm = OllamaLLM(model="qwen2.5:3b")

#-------------------------------------------------
# Load Hugging face Embeddings
# all-MiniLM-L6-v2 => 384 dimensions
#-------------------------------------------------
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

#-------------------------------------------------
# SESSION STATE INITIALIZATION
# Prevents Streamlit rerun bugs
#-------------------------------------------------
if "faiss_index" not in st.session_state:
    st.session_state.faiss_index = faiss.IndexFlatL2(384)

if "vector_store" not in st.session_state:
    st.session_state.vector_store = []  #To store text chunks & metadata

if "summary_text" not in st.session_state:
    st.session_state.summary_text = ""

#-------------------------------------------------
# Let's write the function to extract text from PDFs
#-------------------------------------------------
def extract_text_from_pdf(uploaded_file):
    #Let's define a variable to read the uploaded pdfs
    pdf_reader = pypdf.PdfReader(uploaded_file)
    text = ""

    for page in pdf_reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"

    return text


#-------------------------------------------------
# Function to store the data in FAISS
#-------------------------------------------------
def store_in_faiss(text, file_name):
    st.write(f"📥 Storing document '{file_name}' in FAISS")

    # Split the text into chunks
    splitter = CharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )
    chunks = splitter.split_text(text)

    # Convert text into embeddings and store each chunk
    for chunk in chunks:
        embedding = embeddings.embed_documents([chunk])
        vector = np.array(embedding, dtype=np.float32)

        # Store vector in FAISS
        st.session_state.faiss_index.add(vector)

        # Store metadata in the same order
        st.session_state.vector_store.append({
            "source": file_name,
            "content": chunk
        })

    return f"🟢 {len(chunks)} chunks stored successfully"


#-------------------------------------------------
# Function to generate AI summary
#-------------------------------------------------
def generate_summary(text):
    st.write("🧠 Generating AI summary...")

    st.session_state.summary_text = llm.invoke(
        f"Summarize the following document:\n\n{text[:3000]}"
    )

    return st.session_state.summary_text


#-------------------------------------------------
# Function to retrieve chunks and answer questions
#-------------------------------------------------
def retrieve_and_answer(query):
    # Safety check: no vectors stored
    if st.session_state.faiss_index.ntotal == 0:
        return "⚠️ No document indexed yet. Please upload a PDF first."

    # Convert user query into embedding
    query_embedding = embeddings.embed_query(query)
    query_vector = np.array(query_embedding, dtype=np.float32).reshape(1, -1)

    # Search FAISS
    distances, indices = st.session_state.faiss_index.search(query_vector, k=3)

    context = ""

    for idx in indices[0]:
        # FAISS may return -1 if no match
        if idx == -1:
            continue

        # Ensure index exists in vector_store
        if idx < len(st.session_state.vector_store):
            context += st.session_state.vector_store[idx]["content"] + "\n\n"

    if not context.strip():
        return "🤖 No relevant data found in the document."

    # Ask AI to generate an answer
    return llm.invoke(
        f"Based on the following context, answer the question:\n\n"
        f"{context}\n\n"
        f"Question: {query}\nAnswer:"
    )


#-------------------------------------------------
# Function to allow file download
#-------------------------------------------------
def download_summary():
    if st.session_state.summary_text:
        st.download_button(
            label="📥 Download summary",
            data=st.session_state.summary_text,
            file_name="AI_summary.txt",
            mime="text/plain"
        )


#-------------------------------------------------
# STREAMLIT WEB UI
#-------------------------------------------------
st.title("🤖 AI-Powered Document Reader & Q&A Bot")
st.write("🔗 Upload a PDF and get an AI-generated summary!")

# File uploader
uploaded_file = st.file_uploader(
    "📂 Upload a PDF document",
    type=["pdf"]
)

if uploaded_file:
    document_text = extract_text_from_pdf(uploaded_file)

    # Store document in FAISS
    status = store_in_faiss(document_text, uploaded_file.name)
    st.success(status)

    # Generate summary
    summary = generate_summary(document_text)
    st.subheader("📄 AI Generated Summary")
    st.write(summary)

    # Enable summary download
    download_summary()

# User input for Q&A
query = st.text_input("❓ Ask a question based on the uploaded document:")
if query:
    answer = retrieve_and_answer(query)
    st.subheader("🤖 AI Answer")
    st.write(answer)
