# Let import our libraries
import speech_recognition as sr
import pyttsx3 
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_ollama import OllamaLLM

# Initialize chat history
chat_history = ChatMessageHistory()  # To store past conversations between the AI and user

# Initialize the text to speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 160)  # Adjusting the speaking speed

# Speech Recognition
recognizer = sr.Recognizer()

# Function to speak
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to listen
def listen():
    with sr.Microphone() as source:
        print("\nListening...")
        recognizer.adjust_for_ambient_noise(source)  # To consider the background noise
        audio = recognizer.listen(source)
    try:
        query = recognizer.recognize_google(audio)    
        print(f'👂 You said: {query}')
        return query.lower()
    except sr.UnknownValueError:
        print("🤖 Sorry, I couldn't understand. Try again!")
        return ""
    except sr.RequestError:
        print("⚠️ Speech recognition service unavailable")
        return ""

# AI chat Prompt - Using proper ChatPromptTemplate
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI assistant. Answer the user's questions clearly and concisely."),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{question}")
])

# Load our AI model (moved to avoid loading if there's an error earlier)
llm = OllamaLLM(model="qwen2.5:3b")

# Function to process AI response
def run_chain(question):
    # Format the chat history for the prompt
    history_messages = chat_history.messages
    
    # Run the AI response
    response = chain.invoke({
        "chat_history": history_messages,
        "question": question
    })
    
    # Extract text from response
    if isinstance(response, dict) and 'text' in response:
        response_text = response['text']
    else:
        response_text = str(response)
    
    # Update chat history
    chat_history.add_user_message(question)
    chat_history.add_ai_message(response_text)
    
    return response_text

# Alternative simpler function without LLMChain
def run_chain_simple(question):
    """Simpler version without LLMChain"""
    # Build conversation history
    conversation_history = ""
    for message in chat_history.messages:
        if isinstance(message, HumanMessage):
            conversation_history += f"Human: {message.content}\n"
        elif isinstance(message, AIMessage):
            conversation_history += f"AI: {message.content}\n"
    
    # Create prompt with history
    full_prompt = f"""Previous conversation:
{conversation_history}
Human: {question}
AI: """
    
    # Get response from LLM
    response = llm.invoke(full_prompt)
    
    # Update chat history
    chat_history.add_user_message(question)
    chat_history.add_ai_message(response)
    
    return response

# Main loop
def main():
    speak("Hello, I'm your AI assistant. How can I help you today?")
    print("AI: Hello, I'm your AI assistant. How can I help you today?")
    
    while True:
        query = listen()
        if not query:
            continue
            
        if 'exit' in query or 'stop' in query or 'quit' in query:
            speak("Goodbye! Have a great day!")
            print("🤖 Goodbye! Have a great day!")
            break
            
        try:
            response = run_chain_simple(query)  # Using simpler version
            print(f"\n🤖 AI: {response}")
            speak(response)
        except Exception as e:
            error_msg = f"Sorry, I encountered an error: {str(e)}"
            print(f"❌ Error: {e}")
            speak("Sorry, I encountered an error. Please try again.")

if __name__ == "__main__":
    main()