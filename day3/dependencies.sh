#!/bin/bash
#Installing dependencies for day3
#Let some add the activation script before installing our programs

set -e
echo  -e "Installing day3 app dependencies"
pip install  requests beautifulsoup4 streamlit langchain langchain_ollama

echo -e "Installing dependencies for data storing in vector database"
pip install faiss-cpu chromadb langchain_huggingface   #Where one manage the DB and the other help in storing data in vector formed


pip install -U sentence-transformers torch transformers


echo -e "====================Installation complete================="
