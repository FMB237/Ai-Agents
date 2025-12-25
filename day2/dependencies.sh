#!/bin/bash
#These are the needed dependecies we need to install for our AI power assitant

set -e
echo "Installing our AI Assitant dependencies"
pip install langchain-core langchain-community langchain-ollama speechrecognition pyttsx3 pyaudio
sudo apt-get update && sudo apt-get install -y portaudio19-dev

