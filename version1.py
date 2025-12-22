#This is the initail code written in python only made for starting conversations with our AI-models

from langchain_ollama import OllamaLLM #use to import an LLM model

llm=OllamaLLM(model="qwen2.5:3b") #Any model can be used here
print("\n Welcome to your AI agent,How can i help you today")
while True:
    question= input("Your Question(or type exit to stop) :")
    if question.lower() == 'exit':
        print('Good bye')
        break
    reponse = llm.invoke(question)
    print("\n AI repsonse is :",reponse )  