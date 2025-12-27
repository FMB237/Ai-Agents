#This is a more advanced version of the ai_document_reader.py
#In this version user will be able to download summarized AI analysis

#Now let's import our modules
import streamlit as st
import faiss
import numpy as np
import pypdf
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import OllamaLLM
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import CharacterTextSplitter

llm = OllamaLLM(model="qwen2.5:3b") #Import our AI model

#Load Hugging face Embeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

#Initialise file in the database
index = faiss.IndexFlatL2(384)
vector_store = [] #To store the vector and metadata
#Let's create a summary text variable
summary_text = ""

#Let's write the function to extract text from PDFs
def extract_text_from_pdf(uploaded_file):
    #Let's define a variable to read the uploaded pdfs
    pdf_reader = pypdf.PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text

# Function to store the data in FAISS
def store_in_faiss(text, url):
    global index, vector_store
    st.write(f"📥 Storing document '{url}' in FAISS")

    # Split the text into chunks
    splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    texts = splitter.split_text(text)

    # Convert text into embeddings and store each chunk
    for chunk in texts:
        vector = embeddings.embed_documents([chunk])
        vector = np.array(vector, dtype=np.float32)
        index.add(vector)
        vector_store.append((url, chunk))

    return "🟢 Data stored successfully"


#Function to generate AI summary
def generate_summary(text):
    global summary_text
    st.write("Generating AI summary")
    summary_text = llm.invoke(f"Summarize the following document:\n\n{text[:3000]}")  # Limiting input size
    return summary_text



# Function to retrieve chunks and answer questions
def retrieve_and_answer(query):
    global index, vector_store

    # Convert user query into an embedding
    query_vector = np.array(embeddings.embed_query(query), dtype=np.float32).reshape(1, -1)

    # Search FAISS
    D, I = index.search(query_vector, k=2)  # Used to retrieve top similar chunks

    context = ""
    for idx in I[0]:
        if idx < len(vector_store):
            context += vector_store[idx][1] + "\n\n"
    if not context:
        return "🤖 No relevant data found."
    # Ask AI to generate an answer
    return llm.invoke(f"Based on the following context, answer the question:\n\n{context}\n\nQuestion: {query}\nAnswer:")


#Function to allow file download
def download_summary():
    if summary_text:
        st.download_button(label="📥 Download summaty",data=text,filename="AI_summary.txt",mime="text/plain")

# Streamlit Web UI
st.title("🤖 AI-Powered Document Reader & Q&A bot")
st.write("🔗 Upload a PDF and get an AI generated summary!")

# File uploaded
uploaded_file = st.file_uploader("📂 Upload a PDF document", type=["pdf"])
if uploaded_file:
    text = extract_text_from_pdf(uploaded_file)
    store_message = store_in_faiss(text, uploaded_file.name)
    st.write(store_message)

    # Generate AI summary
    summary = generate_summary(text)
    st.subheader("AI Generated Summary")
    st.write(summary)

    # Enable File Download for Summary
    download_summary()

# User input for Q&A
query = st.text_input("❓ Ask a question based on the uploaded document:")
if query:
    answer = retrieve_and_answer(query)
    st.subheader("🤖 AI Answer:")
    st.write(answer)
