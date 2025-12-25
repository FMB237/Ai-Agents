# This is the GUI for our AI Voice Assistant
# This version uses Streamlit (like in day 1)

import streamlit as st
import speech_recognition as sr
import pyttsx3

from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.prompts import PromptTemplate
from langchain_ollama import OllamaLLM


# ---------------------------
# LLM INITIALIZATION
# ---------------------------
# Load the local Ollama model
llm = OllamaLLM(model="qwen2.5:3b")


# ---------------------------
# SESSION STATE (CHAT MEMORY)
# ---------------------------
# Streamlit needs session_state to persist memory
if "chat_history" not in st.session_state:
    st.session_state.chat_history = ChatMessageHistory()


# ---------------------------
# TEXT TO SPEECH ENGINE
# ---------------------------
engine = pyttsx3.init()
engine.setProperty("rate", 140)

def speak(text):
    """Convert text to speech"""
    engine.say(text)
    engine.runAndWait()


# ---------------------------
# SPEECH RECOGNITION
# ---------------------------
recogniser = sr.Recognizer()

def listen():
    """Listen from microphone and convert speech to text"""
    with sr.Microphone() as source:  # MUST be sr.Microphone()
        print("\n🎧 Listening...")
        recogniser.adjust_for_ambient_noise(source)
        audio = recogniser.listen(source)

    try:
        query = recogniser.recognize_google(audio)
        print(f"👂 You said: {query}")
        return query.lower()

    except sr.UnknownValueError:
        print("🤖 Sorry, I couldn't understand. Try again!")
        return ""

    except sr.RequestError:
        print("⚠️ Speech recognition service unavailable")
        return ""


# ---------------------------
# PROMPT TEMPLATE
# ---------------------------
prompt = PromptTemplate(
    input_variables=["chat_history", "question"],
    template=(
        "Previous conversation:\n{chat_history}\n\n"
        "User: {question}\n"
        "AI:"
    )
)


# ---------------------------
# AI RESPONSE FUNCTION
# ---------------------------
def run_chain(question):
    """Generate AI response and update memory"""

    # Convert chat history to text
    chat_history_text = "\n".join(
        [f"{msg.type.capitalize()}: {msg.content}"
         for msg in st.session_state.chat_history.messages]
    )

    # Invoke the LLM
    response = llm.invoke(
        prompt.format(
            chat_history=chat_history_text,
            question=question
        )
    )

    # Store conversation in memory
    st.session_state.chat_history.add_user_message(question)
    st.session_state.chat_history.add_ai_message(response)

    return response


# ---------------------------
# STREAMLIT UI
# ---------------------------
st.title("🤖 AI Voice Assistant")
st.write("🎤 Click the button below to speak with your AI assistant")

# Button to start listening
if st.button("🎤 Start Listening"):
    user_query = listen()

    if user_query:
        ai_response = run_chain(user_query)

        st.write(f"**You:** {user_query}")
        st.write(f"**AI:** {ai_response}")

        # Speak the response
        speak(ai_response)


# ---------------------------
# DISPLAY CHAT HISTORY
# ---------------------------
st.subheader("📜 Chat History")

for msg in st.session_state.chat_history.messages:
    st.write(f"**{msg.type.capitalize()}**: {msg.content}")
