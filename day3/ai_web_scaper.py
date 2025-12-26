#This will be an ai_web_scraper agent
#Let's import our newly installed modules

import requests
from bs4 import BeautifulSoup
import streamlit as st
from langchain_ollama import OllamaLLM

llm=OllamaLLM(model="qwen2.5:3b")

#Let's write the function to scrape a website
def scrape_website(url):
    try:
        st.write(f'🌍 Scraping Website :{url}')
        headers = {"User-Agent":"Mozilla/5.0"}
        response = requests.get(url,headers=headers)

    #Let's check if request is successful
        if response.status_code!=200:
            return f'Failed to fetch {url}'

    #Extract the page content
        soup = BeautifulSoup(response.text,"html.parser")
        paragraphs = soup.find_all("p") #Permit to extract all the paragraphs in an HTML page
        text ="".join([p.get_text() for p in paragraphs])

        return text[:2000]
    except Exception as e:
        return f'❌ Error : {str(e)}'

# Function to summarise content
def summarise_content(content):
    st.write("✍️ Summarising content")
    return llm.invoke(f'Summarise the following content :\n\n{content[:1000]}')


#Streamlit UI
st.title("🤖 AI-Powered Web Scraper")
st.write("Enter a Website URL below and get a summarized version")

#User_input
url = st.text_input('Enter a url :')
if url:
    content = scrape_website(url)
    if 'Failed' in content or "❌ Error" in content:
        st.write(content)
    else:
        summary= summarise_content(content)
        st.subheader("📄 Website Summary")
        st.write(summary)
