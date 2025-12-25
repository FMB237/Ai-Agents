#Let import our libraries
import speech_recognition as sr
import pyttsx3 
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.prompts import PromptTemplate
from langchain_ollama import OllamaLLM

#2.Let load our Ai model
llm = OllamaLLM(model="qwen2.5:3b")

#3.Initialize chat history
chat_history =ChatMessageHistory() #To store pass conversion between the ai and user

#4.Initialising the text to speech engine

engine =pyttsx3.init()
engine.setProperty('rate',140) #Ajusting the  speaking speed

#5.Speech Recongnition
recognise =sr.Recognizer()

#6.Function to speak
def speak(text):
    engine.say(text)
    engine.runAndWait()

#7.Function to listen
def listen():
    with sr.Microphone() as source :
        print("\n Listening...")
        recognise.adjust_for_ambient_noise(source) #To consider the bachgroundnoise
        audio = recognise.listen(source)
    try:
        query =recognise.recognize_google(audio)    
        print(f'👂You said : {query}')
        return query.lower()
    except sr.UnknownValueError:
        print(" 🤖 Sorry i coudn't understand, Try again!")
        return ""
    except sr.RequestError:
        print("⚠️ Speech recognisation service Unavaliable")      


#8.AI chat Prompt
prompt = PromptTemplate(
    input_variables=["chat_history","question"],
    template="Previous conversation:{chat_history}\nUser :{question}\nAI"
    )

#9.Function to process AI response
def run_chain(question):
     chat_history_text = "\n".join([f"{msg.type.capitalize()} : {msg.content}" for msg in chat_history.messages])

#10.Run the AI response
     response = llm.invoke(prompt.format(chat_history=chat_history_text,question=question))

     chat_history.add_user_message(question)
     chat_history.add_ai_message(response)

     return response


#11.Main loop
speak("Hello,I'm your AI assitant how can i help you today  ?")
while True:
    query = listen()
    if'exit' in query or "stop" in query:
        speak("Goodbye,have a great day")
        break
    if query:
        response =run_chain(query)
        print(f"\n 🤖 AI respone {response}")
        speak(response)
