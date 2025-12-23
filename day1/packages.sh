#!/bin/bash
# This is the package file for day 1 of building ai chatbot using python and ollama
# 
echo -e "\n=========Installing  ollama package========"
pip install ollama langchain langchain-ollama langchain-community*
pip install streamlit 
echo  -e "\n=========Packages installed successfully=========\n."

#I install this packages to used then to build a chatbot using qwen2.5:3b as model