# AI Agents Udemy Course Repository

This repository contains code and projects from my Udemy course on building AI agents. It demonstrates the progression from basic text-based chatbots to advanced voice-powered assistants using local LLMs like Ollama.

## Overview

The course is structured into days, each building upon the previous one:

- **Day 1**: Basic AI agents with text input, memory, and web UI using Streamlit.
- **Day 2**: Voice-powered AI assistant with speech recognition and text-to-speech capabilities.

All agents use LangChain for prompt management and Ollama for running local LLMs (e.g., qwen2.5:3b).

## Features

- **Conversational Memory**: Agents remember past interactions for context-aware responses.
- **Web UI**: Interactive chat interface using Streamlit.
- **Voice Interaction**: Speech-to-text and text-to-speech for hands-free operation.
- **Local LLM Integration**: Runs AI models locally via Ollama for privacy and offline use.
- **Modular Code**: Easy to extend and customize.

## Project Structure

```
AiChatbotUdemyCourse/
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── day1/                     # Day 1: Basic AI Agents
│   ├── basic_ai_agent.py     # Combined script with multiple versions
│   ├── version1.py           # Web UI version
│   ├── version2.py           # Alternative Web UI implementation
│   └── packages.sh           # Installation script for Day 1
├── day2/                     # Day 2: Voice Assistant
│   ├── ai_voice_assistant.py # Main voice assistant script
│   ├── version2.py           # Web UI version (similar to day1)
│   ├── Readme.md             # Day 2 specific notes
│   └── dependencies.sh       # Installation script for Day 2
└── other files...            # Additional scripts (e.g., guessnumber.py, Recall.py)
```

## Prerequisites

- Python 3.8+
- Ollama installed and running locally (download from [ollama.ai](https://ollama.ai))
- Pull required models: `ollama pull qwen2.5:3b` (or your preferred model)
- Microphone for voice input (Day 2)
- Speakers/headphones for voice output (Day 2)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/AiChatbotUdemyCourse.git
   cd AiChatbotUdemyCourse
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

   Or run the day-specific scripts:
   - For Day 1: `./day1/packages.sh`
   - For Day 2: `./day2/dependencies.sh`

3. Ensure Ollama is running and models are pulled.

## Usage

### Day 1: Basic AI Agents

#### Text-based CLI Agent
Run the basic agent without UI:
```bash
python day1/basic_ai_agent.py
```
Type questions and get responses. Type 'exit' to quit.

#### Web UI Agent
Launch the Streamlit app:
```bash
streamlit run day1/version1.py
# or
streamlit run day1/version2.py
```
Open the provided URL in your browser for an interactive chat with memory.

### Day 2: Voice Assistant

Run the voice-powered assistant:
```bash
python day2/ai_voice_assistant.py
```
Speak commands/questions. The AI will listen, process, and respond via speech. Say "exit" or "stop" to quit.

## Notes

- Adjust the LLM model in the scripts if you have different Ollama models installed.
- For voice features, ensure your microphone is working and permissions are granted.
- The web UI versions include chat history display.
- Code includes commented-out sections for different implementations.

## Contributing

This is a personal learning repository, but feel free to fork and experiment!

## License

MIT License - see LICENSE file for details (if applicable).
