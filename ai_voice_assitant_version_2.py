# Let imports
import speech_recognition as sr
import pyttsx3
from langchain_ollama import OllamaLLM

# Load the AI model (ensure Ollama is running locally and the model is pulled)
llm = OllamaLLM(model="qwen2.5:3b")

#3.Initialize chat history
chat_history = []  # each entry: {'user': str, 'ai': str}

#4.Initialising the text to speech engine

engine = pyttsx3.init()
engine.setProperty('rate', 140)  # Adjust speaking speed

#5.Speech Recognition
recognizer = sr.Recognizer()

#6.Function to speak
def speak(text: str) -> None:
    """Speak the given text aloud."""
    engine.say(text)
    engine.runAndWait()

#7.Function to listen
def listen(timeout: float = 5, phrase_time_limit: float = 10) -> str:
    """Listen on the default microphone and return recognized text (lowercased).

    Returns an empty string on failure or if nothing recognized.
    """
    with sr.Microphone() as source:
        print("\nListening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
        except sr.WaitTimeoutError:
            print("⏱️ Listening timed out, try speaking again.")
            return ""
    try:
        query = recognizer.recognize_google(audio)
        print(f"👂 You said: {query}")
        return query.lower()
    except sr.UnknownValueError:
        print("🤖 Sorry, I couldn't understand. Try again!")
        return ""
    except sr.RequestError as e:
        print(f"⚠️ Speech recognition service unavailable: {e}")
        return ""


def build_prompt(question: str) -> str:
    """Build a simple prompt including recent conversation history."""
    history_lines = []
    for entry in chat_history:
        user = entry.get('user', '')
        ai = entry.get('ai', '')
        if user:
            history_lines.append(f"User: {user}")
        if ai:
            history_lines.append(f"AI: {ai}")
    history_text = "\n".join(history_lines)
    prompt = f"Previous conversation:\n{history_text}\nUser: {question}\nAI:"
    return prompt

def run_chain(question: str) -> str:
    """Send the prompt to the LLM and return the text response."""
    prompt_text = build_prompt(question)

    try:
        # Support different wrappers: prefer `.invoke`, fall back to callable interface
        if hasattr(llm, 'invoke'):
            response_obj = llm.invoke(prompt_text)
            # try to extract a text string from common response shapes
            if isinstance(response_obj, str):
                text = response_obj
            else:
                text = getattr(response_obj, 'text', str(response_obj))
        else:
            maybe = llm(prompt_text)
            if isinstance(maybe, str):
                text = maybe
            else:
                text = getattr(maybe, 'text', str(maybe))
    except Exception as e:
        print("⚠️ Error calling the LLM:", e)
        text = "Sorry, I couldn't get a response from the model."

    # Update chat history
    chat_history.append({'user': question, 'ai': text})
    return text


if __name__ == '__main__':
    speak("Hello, I'm your AI assistant. How can I help you today?")
    try:
        while True:
            query = listen()
            if not query:
                continue
            if 'exit' in query or 'stop' in query:
                speak('Goodbye, have a great day')
                break
            response = run_chain(query)
            print(f"\n🤖 AI response: {response}")
            speak(response)
    except KeyboardInterrupt:
        print('\nExiting...')
