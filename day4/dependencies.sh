#!/bin/bash
#The file will used to install all the dependencies needed for  day 4

set -e
echo  -e "=====================Installing Day4 dependencies===================="
pip install pypdf  faiss-cpu langchain langchain_ollama  streamlit langchain_huggingface

echo -e " 🟢====================Installation complete==============================="