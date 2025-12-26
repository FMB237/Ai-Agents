#!/bin/bash
#Installing dependencies for day3

set -e
echo  -e "Installing day3 app dependencies"
pip install  requests beautifulsoup4 streamlit langchain langchain_ollama

